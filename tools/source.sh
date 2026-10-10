#!/bin/sh
# Since the switch (10 Oct 2026) the live site is in the new design, so the builds read each page's wording from
# the live repo as it was just before the switch (commit 7312a6f), checked out at /home/claude/pp-source.
# Wording changes now go into the build tools (or this source copy), then publish as usual.
set -e
LIVE=/home/claude/Painting-Pixie
[ -d /home/claude/pp-source ] || (cd "$LIVE" && git fetch -q && git worktree add -q --detach /home/claude/pp-source 7312a6fdb4d5175a36b09d75397e2dc69c0b427b)
