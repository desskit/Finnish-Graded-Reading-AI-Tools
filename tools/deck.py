#!/usr/bin/env python3
"""DEPRECATED — superseded by coverage.py on 2026-08-20.

This indexed `All Decks.txt`, which lists every Anki note whether or not it has
ever been studied. That counted never-scheduled words as known vocabulary and
made lesson 01 harder than designed.

Use the collection package instead:

    COLPKG=".../collection-YYYY-MM-DD@HH-MM-SS.colpkg" python3 coverage.py draft.txt

See manifest.md §2.1 and §3.
"""
import sys
print(__doc__, file=sys.stderr)
sys.exit(1)
