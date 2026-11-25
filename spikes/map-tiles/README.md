# Spike: offline map tiles (PMTiles)

Measures the size of a PMTiles extract for a bounding box using HTTP range requests, without downloading the archive. Standard library only.

```sh
python -I measure_pmtiles.py https://build.protomaps.com/20261124.pmtiles 5.5 50.44 5.85 50.66 15 ../../data/raw/tiles/corridor-report.json
```

Result and decision: `docs/adr/0006-tuiles-hors-ligne.md`.
