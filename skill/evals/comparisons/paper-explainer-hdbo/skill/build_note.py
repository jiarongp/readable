"""Build the self-contained note from its template.

Run from this directory, after make_figures.py:
    python3 build_note.py

Steps:
  1. Replace every $$...$$ (display) and $...$ (inline) in note_template.html
     with MathML produced by the KaTeX command-line tool (katex -F mathml).
     The original LaTeX is retained inside each <annotation encoding=
     "application/x-tex"> element that KaTeX emits.
  2. Replace every {{fig:name.png}} with a base64 data URI of that file.
  3. Replace {{readtime}} with an estimate at 250 words per minute.
  4. Write hdbo-linear-note.html.
"""

import base64
import html
import pathlib
import re
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE / "note_template.html"
OUTPUT = HERE / "hdbo-linear-note.html"

src = TEMPLATE.read_text(encoding="utf-8")

# Reading time from the template's visible words (tags stripped, TeX kept as words).
text = re.sub(r"<style>.*?</style>", " ", src, flags=re.S)
text = re.sub(r'<nav class="toc">.*?</nav>', " ", text, flags=re.S)
text = re.sub(r'alt="[^"]*"', " ", text)
text = re.sub(r"<[^>]+>", " ", text)
words = len(html.unescape(text).split())
readtime = max(1, round(words / 250))


def katex(tex: str, display: bool) -> str:
    args = ["katex", "-F", "mathml"] + (["-d"] if display else [])
    proc = subprocess.run(args, input=tex, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"KaTeX failed on: {tex}\n{proc.stderr}")
    return proc.stdout.strip()


def rep_display(m: re.Match) -> str:
    return f'<div class="math-display">{katex(m.group(1).strip(), True)}</div>'


def rep_inline(m: re.Match) -> str:
    return katex(m.group(1).strip(), False)


src = re.sub(r"\$\$(.+?)\$\$", rep_display, src, flags=re.S)
src = re.sub(r"\$(.+?)\$", rep_inline, src, flags=re.S)


def rep_fig(m: re.Match) -> str:
    data = (HERE / m.group(1)).read_bytes()
    return "data:image/png;base64," + base64.b64encode(data).decode("ascii")


src = re.sub(r"\{\{fig:([^}]+)\}\}", rep_fig, src)
src = src.replace("{{readtime}}", str(readtime))

OUTPUT.write_text(src, encoding="utf-8")
print(f"wrote {OUTPUT.name}: {words} words, ~{readtime} min, {OUTPUT.stat().st_size / 1024:.0f} KB")
