#!/usr/bin/env python3
"""Validate every SKILL.md: well-formed frontmatter, kebab-case name == directory,
a usable description. Keeps the bundle installable and discoverable.

Run from the repo root:  python scripts/validate.py
Requires: pyyaml.
"""
from __future__ import annotations

import glob
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("validate.py needs pyyaml:  pip install pyyaml")

FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.S)
KEBAB = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")

skills = sorted(glob.glob("*/SKILL.md"))
if not skills:
    sys.exit("no */SKILL.md found — run from the repo root")

fails = 0
for path in skills:
    directory = os.path.dirname(path)
    problems: list[str] = []
    m = FRONTMATTER.match(open(path, encoding="utf-8").read())
    if not m:
        problems.append("missing YAML frontmatter (--- name/description ---)")
    else:
        fm = yaml.safe_load(m.group(1)) or {}
        name = str(fm.get("name", ""))
        desc = fm.get("description", "")
        if not KEBAB.fullmatch(name):
            problems.append(f"name {name!r} must be kebab-case")
        if name != directory:
            problems.append(f"name {name!r} must equal its directory {directory!r}")
        if not isinstance(desc, str) or len(desc) < 40:
            problems.append("description missing or too short (<40 chars)")
    if problems:
        fails += 1
        print(f"FAIL {path}: " + "; ".join(problems))
    else:
        print(f"ok   {path}")

print()
print("all skills valid" if not fails else f"{fails} skill(s) have problems")
sys.exit(1 if fails else 0)
