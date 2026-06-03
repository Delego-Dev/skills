#!/usr/bin/env bash
# Symlink each delego skill into .claude/skills/ so Claude Code discovers it.
# Claude Code finds skills only one level deep (.claude/skills/<name>/SKILL.md),
# so a nested clone isn't found — this links each skill into place.
#
# Usage (from a repo cloned at .claude/delego-skills):
#   .claude/delego-skills/install.sh            # -> links into .claude/skills/
#   .claude/delego-skills/install.sh <dir>      # -> links into <dir>
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${1:-$(cd "$HERE/.." && pwd)/skills}"   # default: sibling .claude/skills
mkdir -p "$DEST"
n=0
for skill in "$HERE"/*/SKILL.md; do
  [ -e "$skill" ] || continue
  d="$(dirname "$skill")"; name="$(basename "$d")"
  ln -sfn "$d" "$DEST/$name"
  echo "  linked skill  $name -> $DEST/$name"
  n=$((n + 1))
done
echo "Linked $n skill(s). Skills hot-load — invoke with /delego-init, /delego-policy-drafter, etc."
