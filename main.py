#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261120 (nurz).

Copies the pre-drawn front page (entry.png, in this repository) to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output), validating the gate
limits first: PNG, at most 1024x1024 px, at most 1 MiB. Standard
library only; deterministic -- both runs write identical bytes.
"""

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

MAX_BYTES = 1_048_576
MAX_DIM = 1024

SRC = Path(__file__).resolve().parent / "entry.png"


def validate_png(path: Path) -> None:
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png too large: {len(data)} bytes")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        raise SystemExit(f"entry.png too big: {width}x{height}")
    if width < 1 or height < 1:
        raise SystemExit("entry.png has invalid dimensions")
    print(f"entry.png OK: {width}x{height}, {len(data)} bytes")


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    validate_png(SRC)
    dest = out_dir / "entry.png"
    shutil.copyfile(SRC, dest)
    # Confirm the copy is byte-identical to the source before finishing.
    if hashlib.sha256(SRC.read_bytes()).hexdigest() != hashlib.sha256(
        dest.read_bytes()
    ).hexdigest():
        raise SystemExit("copy mismatch: output differs from entry.png")
    print(f"wrote {dest}")


if __name__ == "__main__":
    main()
