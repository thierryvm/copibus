"""Compare TEC real-time feeds (SIRI ET vs SIRI VM) against the static GTFS.

Phase 0, verification 10. Reads snapshots already downloaded by fetch.sh (no network here)
and the unzipped static GTFS, then reports:
  - how SIRI identifiers map onto GTFS ids (lines, trips, stops);
  - what each feed carries (positions, expected times, cancellations);
  - freshness (age of each record, update cadence between two VM snapshots);
  - coverage of lines 64 and 65 (gr:tec:L0064-24183, gr:tec:L0065-24185): share of the
    trips scheduled at snapshot time that appear in each feed.

Usage (from the repository root):
    python -I spikes/tec-realtime/analyze.py data/raw/tec/gtfs data/raw/tec/rt
"""

import csv
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

PILOT_ROUTES = ("gr:tec:L0064-24183", "gr:tec:L0065-24185")
REF = re.compile(r"^BE:BMC:[A-Za-z]+:(.*):$")


def norm(gtfs_id: str) -> str:
    """GTFS id -> the form SIRI uses ('gt:tec:123-A-B' -> 'gt_tec_123_A_B')."""
    return gtfs_id.replace(":", "_").replace("-", "_")


def unref(siri_ref: str) -> str:
    m = REF.match(siri_ref or "")
    return m.group(1) if m else (siri_ref or "")


def ts(value: str) -> datetime:
    return datetime.fromisoformat(value)


def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        yield from csv.DictReader(f)


def gtfs_seconds(hms: str) -> int:
    h, m, s = (int(x) for x in hms.split(":"))
    return h * 3600 + m * 60 + s


def pct(part: int, whole: int) -> float:
    return round(100.0 * part / whole, 1) if whole else 0.0


def quantiles(values):
    if not values:
        return None
    v = sorted(values)
    q = lambda p: v[min(len(v) - 1, int(p * (len(v) - 1) + 0.5))]  # noqa: E731
    return {"n": len(v), "min": v[0], "p50": q(0.5), "p90": q(0.9), "max": v[-1]}


def active_services(gtfs_dir: Path, day: date) -> set:
    weekday = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"][day.weekday()]
    key = day.strftime("%Y%m%d")
    active = set()
    for c in read_csv(gtfs_dir / "calendar.txt"):
        if c["start_date"] <= key <= c["end_date"] and c[weekday] == "1":
            active.add(c["service_id"])
    for c in read_csv(gtfs_dir / "calendar_dates.txt"):
        if c["date"] == key:
            if c["exception_type"] == "1":
                active.add(c["service_id"])
            else:
                active.discard(c["service_id"])
    return active


def load_gtfs(gtfs_dir: Path, day: date):
    routes = {norm(r["route_id"]): r["route_id"] for r in read_csv(gtfs_dir / "routes.txt")}
    stops = {norm(s["stop_id"]): s["stop_id"] for s in read_csv(gtfs_dir / "stops.txt")}
    services = active_services(gtfs_dir, day)
    trips, trip_route, pilot_today = {}, {}, set()
    collisions = 0
    for t in read_csv(gtfs_dir / "trips.txt"):
        k = norm(t["trip_id"])
        if k in trips:
            collisions += 1
        trips[k] = t["trip_id"]
        trip_route[t["trip_id"]] = t["route_id"]
        if t["route_id"] in PILOT_ROUTES and t["service_id"] in services:
            pilot_today.add(t["trip_id"])
    # Scheduled window and per-stop times of today's pilot trips.
    window = {}
    sched = defaultdict(dict)
    for st in read_csv(gtfs_dir / "stop_times.txt"):
        tid = st["trip_id"]
        if tid not in pilot_today:
            continue
        dep = gtfs_seconds(st["departure_time"] or st["arrival_time"])
        lo, hi = window.get(tid, (dep, dep))
        window[tid] = (min(lo, dep), max(hi, dep))
        sched[tid][st["stop_id"]] = dep
    return {
        "routes": routes,
        "stops": stops,
        "trips": trips,
        "trip_route": trip_route,
        "trip_id_collisions": collisions,
        "pilot_today": pilot_today,
        "window": window,
        "sched": sched,
    }


def et_journeys(doc):
    frames = doc["ServiceDelivery"]["EstimatedTimetableDelivery"][0]["EstimatedJourneyVersionFrame"]
    for fr in frames:
        yield from fr.get("EstimatedVehicleJourney", [])


def vm_activities(doc):
    yield from doc["ServiceDelivery"]["VehicleMonitoringDelivery"][0].get("VehicleActivity", [])


def analyse_et(doc, g, midnight):
    now = ts(doc["ServiceDelivery"]["ResponseTimestamp"])
    js = list(et_journeys(doc))
    lines, line_ok, trip_ok, stop_total, stop_ok = set(), 0, 0, 0, 0
    with_expected, cancelled, call_cancel = 0, 0, 0
    recorded_keys = Counter()
    pilot = {}
    delays_all, aimed_vs_gtfs = [], []
    for j in js:
        line = unref(j["LineRef"])
        lines.add(line)
        line_ok += line in g["routes"]
        trip = g["trips"].get(unref(j["FramedVehicleJourneyRef"]["DatedVehicleJourneyRef"]))
        trip_ok += trip is not None
        cancelled += bool(j.get("Cancellation"))
        for rc in j.get("RecordedCalls", []):
            recorded_keys.update(rc.keys())
        calls = j.get("EstimatedCalls", [])
        timed = [c for c in calls if "ExpectedDepartureTime" in c or "ExpectedArrivalTime" in c]
        with_expected += bool(timed)
        for c in calls:
            stop_total += 1
            stop_ok += unref(c["StopPointRef"]) in g["stops"]
            call_cancel += bool(c.get("Cancellation"))
        if timed:
            c = timed[0]
            aimed = c.get("AimedDepartureTime") or c.get("AimedArrivalTime")
            exp = c.get("ExpectedDepartureTime") or c.get("ExpectedArrivalTime")
            if aimed and exp:
                delays_all.append(int((ts(exp) - ts(aimed)).total_seconds()))
        if trip in g["pilot_today"]:
            entry = {"has_expected": bool(timed), "cancelled": bool(j.get("Cancellation"))}
            if timed:
                c = timed[0]
                aimed = c.get("AimedDepartureTime") or c.get("AimedArrivalTime")
                exp = c.get("ExpectedDepartureTime") or c.get("ExpectedArrivalTime")
                entry["delay_s"] = int((ts(exp) - ts(aimed)).total_seconds()) if aimed and exp else None
            # Aimed times must match the static timetable (same feed version).
            for c in calls:
                sid = g["stops"].get(unref(c["StopPointRef"]))
                aimed = c.get("AimedDepartureTime") or c.get("AimedArrivalTime")
                if sid and aimed and sid in g["sched"][trip]:
                    secs = int((ts(aimed) - midnight).total_seconds())
                    aimed_vs_gtfs.append(secs - g["sched"][trip][sid])
            pilot[trip] = entry
    return now, {
        "response_timestamp": doc["ServiceDelivery"]["ResponseTimestamp"],
        "recorded_at": doc["ServiceDelivery"]["EstimatedTimetableDelivery"][0]["EstimatedJourneyVersionFrame"][0].get("RecordedAtTime"),
        "journeys": len(js),
        "lines": len(lines),
        "journeys_with_expected_times": with_expected,
        "journeys_cancelled": cancelled,
        "calls": stop_total,
        "calls_cancelled": call_cancel,
        "recorded_call_keys": dict(recorded_keys),
        "join_line_pct": pct(line_ok, len(js)),
        "join_trip_pct": pct(trip_ok, len(js)),
        "join_stop_pct": pct(stop_ok, stop_total),
        "delay_first_timed_call_s": quantiles(delays_all),
        "pilot_aimed_minus_gtfs_s": quantiles(aimed_vs_gtfs),
    }, pilot


def analyse_vm(doc, g):
    now = ts(doc["ServiceDelivery"]["ResponseTimestamp"])
    vas = list(vm_activities(doc))
    ages, validity, trip_ok, monitored = [], [], 0, 0
    pilot, by_vehicle = {}, {}
    for v in vas:
        rec = ts(v["RecordedAtTime"])
        ages.append(int((now - rec).total_seconds()))
        if v.get("ValidUntilTime"):
            validity.append(int((ts(v["ValidUntilTime"]) - rec).total_seconds()))
        mvj = v["MonitoredVehicleJourney"]
        monitored += bool(mvj.get("Monitored"))
        trip = g["trips"].get(unref(mvj["FramedVehicleJourneyRef"]["DatedVehicleJourneyRef"]))
        trip_ok += trip is not None
        loc = mvj.get("VehicleLocation", {})
        by_vehicle[mvj.get("VehicleRef")] = (rec, loc.get("Latitude"), loc.get("Longitude"), trip)
        if trip in g["pilot_today"]:
            pilot[trip] = {"age_s": ages[-1]}
    return now, {
        "response_timestamp": doc["ServiceDelivery"]["ResponseTimestamp"],
        "vehicles": len(vas),
        "monitored_pct": pct(monitored, len(vas)),
        "join_trip_pct": pct(trip_ok, len(vas)),
        "age_s": quantiles(ages),
        "valid_for_s": quantiles(validity),
    }, pilot, by_vehicle


def scheduled_now(g, now, midnight, slack=300):
    """Pilot trips whose scheduled window contains the snapshot time (with 5 min slack)."""
    secs = int((now - midnight).total_seconds())
    return {t for t, (lo, hi) in g["window"].items() if lo - slack <= secs <= hi + slack}


def main(gtfs_dir: Path, rt_dir: Path) -> None:
    et_files = sorted(rt_dir.glob("estimated-timetable-*.json"))
    vm_files = sorted(rt_dir.glob("vehicle-monitoring-*.json"))
    first = json.loads(et_files[0].read_text(encoding="utf-8"))
    now0 = ts(first["ServiceDelivery"]["ResponseTimestamp"])
    day = now0.date()
    midnight = datetime(day.year, day.month, day.day, tzinfo=now0.tzinfo)
    g = load_gtfs(gtfs_dir, day)

    report = {
        "service_day": day.isoformat(),
        "gtfs_trip_id_collisions_after_normalisation": g["trip_id_collisions"],
        "pilot_trips_today": len(g["pilot_today"]),
        "et": [],
        "vm": [],
    }

    for f in et_files:
        now, summary, pilot = analyse_et(json.loads(f.read_text(encoding="utf-8")), g, midnight)
        due = scheduled_now(g, now, midnight)
        summary["pilot_scheduled_now"] = len(due)
        summary["pilot_in_feed"] = len(pilot.keys() & due)
        summary["pilot_with_expected_times"] = sum(1 for t in due if pilot.get(t, {}).get("has_expected"))
        summary["pilot_cancelled"] = sum(1 for t in due if pilot.get(t, {}).get("cancelled"))
        summary["pilot_delay_s"] = quantiles([p["delay_s"] for t, p in pilot.items() if t in due and p.get("delay_s") is not None])
        summary["file"] = f.name
        report["et"].append(summary)

    snapshots = []
    for f in vm_files:
        now, summary, pilot, by_vehicle = analyse_vm(json.loads(f.read_text(encoding="utf-8")), g)
        due = scheduled_now(g, now, midnight)
        summary["pilot_scheduled_now"] = len(due)
        summary["pilot_with_position"] = len(pilot.keys() & due)
        summary["file"] = f.name
        report["vm"].append(summary)
        snapshots.append((now, by_vehicle))

    # Cadence between consecutive VM snapshots: did each vehicle send a new record, and move?
    cadence = []
    for (t0, a), (t1, b) in zip(snapshots, snapshots[1:]):
        common = a.keys() & b.keys()
        updated = [v for v in common if b[v][0] > a[v][0]]
        moved = [v for v in updated if (b[v][1], b[v][2]) != (a[v][1], a[v][2])]
        steps = [int((b[v][0] - a[v][0]).total_seconds()) for v in updated]
        cadence.append(
            {
                "between_s": int((t1 - t0).total_seconds()),
                "vehicles_in_both": len(common),
                "updated_pct": pct(len(updated), len(common)),
                "moved_pct": pct(len(moved), len(common)),
                "record_step_s": quantiles(steps),
            }
        )
    report["vm_cadence"] = cadence

    # Cross-check on the closest pair of snapshots: are VM vehicles also in ET with times?
    if snapshots and et_files:
        last_et = json.loads(et_files[-1].read_text(encoding="utf-8"))
        et_trips = {}
        for j in et_journeys(last_et):
            trip = g["trips"].get(unref(j["FramedVehicleJourneyRef"]["DatedVehicleJourneyRef"]))
            timed = any("ExpectedDepartureTime" in c or "ExpectedArrivalTime" in c for c in j.get("EstimatedCalls", []))
            et_trips[trip] = timed
        vm_trips = {v[3] for v in snapshots[-1][1].values() if v[3]}
        report["vm_trips_found_in_et_pct"] = pct(len(vm_trips & et_trips.keys()), len(vm_trips))
        report["vm_trips_with_et_expected_times_pct"] = pct(sum(1 for t in vm_trips if et_trips.get(t)), len(vm_trips))

    (rt_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: analyze.py <gtfs_dir> <rt_dir>")
    main(Path(sys.argv[1]), Path(sys.argv[2]))
