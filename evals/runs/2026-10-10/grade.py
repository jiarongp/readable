#!/usr/bin/env python3
"""Fill grades into results.md. Usage: python3 grade.py <eval_id> 'GRADE|note' 'GRADE|note' ... (one per assertion, in order)."""
import sys, re, pathlib
p = pathlib.Path(__file__).with_name("results.md"); s = p.read_text()
eid = int(sys.argv[1]); grades = [g.split("|", 1) for g in sys.argv[2:]]
start = s.index(f"## Eval {eid}\n"); end = s.find("\n## Eval ", start + 1); end = len(s) if end == -1 else end
block = s[start:end]; lines = block.split("\n"); k = 0
for i, ln in enumerate(lines):
    if ln.startswith("| ") and not ln.startswith("| assertion") and not ln.startswith("|---"):
        if k < len(grades):
            g, n = (grades[k] + [""])[:2]
            cells = ln.split(" | "); cells = [cells[0], g.strip(), n.strip() + " |"]
            lines[i] = " | ".join(cells); k += 1
assert k == len(grades), f"eval {eid}: filled {k} rows, got {len(grades)} grades"
s = s[:start] + "\n".join(lines) + s[end:]; p.write_text(s); print(f"eval {eid}: {k} graded")
