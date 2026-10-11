#!/usr/bin/env python3
"""Deterministic synthetic coefficient generator (identity / no-op).

Produces the native 540-coefficient format (540 x little-endian signed int32,
signed-12 range) used by the Image Control slot framework, populated with the
identity transform (Q10 scale; a technical identity fixture, not a firmware patch).

The output is a TECHNICAL TEST FIXTURE ONLY. It does not emulate any film
stock, and it is generated deterministically by this repository's own code —
no binary blob is checked in.

Usage:
  python3 gen_synthetic_coefficients.py <outdir>
"""
import hashlib, json, struct, sys
from _fixture_output import fresh_output, write_fixture
from pathlib import Path

def identity_540() -> bytes:
    q = 1024  # Q10 identity scale (fits signed-12 range)
    matrix = (q, 0, 0, 0, q, 0, 0, 0, q)
    values = []
    for _bank in range(10):       # 10 luminance banks
        for _sector in range(6):  # 6 chroma sectors
            values.extend(matrix)
    assert len(values) == 540
    return struct.pack('<540i', *values)

def identity_q13_3x3() -> list:
    q = 8192  # Q13 scale, signed-16 range — native basis matrix convention
    return [q, 0, 0, 0, q, 0, 0, 0, q]

def main():
    if len(sys.argv) != 2:
        raise SystemExit('usage: gen_synthetic_coefficients.py FRESH_TEMP_OUTPUT_DIR')
    blob = identity_540()
    outdir = fresh_output(sys.argv[1])
    blob = identity_540()
    write_fixture(outdir, 'primary-identity-540.bin', blob)
    report = {
        'generator': 'gen_synthetic_coefficients.py (deterministic, repository-authored)',
        'fixture_notice': 'TECHNICAL TEST FIXTURE ONLY — does not emulate any real film stock or commercial preset',
        'primary_540': {
            'path': 'primary-identity-540.bin',
            'bytes': len(blob),
            'count': 540, 'encoding': 'little-endian signed int32', 'scale': 'Q10 identity (1024)',
            'sha256': hashlib.sha256(blob).hexdigest(),
        },
        'native_q13_identity_3x3': identity_q13_3x3(),
    }
    write_fixture(outdir, 'coefficients-report.json', (json.dumps(report, indent=2)+'\n').encode())
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
