"""Route TEC line patterns through a local Valhalla (bus costing) and compare with the GTFS shape.

For each chosen pattern, asks Valhalla for a route through every stop in order, then measures
how far the Valhalla geometry strays from the TEC shape (and the reverse).

Usage: python -I compare_routes.py <valhalla-url> <out.json> <package.json>:<pattern_index> [...]
"""
import json
import math
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path


def decode_polyline(s: str, precision: int) -> list[tuple[float, float]]:
    pts, idx, lat, lon, f = [], 0, 0, 0, 10 ** precision
    while idx < len(s):
        for which in (0, 1):
            shift = result = 0
            while True:
                b = ord(s[idx]) - 63
                idx += 1
                result |= (b & 0x1F) << shift
                shift += 5
                if b < 0x20:
                    break
            d = ~(result >> 1) if result & 1 else result >> 1
            if which == 0:
                lat += d
            else:
                lon += d
        pts.append((lat / f, lon / f))
    return pts


def to_xy(p, lat0):
    r = 6371000.0
    return (math.radians(p[1]) * r * math.cos(math.radians(lat0)), math.radians(p[0]) * r)


def point_seg(p, a, b):
    ax, ay = a
    bx, by = b
    px, py = p
    dx, dy = bx - ax, by - ay
    L = dx * dx + dy * dy
    t = 0.0 if L == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)


def densify(xy, step=10.0):
    out = [xy[0]]
    for a, b in zip(xy, xy[1:]):
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) // step))
        for i in range(1, n + 1):
            out.append((a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n))
    return out


def deviations(src, ref):
    """Distance from each densified point of src to the polyline ref (grid-indexed)."""
    cell = 200.0
    grid: dict[tuple[int, int], list[int]] = {}
    for i, (a, b) in enumerate(zip(ref, ref[1:])):
        for gx in range(int(min(a[0], b[0]) // cell) - 1, int(max(a[0], b[0]) // cell) + 2):
            for gy in range(int(min(a[1], b[1]) // cell) - 1, int(max(a[1], b[1]) // cell) + 2):
                grid.setdefault((gx, gy), []).append(i)
    out = []
    for p in densify(src):
        segs = grid.get((int(p[0] // cell), int(p[1] // cell)))
        if segs:
            out.append(min(point_seg(p, ref[i], ref[i + 1]) for i in segs))
        else:
            out.append(min(point_seg(p, a, b) for a, b in zip(ref, ref[1:])))
    return out


def stats(v):
    s = sorted(v)
    pick = lambda q: s[min(len(s) - 1, int(q * len(s)))]  # noqa: E731
    return {"p50": round(pick(.5), 1), "p95": round(pick(.95), 1), "max": round(s[-1], 1),
            "share_over_30m": round(sum(1 for x in s if x > 30) / len(s), 4)}


def route(url, stops):
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != "http" or parts.hostname not in ("127.0.0.1", "localhost"):
        raise RuntimeError("Valhalla must be a local http server (127.0.0.1 or localhost)")
    locs = [{"lat": s["lat"], "lon": s["lon"], "type": "break" if i in (0, len(stops) - 1) else "through"}
            for i, s in enumerate(stops)]
    body = json.dumps({"locations": locs, "costing": "bus", "units": "kilometers",
                       "directions_options": {"language": "fr-FR"}}).encode()
    req = urllib.request.Request(url + "/route", data=body, headers={"Content-Type": "application/json"})
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read())
    return data, time.perf_counter() - t0


def main():
    url, out = sys.argv[1], Path(sys.argv[2])
    results = []
    for arg in sys.argv[3:]:
        path, idx = arg.rsplit(":", 1)
        pkg = json.loads(Path(path).read_text(encoding="utf-8"))
        pat = pkg["patterns"][int(idx)]
        by_id = {s["id"]: s for s in pkg["stops"]}
        stops = [by_id[s] for s in pat["stops"]]
        data, secs = route(url, stops)
        leg = data["trip"]["legs"][0]
        lat0 = stops[0]["lat"]
        v_xy = [to_xy(p, lat0) for p in decode_polyline(leg["shape"], 6)]
        g_xy = [to_xy(p, lat0) for p in decode_polyline(pat["shape"], 5)]
        man = leg["maneuvers"]
        res = {
            "route_id": pkg["route"].get("route_id", pkg["route"].get("id")),
            "pattern": int(idx), "dir": pat["dir"], "stops": len(stops),
            "first": stops[0]["name"], "last": stops[-1]["name"],
            "gtfs_length_m": pat["dist_m"][-1],
            "valhalla_length_m": round(data["trip"]["summary"]["length"] * 1000),
            "valhalla_time_s": round(data["trip"]["summary"]["time"]),
            "query_s": round(secs, 3),
            "maneuvers": len(man),
            "valhalla_vs_gtfs_m": stats(deviations(v_xy, g_xy)),
            "gtfs_vs_valhalla_m": stats(deviations(g_xy, v_xy)),
            "sample_instructions": [m["instruction"] for m in man[:6]],
        }
        results.append(res)
        print(json.dumps(res, ensure_ascii=False))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
