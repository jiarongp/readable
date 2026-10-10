#!/usr/bin/env python3
"""Mechanical checks for a readable HTML document.

Usage: python3 check_page.py page.html [source.md]

Reports: loaded network resources, skeleton, theme tokens, embedded images,
duplicate ids, unresolved in-document anchors, table of contents, References,
retained LaTeX (and whether it matches the source's display equations), and
prose density (paragraph and sentence medians, words per visual and heading).
Exit code 1 if any hard check fails.
"""
import html, re, statistics as st, sys, pathlib

page = pathlib.Path(sys.argv[1]).read_text()
src = pathlib.Path(sys.argv[2]).read_text() if len(sys.argv) > 2 else None
fail = []

def hard(cond, msg):
    (print("PASS", msg) if cond else (print("FAIL", msg), fail.append(msg)))

# 1. loaded resources (not navigation links)
loads = []
loads += re.findall(r'<script[^>]+src="([^"]+)"', page)
loads += re.findall(r'<link[^>]+href="([^"]+)"', page)
loads += re.findall(r'<(?:img|source|video|audio|iframe|embed|object|track)[^>]+(?:src|srcset|data)="([^"]+)"', page)
loads += re.findall(r'url\(["\']?([^)"\']+)', page)
loads += re.findall(r'@import\s+["\']?([^"\';)]+)', page)
loads += re.findall(r'<image[^>]+(?:href|xlink:href)="([^"]+)"', page)
loads += re.findall(r'\bfetch\(\s*["\']([^"\']+)', page)
network = [u for u in loads if re.match(r'(https?:)?//', u)]
hard(not network, f"no loaded network resources ({len(network)} found: {network[:3]})")

# 2. skeleton, title, themes
hard(re.search(r'<!doctype html>', page, re.I) and '<head' in page and '<body' in page, "full html skeleton")
hard(re.search(r'<title>[^<]+</title>', page), "title present")
hard(':root' in page, "tokens on bare :root")
hard(re.search(r'prefers-color-scheme:\s*dark', page) and '[data-theme="dark"]' in page, "both dark theme blocks")
hard(re.search(r'body\s*{[^}]*background', page), "body background from token")

# 3. images embedded
imgs = re.findall(r'<img[^>]+src="([^"]+)"', page)
hard(all(u.startswith('data:') for u in imgs), f"all {len(imgs)} <img> are data URIs")
svgs = len(re.findall(r'<svg', page)); mathml = len(re.findall(r'<math', page))

# 4. ids and anchors
ids = re.findall(r'\sid="([^"]+)"', page)
dups = {i for i in ids if ids.count(i) > 1}
hard(not dups, f"ids unique ({sorted(dups)[:5]})")
anchors = [a[1:] for a in re.findall(r'href="(#[^"]+)"', page)]
missing = sorted({a for a in anchors if a not in ids})
hard(not missing, f"all {len(anchors)} in-document anchors resolve (missing: {missing[:5]})")
headings = re.findall(r'<h([23])[^>]*\sid="([^"]+)"', page)
toc = re.search(r'<nav[^>]*class="[^"]*toc[^"]*"[^>]*>(.*?)</nav>', page, re.S)
if toc:
    toc_targets = set(re.findall(r'href="#([^"]+)"', toc.group(1)))
    not_in_toc = [h for _, h in headings if h not in toc_targets and h.lower() != 'references' or False]
    hard(not [h for _, h in headings if h not in toc_targets], f"toc covers every h2/h3 ({[h for _,h in headings if h not in toc_targets][:4]})")
else:
    hard(False, "table of contents <nav class=toc> present")
cites = re.findall(r'<a href="https?://[^"]+"[^>]*>[^<]*\d{4}[^<]*</a>', page)
refs = re.search(r'<h2[^>]*>\s*References', page)
hard(refs or not cites, f"References section present when citations exist ({len(cites)} author-year links)")

# 5. equations
tex = re.findall(r'<annotation encoding="application/x-tex">(.*?)</annotation>', page, re.S)
tex += re.findall(r'data-tex="([^"]*)"', page)
tex = [html.unescape(t) for t in tex]
print(f"INFO  math: {mathml} <math>, {svgs} <svg>, {len(tex)} retained LaTeX strings")
if src is not None:
    eqs = re.findall(r'\$\$\s*(.*?)\s*\$\$', src, re.S)
    norm = lambda s: ' '.join(s.split())
    texn = [norm(t) for t in tex]
    for e in eqs:
        hard(norm(e) in texn or norm(e) in norm(page), f"source equation retained: {norm(e)[:60]}")
    codes = re.findall(r'```\w*\n(.*?)```', src, re.S)
    pagecode = html.unescape(re.sub(r'<[^>]+>', '', ' '.join(re.findall(r'<pre[^>]*>(.*?)</pre>', page, re.S))))
    for c in codes:
        hard(c.strip() in pagecode, f"source code block retained: {c.strip()[:40]!r}")

# 6. density
body = re.sub(r'<(script|style|nav|figure|table|pre|ol class="references")[^>]*>.*?</\1>', '', page, flags=re.S)
ps = [html.unescape(re.sub(r'<[^>]+>', ' ', p)).strip() for p in re.findall(r'<p[^>]*>(.*?)</p>', body, re.S)]
ps = [p for p in ps if p]
L = sorted(len(p.split()) for p in ps) or [0]
sents = [x for p in ps for x in re.split(r'(?<=[.!?])\s+(?=[A-Z\\(])', p) if x.strip()]
SL = [len(x.split()) for x in sents] or [0]
words = sum(L); figs = len(re.findall(r'<figure', page)); nh = len(headings)
print(f"INFO  density: {words} words in {len(L)} paragraphs; median para {st.median(L)}, p90 {L[int(.9*(len(L)-1))]}, max {max(L)}, >80: {sum(x>80 for x in L)}")
print(f"INFO  sentences: {len(SL)}, median {st.median(SL)}, mean {sum(SL)/len(SL):.1f}; visuals {figs} (1 per {words//max(figs,1)} words); headings {nh} (1 per {words//max(nh,1)} words)")
caps = [len(re.sub(r'<[^>]+>', ' ', c).split()) for c in re.findall(r'<figcaption[^>]*>(.*?)</figcaption>', page, re.S)]
print(f"INFO  caption words: {caps}; file size {len(page.encode())//1024} KB")
sys.exit(1 if fail else 0)
