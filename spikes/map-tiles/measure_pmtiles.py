"""Measure the size of a PMTiles extract for a bbox, without downloading the archive.

Reads the PMTiles v3 header and directories with HTTP range requests, looks up every
tile of the bbox per zoom level and sums the tile lengths (unique offsets only, as an
extract would deduplicate them).

Usage: python -I measure_pmtiles.py <pmtiles-url> <min_lon> <min_lat> <max_lon> <max_lat> <max_zoom> <out.json>
"""
import zlib
import json
import math
import struct
import sys
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = "copibus-phase0-spike/0.1"


MAX_FETCH = 16 * 1024 * 1024
MAX_DIR = 64 * 1024 * 1024


def fetch(url: str, offset: int, length: int) -> bytes:
    if urllib.parse.urlsplit(url).scheme != "https":
        raise RuntimeError("only https URLs are accepted")
    if offset < 0 or length <= 0 or length > MAX_FETCH:
        raise RuntimeError(f"refusing range offset={offset} length={length}")
    req = urllib.request.Request(url, headers={
        "Range": f"bytes={offset}-{offset + length - 1}",
        "User-Agent": USER_AGENT,
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        if resp.status != 206:
            raise RuntimeError(f"server ignored Range (HTTP {resp.status})")
        data = resp.read(length + 1)
    if len(data) != length:
        raise RuntimeError(f"short read: wanted {length}, got {len(data)}")
    return data


def read_varint(buf: bytes, pos: int) -> tuple[int, int]:
    result, shift = 0, 0
    while True:
        if pos >= len(buf):
            raise RuntimeError("truncated varint")
        if shift > 63:
            raise RuntimeError("varint longer than 64 bits")
        b = buf[pos]
        pos += 1
        result |= (b & 0x7F) << shift
        if b < 0x80:
            return result, pos
        shift += 7


def parse_directory(raw: bytes) -> list[tuple[int, int, int, int]]:
    """Return entries as (tile_id, offset, length, run_length)."""
    pos = 0
    n, pos = read_varint(raw, pos)
    if n > len(raw):  # every entry needs at least one byte per field
        raise RuntimeError(f"directory claims {n} entries for {len(raw)} bytes")
    ids, runs, lens, offs = [], [], [], []
    last = 0
    for _ in range(n):
        v, pos = read_varint(raw, pos)
        last += v
        ids.append(last)
    for _ in range(n):
        v, pos = read_varint(raw, pos)
        runs.append(v)
    for _ in range(n):
        v, pos = read_varint(raw, pos)
        lens.append(v)
    for i in range(n):
        v, pos = read_varint(raw, pos)
        if v == 0 and i > 0:
            offs.append(offs[i - 1] + lens[i - 1])
        elif v == 0:
            raise RuntimeError("invalid directory: first offset is zero")
        else:
            offs.append(v - 1)
    return list(zip(ids, offs, lens, runs))


def zxy_to_tile_id(z: int, x: int, y: int) -> int:
    acc = ((1 << (2 * z)) - 1) // 3
    n = 1 << z
    d = 0
    s = n >> 1
    while s > 0:
        rx = 1 if x & s else 0
        ry = 1 if y & s else 0
        d += s * s * ((3 * rx) ^ ry)
        if ry == 0:
            if rx == 1:
                x = n - 1 - x
                y = n - 1 - y
            x, y = y, x
        s >>= 1
    return acc + d


def lonlat_to_tile(lon: float, lat: float, z: int) -> tuple[int, int]:
    n = 1 << z
    x = int((lon + 180.0) / 360.0 * n)
    lat_r = math.radians(lat)
    y = int((1.0 - math.asinh(math.tan(lat_r)) / math.pi) / 2.0 * n)
    return min(max(x, 0), n - 1), min(max(y, 0), n - 1)


class Archive:
    def __init__(self, url: str):
        self.url = url
        head = fetch(url, 0, 16384)
        if head[:7] != b"PMTiles" or head[7] != 3:
            raise RuntimeError("not a PMTiles v3 archive")
        (self.root_off, self.root_len, _meta_off, _meta_len, self.leaf_off, _leaf_len,
         self.data_off, _data_len, self.addressed, _entries, _contents) = struct.unpack_from("<11Q", head, 8)
        self.internal_compression = head[97]
        self.tile_compression = head[98]
        self.min_zoom, self.max_zoom = head[100], head[101]
        self.leaf_fetches = 0
        self._cache: dict[tuple[int, int], list] = {}
        if self.root_off + self.root_len > len(head):
            raise RuntimeError("root directory lies outside the header read")
        self.root = self._dir(head[self.root_off:self.root_off + self.root_len])

    def _dir(self, raw: bytes) -> list:
        if self.internal_compression == 2:
            d = zlib.decompressobj(16 + zlib.MAX_WBITS)
            raw = d.decompress(raw, MAX_DIR)
            if d.unconsumed_tail:
                raise RuntimeError("directory too large after decompression")
        elif self.internal_compression != 1:
            raise RuntimeError(f"unsupported internal compression {self.internal_compression}")
        return parse_directory(raw)

    def _leaf(self, off: int, length: int) -> list:
        key = (off, length)
        if key not in self._cache:
            self.leaf_fetches += 1
            self._cache[key] = self._dir(fetch(self.url, self.leaf_off + off, length))
        return self._cache[key]

    def find(self, tile_id: int) -> tuple[int, int] | None:
        entries = self.root
        for _depth in range(4):
            lo, hi = 0, len(entries) - 1
            best = -1
            while lo <= hi:
                mid = (lo + hi) // 2
                if entries[mid][0] <= tile_id:
                    best = mid
                    lo = mid + 1
                else:
                    hi = mid - 1
            if best < 0:
                return None
            tid, off, length, run = entries[best]
            if run == 0:
                entries = self._leaf(off, length)
                continue
            if tile_id < tid + run:
                return off, length
            return None
        raise RuntimeError("directory too deep")


def main() -> None:
    url = sys.argv[1]
    min_lon, min_lat, max_lon, max_lat = map(float, sys.argv[2:6])
    max_zoom = int(sys.argv[6])
    out = Path(sys.argv[7])

    # Self-check of the Hilbert numbering against the PMTiles spec examples.
    if [zxy_to_tile_id(1, 0, 0), zxy_to_tile_id(1, 0, 1), zxy_to_tile_id(1, 1, 1),
            zxy_to_tile_id(1, 1, 0), zxy_to_tile_id(2, 0, 0)] != [1, 2, 3, 4, 5]:
        raise RuntimeError("Hilbert tile numbering self-check failed")

    arc = Archive(url)
    per_zoom = []
    seen: set[int] = set()
    cumulative = 0
    for z in range(arc.min_zoom, min(max_zoom, arc.max_zoom) + 1):
        x0, y0 = lonlat_to_tile(min_lon, max_lat, z)
        x1, y1 = lonlat_to_tile(max_lon, min_lat, z)
        tiles = found = zbytes = 0
        biggest = 0
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                tiles += 1
                hit = arc.find(zxy_to_tile_id(z, x, y))
                if hit is None:
                    continue
                found += 1
                off, length = hit
                biggest = max(biggest, length)
                if off not in seen:
                    seen.add(off)
                    zbytes += length
        cumulative += zbytes
        per_zoom.append({"z": z, "tiles": tiles, "found": found, "bytes": zbytes,
                         "largest_tile": biggest, "cumulative_bytes": cumulative})
        print(f"z{z:2d} tiles={tiles:5d} found={found:5d} bytes={zbytes:>11,} cumul={cumulative:>12,}")

    report = {
        "source": url,
        "bbox": [min_lon, min_lat, max_lon, max_lat],
        "archive_min_zoom": arc.min_zoom,
        "archive_max_zoom": arc.max_zoom,
        "tile_compression": arc.tile_compression,
        "leaf_directory_fetches": arc.leaf_fetches,
        "per_zoom": per_zoom,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
