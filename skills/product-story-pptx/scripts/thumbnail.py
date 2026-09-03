#!/usr/bin/env python3
"""Compatibility alias for render_preview.py.

Usage:
    python scripts/thumbnail.py deck.pptx [--outdir ...]
"""
from render_preview import main

if __name__ == "__main__":
    raise SystemExit(main())
