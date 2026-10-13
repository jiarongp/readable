"""Build docs/readable/sparse_cts.html from the scratchpad template.

- {{m|TEX}} / {{d|TEX}}  -> KaTeX MathML (inline / display), LaTeX retained in the
  MathML annotation and in a data-tex attribute.
- {{img:NAME.png|ALT}}   -> <img> with a base64 data URI, pixel width/height.
- {{READ_MIN}}           -> reading time at 250 words/min.
Then mechanical checks: unique ids, resolving anchors, no external loaded
resources, size, tag balance.
"""
import base64, html, re, subprocess, sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from PIL import Image

SCRATCH = Path(__file__).parent
REPO = Path("/gpfs/home5/jpan/hdbo")
TPL = SCRATCH / "sparse_cts.tpl.html"
OUT = REPO / "docs/readable/sparse_cts.html"
FIGDIR = REPO / "studies/figures/sparse_cts"
KATEX = SCRATCH / "katex/node_modules/.bin/katex"

src = TPL.read_text()


KATEX_DIST = SCRATCH / "katex/node_modules/katex/dist"


def katex_css_embedded() -> str:
    """katex.min.css with every @font-face pointing at an embedded woff2 data URI."""
    css = (KATEX_DIST / "katex.min.css").read_text()
    pat = re.compile(r'src:url\(fonts/([A-Za-z0-9_-]+)\.woff2\) format\("woff2"\),'
                     r'url\(fonts/[A-Za-z0-9_-]+\.woff\) format\("woff"\),'
                     r'url\(fonts/[A-Za-z0-9_-]+\.ttf\) format\("truetype"\)')
    def sub(m):
        b64 = base64.b64encode((KATEX_DIST / "fonts" / f"{m.group(1)}.woff2").read_bytes()).decode()
        return f'src:url(data:font/woff2;base64,{b64}) format("woff2")'
    css, n = pat.subn(sub, css)
    assert n == 20 and "url(fonts/" not in css, f"font-face rewrite incomplete ({n})"
    return css


def katex(tex: str, display: bool) -> str:
    args = [str(KATEX), "-F", "htmlAndMathml"] + (["-d"] if display else [])
    r = subprocess.run(args, input=tex, capture_output=True, text=True, check=True)
    out = r.stdout.strip()
    attr = html.escape(tex, quote=True)
    if display:
        return f'<div class="math-display" data-tex="{attr}">{out}</div>'
    return f'<span class="m" data-tex="{attr}">{out}</span>'


def replace_math(s: str) -> str:
    out, i, n = [], 0, len(s)
    cache = {}
    while i < n:
        j = s.find("{{", i)
        if j < 0 or s[j + 2 : j + 4] not in ("m|", "d|"):
            if j < 0:
                out.append(s[i:]); break
            out.append(s[i : j + 2]); i = j + 2; continue
        out.append(s[i:j])
        kind = s[j + 2]
        p, depth = j + 4, 0
        while p < n:
            ch = s[p]
            if ch == "{":
                depth += 1
            elif ch == "}":
                if depth > 0:
                    depth -= 1
                elif s[p + 1 : p + 2] == "}":
                    break
            p += 1
        tex = s[j + 4 : p].strip()
        key = (kind, tex)
        if key not in cache:
            cache[key] = katex(tex, kind == "d")
        out.append(cache[key])
        i = p + 2
    return "".join(out)


def replace_images(s: str) -> str:
    def sub(m):
        name, alt = m.group(1), m.group(2)
        p = FIGDIR / name
        im = Image.open(p)
        w, h = im.size
        b64 = base64.b64encode(p.read_bytes()).decode()
        return (f'<img src="data:image/png;base64,{b64}" alt="{html.escape(alt, quote=True)}" '
                f'width="{w}" height="{h}">')
    return re.sub(r"\{\{img:([^|}]+)\|([^}]*)\}\}", sub, s)


# reading time from the main reading path: visible text minus styles, the table of
# contents, collapsed "More detail" boxes and References; each equation counts as one word.
t = re.sub(r"<style>.*?</style>", " ", src, flags=re.S)
t = re.sub(r"<details.*?</details>", " ", t, flags=re.S)
t = re.sub(r"<nav.*?</nav>", " ", t, flags=re.S)
t = t.split('id="references"')[0]
t = re.sub(r"\{\{d\|.*?\}\}\n", " EQ ", t, flags=re.S)
t = re.sub(r"\{\{m\|[^{}]*(\{[^{}]*\}[^{}]*)*\}\}", "X", t)
t = re.sub(r"\{\{img:[^}]*\}\}", " ", t)
t = re.sub(r"<[^>]+>", " ", t)
words = len(t.split())
read_min = max(1, round(words / 250))

page = replace_math(src)
page = replace_images(page)
page = page.replace("{{READ_MIN}}", str(read_min))
page = page.replace("{{KATEX_CSS}}", katex_css_embedded())
assert "{{" not in page, "unreplaced placeholder: " + page[page.find("{{") : page.find("{{") + 60]
OUT.write_text(page)

# ---- checks -------------------------------------------------------------
ids = re.findall(r'\sid="([^"]+)"', page)
dups = [k for k, v in Counter(ids).items() if v > 1]
anchors = re.findall(r'href="#([^"]+)"', page)
missing = sorted({a for a in anchors if a not in ids})
ext_loads = re.findall(r'<(?:script|link|img|iframe|video|audio|source)[^>]*(?:src|href)="(https?:[^"]+)"', page)
css_urls = [u for u in re.findall(r"url\(([^)]{0,12})", page) if not u.startswith("data:")]
imports = re.findall(r"@import", page)
annotations = page.count("<annotation ")
datatex = page.count("data-tex=")


class Balance(HTMLParser):
    VOID = {"meta", "img", "br", "hr", "input", "link", "source"}
    def __init__(self):
        super().__init__(); self.stack = []; self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID: self.stack.append(tag)
    def handle_endtag(self, tag):
        if tag in self.VOID: return
        if self.stack and self.stack[-1] == tag: self.stack.pop()
        else: self.errors.append((tag, self.getpos(), self.stack[-3:]))


b = Balance(); b.feed(page)
print(f"words ~{words}, read {read_min} min")
print(f"size {OUT.stat().st_size/1e6:.2f} MB; ids {len(ids)}, dup ids {dups}; missing anchors {missing}")
print(f"external loads {ext_loads}; css url() {len(css_urls)}; @import {len(imports)}")
print(f"math annotations {annotations}, data-tex {datatex}")
print(f"tag balance errors {b.errors[:5]}; unclosed at end {b.stack}")
ok = not dups and not missing and not ext_loads and not css_urls and not imports and not b.errors and not b.stack
print("CHECKS", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
