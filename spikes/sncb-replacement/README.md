# Spike: SNCB replacement buses

Summarises the replacement-bus services (`route_type` 700) of the SNCB GTFS. Standard library only; reads the zip without extracting it.

1. Download the anonymous SNCB GTFS (URL in `docs/donnees/sources.md`) into `data/raw/sncb/sncb-gtfs.zip`.
2. Run:

```sh
python -I analyze_sncb_bus.py ../../data/raw/sncb/sncb-gtfs.zip ../../data/raw/sncb/bus-report.json Liège Aywaille Esneux Verviers Spa
```

Infrabel works were queried by hand through the Explore v2.1 API of `opendata.infrabel.be` (dataset `langetermijnplanning-tcr-spoornetwerk`), filtered on `line` and dates.

Result and decision: `docs/adr/0008-navettes-sncb.md`.
