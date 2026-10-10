#!/usr/bin/env python3
"""Assemble the self-contained HTML page from page_template.html.

Run from this directory with the system python3 (standard library only):
    python3 build.py

Steps:
  1. Replace every $$...$$ (display) and $...$ (inline) span in the template with
     MathML produced by the KaTeX command-line tool. KaTeX keeps the exact LaTeX in
     an <annotation encoding="application/x-tex"> inside each <math> element.
  2. Replace {{FIG:name|alt text}} markers with a pair of <img> elements (light and
     dark renderings of name_light.png / name_dark.png) embedded as data URIs.
  3. Fill {{READ_TIME}} from the word count of the body text at 250 words a minute.
  4. Write the page and run mechanical checks: full skeleton, unique ids, resolving
     in-document anchors, no external loaded resources, file size.
"""
import base64
import html
import re
import struct
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "page_template.html"
OUT = HERE / "sparse-cts-generator-6.1-6.3.html"


def katex(tex, display):
    args = ["katex", "-F", "mathml"] + (["-d"] if display else [])
    res = subprocess.run(args, input=tex, text=True, capture_output=True)
    if res.returncode != 0:
        sys.exit(f"katex failed on {tex!r}: {res.stderr}")
    out = res.stdout.strip()
    m = re.search(r"<math.*</math>", out, re.S)
    if not m:
        sys.exit(f"no <math> in katex output for {tex!r}")
    return m.group(0)


def render_math(text):
    n_display = n_inline = 0

    def disp(m):
        nonlocal n_display
        n_display += 1
        tex = m.group(1).strip()
        return f'<div class="math-display" data-tex="{html.escape(tex, quote=True)}">{katex(tex, True)}</div>'

    text = re.sub(r"\$\$(.+?)\$\$", disp, text, flags=re.S)

    def inl(m):
        nonlocal n_inline
        n_inline += 1
        tex = m.group(1).strip()
        return f'<span class="math-inline">{katex(tex, False)}</span>'

    # Inline math: $...$ on one line, not preceded by a backslash or digit.
    text = re.sub(r"(?<![\\\d])\$([^$\n]+?)\$", inl, text)
    return text, n_display, n_inline


def png_size(data):
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    w, h = struct.unpack(">II", data[16:24])
    return w, h


def embed_figures(text):
    def fig(m):
        name, alt = m.group(1), m.group(2)
        tags = []
        for theme in ("light", "dark"):
            path = HERE / f"{name}_{theme}.png"
            data = path.read_bytes()
            w, h = png_size(data)
            uri = "data:image/png;base64," + base64.b64encode(data).decode()
            tags.append(f'<img class="fig-{theme}" src="{uri}" alt="{html.escape(alt, quote=True)}" '
                        f'width="{w}" height="{h}">')
        return "\n".join(tags)

    return re.sub(r"\{\{FIG:([a-z0-9_]+)\|(.+?)\}\}", fig, text)


def word_count(body_html):
    text = re.sub(r"<[^>]+>", " ", body_html)
    text = html.unescape(text)
    return len(text.split())


def checks(page):
    problems = []
    for needed in ("<!doctype html>", "<html lang=", "<head>", "</head>", "<body>", "</body>", "</html>",
                   '<meta charset="utf-8">', "<title>"):
        if needed not in page:
            problems.append(f"missing {needed}")
    ids = re.findall(r'\sid="([^"]+)"', page)
    dups = {i for i in ids if ids.count(i) > 1}
    if dups:
        problems.append(f"duplicate ids: {sorted(dups)}")
    hrefs = re.findall(r'href="#([^"]+)"', page)
    missing = sorted({h for h in hrefs if h not in ids})
    if missing:
        problems.append(f"anchors without targets: {missing}")
    for attr in ("src", "href"):
        for url in re.findall(rf'{attr}="([^"]+)"', page):
            if attr == "src" and not url.startswith("data:"):
                problems.append(f"non-embedded src: {url[:80]}")
            if attr == "href" and url.startswith("http") and 'rel="stylesheet"' in page:
                problems.append("external stylesheet link present")
    if re.search(r"<script[^>]+src=", page):
        problems.append("external script")
    if re.search(r"url\(", page) or "@import" in page:
        problems.append("CSS url()/@import present")
    for tok in ("--bg", "--fg", "--accent"):
        if page.count(tok + ":") < 3:
            problems.append(f"token {tok} not defined in all three theme blocks")
    size = len(page.encode())
    if size > 16 * 1024 * 1024:
        problems.append(f"file too large: {size}")
    leftover = re.findall(r"\{\{[A-Z_]+[^}]*\}\}", page)
    if leftover:
        problems.append(f"unfilled placeholders: {leftover[:5]}")
    if "$" in re.sub(r"<[^>]+>", "", page).replace("&#36;", ""):
        problems.append("stray $ in rendered text (unconverted math?)")
    return problems, size


def main():
    text = TEMPLATE.read_text()
    text, nd, ni = render_math(text)
    text = embed_figures(text)
    body = re.search(r"<main>(.*)</main>", text, re.S).group(1)
    # Count only running text for reading time; strip MathML annotations.
    body_for_count = re.sub(r"<annotation.*?</annotation>", " ", body, flags=re.S)
    words = word_count(body_for_count)
    minutes = max(1, round(words / 250))
    text = text.replace("{{READ_TIME}}", f"{minutes} min read")
    OUT.write_text(text)
    problems, size = checks(text)
    print(f"wrote {OUT}  ({size/1024:.0f} KB, {words} words, {nd} display + {ni} inline equations)")
    if problems:
        print("CHECKS FAILED:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("mechanical checks passed")


if __name__ == "__main__":
    main()
