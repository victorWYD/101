#!/usr/bin/env python3
"""Encode a 512x512 RGBA PNG into a WYD WS10 .wys (BC3/DXT5 + mips)."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image
from quicktex import RawTexture
from quicktex.s3tc.bc3 import BC3Encoder

EXPECTED_MIPS = 349552
HEADER_SIZE = 128


def encode_bc3_mipchain(img: Image.Image) -> bytes:
    enc = BC3Encoder(18)
    chunks: list[bytes] = []
    cur = img.convert("RGBA")
    while True:
        w, h = cur.size
        arr = np.ascontiguousarray(np.array(cur))
        chunks.append(enc.encode(RawTexture.frombytes(arr.tobytes(), w, h)).tobytes())
        if w == 1 and h == 1:
            break
        cur = cur.resize((max(1, w // 2), max(1, h // 2)), Image.Resampling.LANCZOS)
    data = b"".join(chunks)
    if len(data) < EXPECTED_MIPS:
        data += b"\x00" * (EXPECTED_MIPS - len(data))
    return data[:EXPECTED_MIPS]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", type=Path, required=True)
    ap.add_argument("--template-wys", type=Path, required=True, help="Original .wys for header/trailer")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    template = args.template_wys.read_bytes()
    header = template[:HEADER_SIZE]
    trailer = template[HEADER_SIZE + EXPECTED_MIPS :]
    img = Image.open(args.png).convert("RGBA").resize((512, 512), Image.Resampling.LANCZOS)
    mips = encode_bc3_mipchain(img)
    args.out.write_bytes(header + mips + trailer)
    print(f"wrote {args.out} ({args.out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
