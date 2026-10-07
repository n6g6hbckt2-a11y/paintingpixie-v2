#!/bin/sh
# Build the "switch" version: new design, menus, footer and background on every page, but each existing page keeps its
# live wording, title, description and address. New pages (Prices, Reviews, Services, Workshop parties, Corporate, Christmas)
# are added. Rewritten town pages and town<->service links are NOT included (they follow in batches).
cd "$(dirname "$0")/.." && rm -rf switch && mkdir switch && export PP_OUT="$PWD/switch" PP_MODE=switch && \
python3 tools/build_draft.py && python3 tools/build_extra.py && python3 tools/build_gallery.py && python3 tools/build_conversion.py && \
python3 tools/build_areas.py && python3 tools/build_photos.py && python3 tools/build_breadcrumbs.py && python3 tools/build_season.py && \
python3 tools/build_theme.py && python3 tools/build_halloween_draft.py
