"""Phase 0 spike: build a compact "line package" for TEC routes from GTFS.

Usage (always with -I, data is untrusted):
    python -I build_package.py <gtfs_dir> <out_dir> <route_id> [<route_id> ...]

Stdlib only. Writes <out_dir>/<route_id-sanitised>.json plus a report
(<out_dir>/report.json) with sizes (raw, gzip -9, xz) and checks used by
ADR 0003. The package format is a prototype, not the final contract.
"""

from __future__ import annotations

import csv
import gzip
import json
import lzma
import math
import sys
from collections import defaultdict
from pathlib import Path

SIMPLIFY_TOLERANCE_M = 2.0
EARTH_R = 6371008.8


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        yield from csv.DictReader(f)


def to_sec(hhmmss: str) -> int:
    h, m, s = hhmmss.strip().split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


# --- geometry -------------------------------------------------------------

def project(lat: float, lon: float, lat0: float) -> tuple[float, float]:
    """Local equirectangular projection in metres (fine at corridor scale)."""
    x = math.radians(lon) * EARTH_R * math.cos(math.radians(lat0))
    y = math.radians(lat) * EARTH_R
    return x, y


def rdp(points: list[tuple[float, float]], tol: float) -> list[int]:
    """Ramer-Douglas-Peucker, iterative. Returns kept indices."""
    n = len(points)
    if n < 3:
        return list(range(n))
    keep = [False] * n
    keep[0] = keep[-1] = True
    stack = [(0, n - 1)]
    while stack:
        a, b = stack.pop()
        ax, ay = points[a]
        bx, by = points[b]
        dx, dy = bx - ax, by - ay
        seg2 = dx * dx + dy * dy
        best, best_i = -1.0, -1
        for i in range(a + 1, b):
            px, py = points[i]
            if seg2 == 0:
                d = math.hypot(px - ax, py - ay)
            else:
                t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / seg2))
                d = math.hypot(px - (ax + t * dx), py - (ay + t * dy))
            if d > best:
                best, best_i = d, i
        if best > tol:
            keep[best_i] = True
            stack.append((a, best_i))
            stack.append((best_i, b))
    return [i for i, k in enumerate(keep) if k]


def cumulative(points: list[tuple[float, float]]) -> list[float]:
    out = [0.0]
    for i in range(1, len(points)):
        out.append(out[-1] + math.hypot(points[i][0] - points[i - 1][0],
                                         points[i][1] - points[i - 1][1]))
    return out


def _project(shape_xy, i, sx, sy):
    ax, ay = shape_xy[i]
    bx, by = shape_xy[i + 1]
    dx, dy = bx - ax, by - ay
    seg2 = dx * dx + dy * dy
    t = 0.0 if seg2 == 0 else max(0.0, min(1.0, ((sx - ax) * dx + (sy - ay) * dy) / seg2))
    return math.hypot(sx - (ax + t * dx), sy - (ay + t * dy)), t


def locate_stops(shape_xy, shape_cum, stops_xy):
    """Distance along shape for each stop.

    Global monotonic alignment (dynamic programming): every stop is matched
    to a shape segment so that segment indices never decrease along the stop
    sequence and the sum of stop-to-shape offsets is minimal. A greedy
    nearest-point search fails on out-and-back spurs (e.g. the Banneux loop of
    line 64), where the same road is driven twice: the first stop of the spur
    snaps to the return pass and every following stop is lost.
    Returns (distances, max_offset_m)."""
    nseg = len(shape_xy) - 1
    if nseg < 1 or not stops_xy:
        return [0 for _ in stops_xy], 0.0
    proj = [[_project(shape_xy, i, sx, sy) for i in range(nseg)] for sx, sy in stops_xy]
    inf = float("inf")
    cost_prev = [p[0] for p in proj[0]]
    back = []
    for j in range(1, len(stops_xy)):
        # prefix minimum of the previous row -> best predecessor at index <= i
        best_val, best_idx = inf, 0
        row, brow = [], []
        for i in range(nseg):
            if cost_prev[i] < best_val:
                best_val, best_idx = cost_prev[i], i
            row.append(best_val + proj[j][i][0])
            brow.append(best_idx)
        back.append(brow)
        cost_prev = row
    i = min(range(nseg), key=cost_prev.__getitem__)
    chosen = [i]
    for brow in reversed(back):
        i = brow[i]
        chosen.append(i)
    chosen.reverse()
    dists, worst, last = [], 0.0, 0.0
    for j, i in enumerate(chosen):
        d, t = proj[j][i]
        pos = shape_cum[i] + t * (shape_cum[i + 1] - shape_cum[i])
        pos = max(pos, last)  # same segment, stops out of order by a few metres
        dists.append(round(pos))
        last = pos
        worst = max(worst, d)
    return dists, worst


def encode_polyline(coords: list[tuple[float, float]], precision: int = 5) -> str:
    """Google encoded polyline (lat, lon)."""
    factor = 10 ** precision
    out, plat, plon = [], 0, 0
    for lat, lon in coords:
        ilat, ilon = round(lat * factor), round(lon * factor)
        for v in (ilat - plat, ilon - plon):
            v = ~(v << 1) if v < 0 else (v << 1)
            while v >= 0x20:
                out.append(chr((0x20 | (v & 0x1F)) + 63))
                v >>= 5
            out.append(chr(v + 63))
        plat, plon = ilat, ilon
    return "".join(out)


# --- build ------------------------------------------------------------------

def build(gtfs: Path, route_ids: list[str]):
    wanted = set(route_ids)
    routes = {r["route_id"]: r for r in read_csv(gtfs / "routes.txt") if r["route_id"] in wanted}
    missing = wanted - routes.keys()
    if missing:
        sys.exit(f"route_id not found: {sorted(missing)}")

    trips = {t["trip_id"]: t for t in read_csv(gtfs / "trips.txt") if t["route_id"] in wanted}
    print(f"trips: {len(trips)}", file=sys.stderr)

    stop_times = defaultdict(list)
    for st in read_csv(gtfs / "stop_times.txt"):
        if st["trip_id"] in trips:
            stop_times[st["trip_id"]].append(st)
    for lst in stop_times.values():
        lst.sort(key=lambda s: int(s["stop_sequence"]))

    used_stops = {st["stop_id"] for lst in stop_times.values() for st in lst}
    all_stops = {s["stop_id"]: s for s in read_csv(gtfs / "stops.txt")}
    stops = {sid: all_stops[sid] for sid in used_stops}

    shape_ids = {t["shape_id"] for t in trips.values() if t["shape_id"]}
    shapes = defaultdict(list)
    for p in read_csv(gtfs / "shapes.txt"):
        if p["shape_id"] in shape_ids:
            shapes[p["shape_id"]].append((int(p["shape_pt_sequence"]), float(p["shape_pt_lat"]), float(p["shape_pt_lon"])))
    for lst in shapes.values():
        lst.sort()

    service_ids = {t["service_id"] for t in trips.values()}
    calendar = {c["service_id"]: c for c in read_csv(gtfs / "calendar.txt") if c["service_id"] in service_ids}
    cal_dates = defaultdict(list)
    for c in read_csv(gtfs / "calendar_dates.txt"):
        if c["service_id"] in service_ids:
            cal_dates[c["service_id"]].append((c["date"], int(c["exception_type"])))
    feed = next(read_csv(gtfs / "feed_info.txt"))
    return routes, trips, stop_times, stops, all_stops, shapes, calendar, cal_dates, feed


def make_package(route_id, routes, trips, stop_times, stops, all_stops, shapes, calendar, cal_dates, feed):
    r = routes[route_id]
    rtrips = [t for t in trips.values() if t["route_id"] == route_id]

    # Patterns: (direction, shape, stop sequence) -> index
    pattern_key_to_idx, patterns = {}, []
    profiles_idx, profiles = {}, []
    headsigns, services, out_trips = [], [], []
    loop_info = {}
    lat0 = sum(float(s["stop_lat"]) for s in stops.values()) / len(stops)

    for t in sorted(rtrips, key=lambda t: (t["direction_id"], to_sec(stop_times[t["trip_id"]][0]["departure_time"]))):
        sts = stop_times[t["trip_id"]]
        seq = tuple(s["stop_id"] for s in sts)
        key = (t["direction_id"], t["shape_id"], seq)
        if key not in pattern_key_to_idx:
            pts = shapes.get(t["shape_id"], [])
            latlon = [(la, lo) for _, la, lo in pts]
            xy = [project(la, lo, lat0) for la, lo in latlon]
            kept = rdp(xy, SIMPLIFY_TOLERANCE_M)
            s_latlon = [latlon[i] for i in kept]
            s_xy = [xy[i] for i in kept]
            s_cum = cumulative(s_xy)
            stops_xy = [project(float(stops[s]["stop_lat"]), float(stops[s]["stop_lon"]), lat0) for s in seq]
            dists, worst = locate_stops(s_xy, s_cum, stops_xy) if s_xy else ([], None)
            dup = len(seq) - len(set(seq))
            pattern_key_to_idx[key] = len(patterns)
            patterns.append({
                "dir": int(t["direction_id"]),
                "stops": list(seq),
                "dist_m": dists,
                "shape": encode_polyline(s_latlon),
                "_shape_points_raw": len(latlon),
                "_shape_points_kept": len(kept),
                "_length_m": round(s_cum[-1]) if s_cum else 0,
                "_max_stop_offset_m": round(worst, 1) if worst is not None else None,
                "_repeated_stops": dup,
                "_monotonic": all(b >= a for a, b in zip(dists, dists[1:])),
            })
        p_idx = pattern_key_to_idx[key]

        t0 = to_sec(sts[0]["departure_time"])
        prof = tuple((to_sec(s["arrival_time"]) - t0, to_sec(s["departure_time"]) - t0) for s in sts)
        # compact: list of [arr_offset, dwell] ; dwell mostly 0
        if prof not in profiles_idx:
            profiles_idx[prof] = len(profiles)
            profiles.append([[a, d - a] if d != a else a for a, d in prof])
        if t["trip_headsign"] not in headsigns:
            headsigns.append(t["trip_headsign"])
        if t["service_id"] not in services:
            services.append(t["service_id"])
        out_trips.append([
            p_idx, profiles_idx[prof], t0, services.index(t["service_id"]),
            headsigns.index(t["trip_headsign"]), t["block_id"], t["trip_id"],
        ])

    used = sorted({s for p in patterns for s in p["stops"]})
    stop_list = []
    for sid in used:
        s = stops[sid]
        parent = all_stops.get(s["parent_station"], {}) if s["parent_station"] else {}
        stop_list.append({
            "id": sid,
            "name": s["stop_name"],
            "lat": round(float(s["stop_lat"]), 6),
            "lon": round(float(s["stop_lon"]), 6),
            "quai": s["platform_code"] or None,
            "parent": s["parent_station"] or None,
            "parent_name": parent.get("stop_name") or None,
        })

    cal = []
    for sid in services:
        c = calendar.get(sid)
        days = "".join(c[d] for d in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")) if c else None
        cal.append({
            "id": sid,
            "days": days,
            "start": c["start_date"] if c else None,
            "end": c["end_date"] if c else None,
            "add": sorted(d for d, e in cal_dates.get(sid, []) if e == 1),
            "remove": sorted(d for d, e in cal_dates.get(sid, []) if e == 2),
        })

    pkg = {
        "format": "copibus-line-package/0-spike",
        "source": {
            # Fields required by ADR 0002 (CC BY 4.0 attribution).
            "operator": "TEC",
            "attribution": "Source : TEC – Open Data, via Belgian Mobility Company",
            "portal_url": "https://data.belgianmobility.io",
            "licence": "CC BY 4.0",
            "licence_url": "https://creativecommons.org/licenses/by/4.0/",
            "modified": "Contient des données publiées à l'origine par le TEC, modifiées par Copibus.",
            "feed_version": feed["feed_version"].strip(),
            "feed_start": feed["feed_start_date"].strip(),
            "feed_end": feed["feed_end_date"].strip(),
        },
        "route": {
            "id": route_id,
            "short_name": r["route_short_name"],
            "long_name": r["route_long_name"],
            "color": r["route_color"],
            "text_color": r["route_text_color"],
        },
        "stops": stop_list,
        "patterns": patterns,
        "time_profiles": profiles,
        "headsigns": headsigns,
        "services": cal,
        "trips_columns": ["pattern", "profile", "start_s", "service", "headsign", "block_id", "trip_id"],
        "trips": out_trips,
    }
    return pkg


def strip_debug(pkg):
    out = json.loads(json.dumps(pkg))
    for p in out["patterns"]:
        for k in [k for k in p if k.startswith("_")]:
            del p[k]
    return out


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    gtfs, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    route_ids = sys.argv[3:]
    out_dir.mkdir(parents=True, exist_ok=True)
    data = build(gtfs, route_ids)
    report = {}
    for rid in route_ids:
        pkg = make_package(rid, *data)
        lean = strip_debug(pkg)
        raw = json.dumps(lean, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        name = rid.replace(":", "_")
        (out_dir / f"{name}.json").write_bytes(raw)
        (out_dir / f"{name}.debug.json").write_text(json.dumps(pkg, ensure_ascii=False, indent=1), encoding="utf-8")
        report[rid] = {
            "trips": len(pkg["trips"]),
            "patterns": len(pkg["patterns"]),
            "time_profiles": len(pkg["time_profiles"]),
            "stops": len(pkg["stops"]),
            "services": len(pkg["services"]),
            "bytes_raw": len(raw),
            "bytes_gzip9": len(gzip.compress(raw, 9)),
            "bytes_xz": len(lzma.compress(raw, preset=9)),
            "patterns_detail": [
                {k: p[k] for k in ("dir", "_shape_points_raw", "_shape_points_kept", "_length_m",
                                    "_max_stop_offset_m", "_repeated_stops", "_monotonic")}
                | {"n_stops": len(p["stops"]),
                   "first": pkg["stops"][[s["id"] for s in pkg["stops"]].index(p["stops"][0])]["name"],
                   "last": pkg["stops"][[s["id"] for s in pkg["stops"]].index(p["stops"][-1])]["name"]}
                for p in pkg["patterns"]
            ],
        }
    (out_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    summary = {rid: {k: v for k, v in rep.items() if k != "patterns_detail"} for rid, rep in report.items()}
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
