"""Entry program for make.fun's news-image-20261119 bounty (Python 3.13,
standard library only).

The repository holds the finished front page as entry.png — one page
summing up the world news of Thursday 19 November 2026, drawn in code by
make_image.py — and this program delivers it: it checks the file still
passes the bounty's gate (a whole PNG of at most 1 MiB and at most
1024x1024 pixels) and copies it to /output/entry.png. Outside the
grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import struct
import sys
import zlib
from pathlib import Path

MAX_BYTES = 1_048_576  # the gate's 1 MiB cap
MAX_SIDE = 1024  # the gate's 1024x1024 cap
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def check_png(data: bytes) -> tuple[int, int]:
    """Walk the PNG chunks, verifying each CRC, and return (width, height).

    Raises ValueError on anything that is not a whole, well-formed PNG.
    """
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("entry.png does not start with the PNG signature")
    pos = len(PNG_SIGNATURE)
    width = height = None
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            raise ValueError("truncated chunk header")
        (length,) = struct.unpack(">I", data[pos : pos + 4])
        kind = data[pos + 4 : pos + 8]
        body = data[pos + 8 : pos + 8 + length]
        if len(body) != length or pos + 12 + length > len(data):
            raise ValueError(f"truncated {kind!r} chunk")
        (stored_crc,) = struct.unpack(
            ">I", data[pos + 8 + length : pos + 12 + length]
        )
        if zlib.crc32(kind + body) & 0xFFFFFFFF != stored_crc:
            raise ValueError(f"bad CRC in {kind!r} chunk")
        if kind == b"IHDR":
            width, height = struct.unpack(">II", body[:8])
        if kind == b"IEND":
            seen_iend = True
            pos += 12 + length
            break
        pos += 12 + length
    if width is None or not seen_iend:
        raise ValueError("PNG is missing its IHDR or IEND chunk")
    return width, height


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    data = source.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError(
            f"entry.png is {len(data)} bytes, over the 1 MiB gate cap"
        )
    width, height = check_png(data)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(
            f"entry.png is {width}x{height}, over the 1024x1024 gate cap"
        )
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    print(f"wrote {target} ({len(data)} bytes, {width}x{height})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
