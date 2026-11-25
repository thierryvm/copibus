"""Summarise SNCB replacement-bus services (route_type 700) in the SNCB GTFS.

Usage: python -I analyze_sncb_bus.py <sncb-gtfs.zip> <report.json> [station_name ...]

Standard library only. Reads the zip without extracting it.
"""
import collections
import csv
import datetime
import io
import json
import sys
import zipfile


def rows(z, name):
    with z.open(name) as fh:
        yield from csv.DictReader(io.TextIOWrapper(fh, "utf-8-sig"))


def parent_id(stop_id, stops):
    s = stops.get(stop_id)
    if s and s["parent_station"]:
        return s["parent_station"]
    return stop_id


def main(zip_path, out_path, focus):
    z = zipfile.ZipFile(zip_path)
    names = set(z.namelist())
    info = next(rows(z, "feed_info.txt")) if "feed_info.txt" in names else {}
    feed_version = info.get("feed_version", "")

    routes = {r["route_id"]: r for r in rows(z, "routes.txt")}
    bus_routes = {k: v for k, v in routes.items() if v["route_type"] == "700"}
    stops = {r["stop_id"]: r for r in rows(z, "stops.txt")}

    trips = {}
    for t in rows(z, "trips.txt"):
        if t["route_id"] in bus_routes:
            trips[t["trip_id"]] = t
    services = {t["service_id"] for t in trips.values()}

    dates = collections.defaultdict(set)
    if "calendar.txt" in names:
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for c in rows(z, "calendar.txt"):
            if c["service_id"] not in services:
                continue
            d = datetime.datetime.strptime(c["start_date"], "%Y%m%d").date()
            end = datetime.datetime.strptime(c["end_date"], "%Y%m%d").date()
            while d <= end:
                if c[days[d.weekday()]] == "1":
                    dates[c["service_id"]].add(d)
                d += datetime.timedelta(days=1)
    for c in rows(z, "calendar_dates.txt"):
        if c["service_id"] not in services:
            continue
        d = datetime.datetime.strptime(c["date"], "%Y%m%d").date()
        if c["exception_type"] == "1":
            dates[c["service_id"]].add(d)
        else:
            dates[c["service_id"]].discard(d)

    trip_stops = collections.defaultdict(list)
    for st in rows(z, "stop_times.txt"):
        if st["trip_id"] in trips:
            trip_stops[st["trip_id"]].append((int(st["stop_sequence"]), st["stop_id"]))
    override_stops = collections.Counter()
    if "stop_time_overrides.txt" in names:
        for o in rows(z, "stop_time_overrides.txt"):
            if o["trip_id"] in trips:
                override_stops[o["stop_id"]] += 1

    per_route = collections.defaultdict(lambda: {"trips": 0, "dates": set(), "stations": set(),
                                                 "short_names": set()})
    for tid, t in trips.items():
        r = per_route[t["route_id"]]
        r["trips"] += 1
        r["dates"] |= dates.get(t["service_id"], set())
        r["short_names"].add(t["trip_short_name"])
        for _, sid in sorted(trip_stops[tid]):
            r["stations"].add(stops[parent_id(sid, stops)]["stop_name"] if parent_id(sid, stops) in stops else sid)

    all_dates = sorted(set().union(*[r["dates"] for r in per_route.values()]) if per_route else [])
    route_out = []
    for rid, r in per_route.items():
        d = sorted(r["dates"])
        route_out.append({
            "route_id": rid,
            "long_name": bus_routes[rid]["route_long_name"],
            "trips": r["trips"],
            "first_date": d[0].isoformat() if d else None,
            "last_date": d[-1].isoformat() if d else None,
            "n_dates": len(d),
            "stations": sorted(r["stations"]),
            "trip_short_name_numeric": all(s.isdigit() for s in r["short_names"] if s),
        })
    route_out.sort(key=lambda x: (x["first_date"] or "", x["route_id"]))

    focus_l = [f.lower() for f in focus]
    focus_hits = [r for r in route_out
                  if any(any(f in s.lower() for f in focus_l) for s in r["stations"])]

    stop_kinds = collections.Counter()
    for _, seq in trip_stops.items():
        for _, sid in seq:
            stop_kinds["platform" if stops.get(sid, {}).get("parent_station") else "station_or_other"] += 1

    report = {
        "feed_version": feed_version,
        "bus_routes": len(bus_routes),
        "bus_routes_with_trips": len(per_route),
        "bus_trips": len(trips),
        "bus_trips_without_dates": sum(1 for t in trips.values() if not dates.get(t["service_id"])),
        "date_range": [all_dates[0].isoformat(), all_dates[-1].isoformat()] if all_dates else None,
        "stop_time_kinds": dict(stop_kinds),
        "override_stops_on_bus_trips": len(override_stops),
        "override_stop_examples": override_stops.most_common(10),
        "focus_terms": focus,
        "focus_routes": focus_hits,
        "routes": route_out,
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=1)
    print(json.dumps({k: report[k] for k in report if k not in ("routes", "focus_routes")},
                     ensure_ascii=False, indent=1))
    print("focus routes:", len(focus_hits))
    for r in focus_hits:
        print(" ", r["route_id"], r["long_name"], r["first_date"], r["last_date"], r["trips"], r["stations"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
