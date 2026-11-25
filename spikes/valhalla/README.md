# Spike: Valhalla bus routing

Routes TEC line patterns through a local Valhalla (`costing: bus`) and compares the result with the GTFS shape.

Setup (local only, data in `data/raw/`, which git ignores):

1. Download `https://download.geofabrik.de/europe/belgium/belgium-latest.osm.pbf` into `data/raw/valhalla/`.
2. Build the tiles and serve them with `ghcr.io/valhalla/valhalla:latest` (pin a tag or digest before reusing this in CI), bound to `127.0.0.1:8002`. Mount `data/raw` as `/data`.
3. In `valhalla.json`, raise `service_limits.bus.max_locations` to 100. The default is 50.

Run:

```sh
python -I compare_routes.py http://127.0.0.1:8002 ../../data/raw/valhalla/compare-report.json <package.json>:<pattern_index> ...
```

Result and decision: `docs/adr/0007-routage-valhalla-bus.md`.
