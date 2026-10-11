#!/usr/bin/env python3
"""Read-only bounded release scan; no firmware safety verdict."""
from release_scan import main

if __name__ == "__main__":
    raise SystemExit(main('firmware'))
