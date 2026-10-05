#!/bin/sh
# Rebuild the whole draft site: pages from the live repo, then the unique location pages.
cd "$(dirname "$0")/.." && python3 tools/build_draft.py && python3 tools/build_locations.py && python3 tools/build_conversion.py
