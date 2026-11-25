"""Summarise the TEC GTFS-RT feeds (served as JSON by the BMC gateway).

Usage: python -I analyze_gtfsrt.py <trip-update.json> <vehicle-position.json> <out.json>
"""
import json
import sys
from pathlib import Path
from statistics import quantiles

PILOT_ROUTES = ("gr:tec:L0064-24183", "gr:tec:L0065-24185")


def q(values):
    if len(values) < 2:
        return {"n": len(values)}
    cuts = quantiles(values, n=10)
    return {"n": len(values), "p50": cuts[4], "p90": cuts[8], "max": max(values), "min": min(values)}


def main(tu_path: Path, vp_path: Path, out_path: Path) -> None:
    tu = json.loads(tu_path.read_text(encoding="utf-8"))
    vp = json.loads(vp_path.read_text(encoding="utf-8"))
    now = int(tu["header"]["timestamp"])

    trips = [e["tripUpdate"] for e in tu.get("entity", []) if "tripUpdate" in e]
    has_trip_desc = sum(1 for t in trips if t.get("trip", {}).get("tripId"))
    with_delay, delays, cancelled_stops, total_stops, ages = 0, [], 0, 0, []
    trip_ids, pilot = set(), 0
    for t in trips:
        desc = t.get("trip", {})
        trip_ids.add(desc.get("tripId", ""))
        if desc.get("routeId") in PILOT_ROUTES:
            pilot += 1
        stus = t.get("stopTimeUpdate", [])
        total_stops += len(stus)
        trip_delays = [s[k]["delay"] for s in stus for k in ("arrival", "departure")
                       if isinstance(s.get(k), dict) and "delay" in s[k]]
        cancelled_stops += sum(1 for s in stus if s.get("scheduleRelationship") == 1)
        if trip_delays:
            with_delay += 1
            delays.append(trip_delays[-1])
        ts = t.get("timestamp")
        if isinstance(ts, dict):
            ts = ts.get("low")
        if ts:
            ages.append(now - int(ts))

    vp_trips = {e["vehicle"]["trip"].get("tripId") for e in vp.get("entity", [])
                if "vehicle" in e and e["vehicle"].get("trip")}
    # TripDescriptor.ScheduleRelationship: 0 SCHEDULED, 3 CANCELED.
    trip_rel = {}
    for t in trips:
        key = str(t.get("trip", {}).get("scheduleRelationship", 0))
        trip_rel[key] = trip_rel.get(key, 0) + 1
    # StopTimeUpdate.ScheduleRelationship: 0 SCHEDULED, 1 SKIPPED, 2 NO_DATA.
    stop_rel = {}
    for t in trips:
        for s in t.get("stopTimeUpdate", []):
            key = str(s.get("scheduleRelationship", 0))
            stop_rel[key] = stop_rel.get(key, 0) + 1
    report = {
        "header_timestamp": now,
        "trip_relationships": trip_rel,
        "stop_relationships": stop_rel,
        "trip_updates": len(trips),
        "with_trip_descriptor": has_trip_desc,
        "with_delay": with_delay,
        "stop_time_updates": total_stops,
        "skipped_stops": cancelled_stops,
        "last_delay_s": q(delays),
        "update_age_s": q(ages),
        "pilot_trip_updates": pilot,
        "vehicles": len(vp.get("entity", [])),
        "vp_trips_with_tu": len(vp_trips & trip_ids),
        "vp_trips": len(vp_trips),
        "sample_trip_keys": sorted(trips[0].keys()) if trips else [],
    }
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
