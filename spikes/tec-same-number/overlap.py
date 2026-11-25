"""Where do same-number TEC lines actually meet?

Phase 0, verification 9 (second pass). For every public number used by several route_ids,
finds the pairs of routes that serve the same stop place (same parent_station, or same stop_id
when there is no parent). Also lists every route (shared number or not) with stops in the
pilot zone (Liège - Banneux - Aywaille - Remouchamps bounding box).

Usage (from the repository root, after inventory.py):
    python -I spikes/tec-same-number/overlap.py data/raw/tec/gtfs data/raw/tec/inventory

Streams stop_times.txt (~630 MB) once; takes about a minute.
"""

import csv
import json
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

# Pilot zone: Liège Guillemins to Aywaille / Remouchamps, Banneux included (WGS84).
PILOT_BBOX = {"lat_min": 50.44, "lat_max": 50.66, "lon_min": 5.50, "lon_max": 5.85}


def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        yield from csv.DictReader(f)


def in_pilot(lat: float, lon: float) -> bool:
    b = PILOT_BBOX
    return b["lat_min"] <= lat <= b["lat_max"] and b["lon_min"] <= lon <= b["lon_max"]


def main(gtfs_dir: Path, inv_dir: Path) -> None:
    inventory = json.loads((inv_dir / "inventory.json").read_text(encoding="utf-8"))
    shared = inventory["shared"]
    wanted = {i["route_id"]: num for num, items in shared.items() for i in items}

    stops = {}
    for s in read_csv(gtfs_dir / "stops.txt"):
        place = s["parent_station"] or s["stop_id"]
        stops[s["stop_id"]] = (place, s["stop_name"], float(s["stop_lat"]), float(s["stop_lon"]))

    routes = {r["route_id"]: r for r in read_csv(gtfs_dir / "routes.txt")}
    trip_route = {t["trip_id"]: t["route_id"] for t in read_csv(gtfs_dir / "trips.txt")}

    route_places = defaultdict(set)
    route_pilot_stops = defaultdict(set)
    for st in read_csv(gtfs_dir / "stop_times.txt"):
        rid = trip_route.get(st["trip_id"])
        if rid is None:
            continue
        info = stops.get(st["stop_id"])
        if info is None:
            continue
        if rid in wanted:
            route_places[rid].add(info[0])
        if in_pilot(info[2], info[3]):
            route_pilot_stops[rid].add(st["stop_id"])

    place_name = {}
    for place, name, _, _ in stops.values():
        place_name.setdefault(place, name)

    meeting = {}
    for num, items in shared.items():
        pairs = []
        for a, b in combinations([i["route_id"] for i in items], 2):
            common = route_places[a] & route_places[b]
            if common:
                pairs.append(
                    {
                        "routes": [a, b],
                        "common_places": len(common),
                        "examples": sorted(place_name.get(p, p) for p in common)[:5],
                    }
                )
        if pairs:
            meeting[num] = pairs

    pilot = {}
    for num, items in shared.items():
        in_zone = [
            {"route_id": i["route_id"], "long_name": i["long_name"], "pilot_stops": len(route_pilot_stops[i["route_id"]])}
            for i in items
            if route_pilot_stops[i["route_id"]]
        ]
        if len(in_zone) > 1:
            pilot[num] = in_zone

    # Every route with at least one stop in the pilot zone: the list Thierry validates.
    pilot_routes = sorted(
        (
            {
                "number": routes[rid]["route_short_name"].strip(),
                "route_id": rid,
                "long_name": routes[rid]["route_long_name"].strip(),
                "pilot_stops": len(sids),
            }
            for rid, sids in route_pilot_stops.items()
        ),
        key=lambda r: (-r["pilot_stops"], r["route_id"]),
    )

    result = {
        "pilot_bbox": PILOT_BBOX,
        "numbers_with_meeting_routes": len(meeting),
        "pairs_meeting": sum(len(v) for v in meeting.values()),
        "numbers_with_several_routes_in_pilot_zone": len(pilot),
        "meeting": meeting,
        "pilot": pilot,
        "pilot_routes": pilot_routes,
    }
    (inv_dir / "overlap.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")

    print("numbers with routes meeting at a stop place:", len(meeting), "pairs:", result["pairs_meeting"])
    print("routes with stops in the pilot zone:", len(pilot_routes))
    print("numbers with several routes in the pilot zone:", len(pilot))
    for num, rows in sorted(pilot.items()):
        for r in rows:
            print(f"  {num:>4} {r['route_id']:24} {r['pilot_stops']:4} stops  {r['long_name']}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: overlap.py <gtfs_dir> <inventory_dir>")
    main(Path(sys.argv[1]), Path(sys.argv[2]))
