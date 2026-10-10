#!/bin/sh
# Go-live (run only when Phil approves): rebuild the switch, package it, and put it on a branch of the live repo
# for a pull request. Nothing reaches paintingpixie.com until that pull request is merged.
set -e
cd "$(dirname "$0")/.."
LIVE=/home/claude/Painting-Pixie
sh tools/source.sh   # pre-switch wording source
(cd "$LIVE" && git checkout -q -f main && git clean -fdq && git pull -q)
sh tools/build_switch.sh
python3 tools/package_golive.py
cd "$LIVE" && git checkout -q main && git pull -q && git checkout -q -B new-design
cp -R /home/claude/paintingpixie-v2/golive/. "$LIVE"/
git add -A && git status --short | head -40 && echo "files changed: $(git status --short | wc -l)"
