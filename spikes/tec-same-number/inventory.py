"""Inventory of TEC lines that share the same public number (route_short_name).

Phase 0, verification 9. Reads the static TEC GTFS (already unzipped) and lists every
route_short_name used by more than one route_id, with region, long name and trip count.

Usage (from the repository root):
    python -I spikes/tec-same-number/inventory.py data/raw/tec/gtfs data/raw/tec/inventory

Writes inventory.json and inventory.md into the output directory (kept out of git; the ADR
quotes the summary).
"""

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

# First letter of the TEC route code (route_id "gr:tec:L0064-24183" -> "L").
REGIONS = {
    "B": "Brabant wallon",
    "C": "Charleroi",
    "H": "Hainaut",
    "L": "Liège-Verviers",
    "N": "Namur",
    "X": "Luxembourg",
}


def route_code(route_id: str) -> str:
    """'gr:tec:L0064-24183' -> 'L0064' (the part before the version suffix)."""
    tail = route_id.rsplit(":", 1)[-1]
    return tail.split("-", 1)[0]


def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        yield from csv.DictReader(f)


def main(gtfs_dir: Path, out_dir: Path) -> None:
    routes = list(read_csv(gtfs_dir / "routes.txt"))

    trips = Counter()
    for t in read_csv(gtfs_dir / "trips.txt"):
        trips[t["route_id"]] += 1

    by_number = defaultdict(list)
    for r in routes:
        code = route_code(r["route_id"])
        by_number[r["route_short_name"].strip()].append(
            {
                "route_id": r["route_id"],
                "code": code,
                "region": REGIONS.get(code[:1], "?"),
                "long_name": r["route_long_name"].strip(),
                "trips": trips.get(r["route_id"], 0),
            }
        )

    shared = {
        num: sorted(items, key=lambda i: (i["region"], i["code"], i["route_id"]))
        for num, items in by_number.items()
        if len(items) > 1
    }

    # Same number used twice in the same region: the risky case for a Liège-only pilot.
    same_region = {}
    for num, items in shared.items():
        regions = Counter(i["region"] for i in items)
        dup = {reg: n for reg, n in regions.items() if n > 1}
        if dup:
            same_region[num] = dup

    # One line code split across several route_ids (e.g. two versions in the same feed).
    codes = Counter(route_code(r["route_id"]) for r in routes)
    split_codes = {c: n for c, n in codes.items() if n > 1}

    def sort_key(num: str):
        return (0, int(num), "") if num.isdigit() else (1, 0, num)

    summary = {
        "routes": len(routes),
        "distinct_numbers": len(by_number),
        "shared_numbers": len(shared),
        "routes_in_shared_numbers": sum(len(v) for v in shared.values()),
        "max_routes_per_number": max((len(v) for v in shared.values()), default=0),
        "same_number_same_region": len(same_region),
        "codes_with_several_route_ids": len(split_codes),
        "routes_without_trips": sum(1 for r in routes if trips.get(r["route_id"], 0) == 0),
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "inventory.json").write_text(
        json.dumps(
            {
                "summary": summary,
                "shared": {k: shared[k] for k in sorted(shared, key=sort_key)},
                "same_region": same_region,
                "split_codes": split_codes,
            },
            ensure_ascii=False,
            indent=1,
        ),
        encoding="utf-8",
    )

    lines = ["| Numéro | route_id | Région | Trajet | Courses |", "|---|---|---|---|---|"]
    for num in sorted(shared, key=sort_key):
        for i in shared[num]:
            lines.append(
                f"| {num} | `{i['route_id']}` | {i['region']} | {i['long_name']} | {i['trips']} |"
            )
    (out_dir / "inventory.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=1))
    print("same number, same region:", json.dumps(same_region, ensure_ascii=False))
    print("codes with several route_ids:", json.dumps(split_codes))
    for num in ("10", "64", "65"):
        print(f"--- {num}")
        for i in shared.get(num, by_number.get(num, [])):
            print(f"  {i['route_id']:24} {i['region']:15} {i['trips']:5}  {i['long_name']}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: inventory.py <gtfs_dir> <out_dir>")
    main(Path(sys.argv[1]), Path(sys.argv[2]))
