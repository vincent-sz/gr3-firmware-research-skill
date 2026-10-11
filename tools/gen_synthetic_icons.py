#!/usr/bin/env python3
"""Deterministic synthetic icon generator (generic 40x40 RGBA package labels).

Draws six simple gray "DEMO n" tiles using only geometric shapes and a plain
bitmap font. No commercial logos, no film-box designs, no trademark shapes.

The output is a TECHNICAL TEST FIXTURE ONLY.

Usage:
  python3 gen_synthetic_icons.py <outdir>
"""
import hashlib, json, sys
from _fixture_output import fresh_output, write_fixture
from pathlib import Path

W = H = 40
# 3x5 pixel font for D E M O space 0-9
FONT = {
 'D':['110','101','101','101','110'], 'E':['111','100','110','100','111'],
 'M':['101','111','111','101','101'], 'O':['111','101','101','101','111'],
 ' ':['000','000','000','000','000'],
 '1':['010','110','010','010','111'], '2':['111','001','111','100','111'],
 '3':['111','001','111','001','111'], '4':['101','101','111','001','001'],
 '5':['111','100','111','001','111'], '6':['111','100','111','101','111'],
}

def draw_text(px, text, x0, y0, fg):
    xx = x0
    for ch in text:
        for j, row in enumerate(FONT[ch]):
            for k, v in enumerate(row):
                if v == '1':
                    x, y = xx + k, y0 + j
                    if 0 <= x < W and 0 <= y < H:
                        px[y][x] = fg
        xx += 4

def make_icon(n: int) -> bytes:
    if type(n) is not int or not 1 <= n <= 6:
        raise ValueError('synthetic icon ID must be 1..6')
    bg = (58, 58, 62, 255)
    fg = (235, 235, 235, 255)
    accent = (120, 120, 126, 255)
    px = [[bg for _ in range(W)] for _ in range(H)]
    # border
    for x in range(W):
        px[0][x] = accent; px[H-1][x] = accent
    for y in range(H):
        px[y][0] = accent; px[y][W-1] = accent
    # label rows
    draw_text(px, 'DEMO', 7, 10, fg)
    draw_text(px, str(n), 17, 20, fg)
    return bytes(v for row in px for p in row for v in p)

def main():
    if len(sys.argv) != 2:
        raise SystemExit('usage: gen_synthetic_icons.py FRESH_TEMP_OUTPUT_DIR')
    outdir = fresh_output(sys.argv[1])
    entries = []
    for n in range(1, 7):
        raw = make_icon(n)
        assert len(raw) == W*H*4
        write_fixture(outdir, f'demo-{n}.rgba', raw)
        entries.append(dict(id=f'demo-{n}', size=[W, H], path=f'demo-{n}.rgba',
                            sha256=hashlib.sha256(raw).hexdigest()))
    entries_note = 'Raw synthetic fixtures only; no renderer or third-party dependency.'
    report = dict(
        generator='gen_synthetic_icons.py (deterministic, repository-authored)',
        fixture_notice='TECHNICAL TEST FIXTURE ONLY — generic shapes/text; no logos or film-box designs',
        icons=entries, note=entries_note)
    write_fixture(outdir, 'icons-report.json', (json.dumps(report, indent=2)+'\n').encode())
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
