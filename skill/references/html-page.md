# Delivering a document as an HTML page

A default readable document is one self-contained `.html` file that opens from disk in a browser. Its text, equations, and initial visuals are readable offline and without JavaScript. Read this reference when the requested output is HTML or the document uses the HTML default. An explicit request for another format takes precedence.

## Baseline page

Write the full skeleton. Nothing wraps the file later.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sparse-Move Step Scale</title>
<style>
/* Layout: one reading column, figures and tables may run wider inside their own scroll box. */
:root{
  --bg:#F7F6F2; --fg:#1D1F23; --fg-muted:#5B5F68; --rule:#D8D7D0;
  --accent:#2F5D8A; --code-bg:#ECEBE6;
  --font-body:"Source Serif 4",Georgia,serif;
  --font-ui:system-ui,-apple-system,"Segoe UI",sans-serif;
  --font-mono:ui-monospace,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#17181C; --fg:#E6E4DF; --fg-muted:#A9A7A1; --rule:#34363D;
    --accent:#8FB4DC; --code-bg:#23252B; color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --bg:#17181C; --fg:#E6E4DF; --fg-muted:#A9A7A1; --rule:#34363D;
  --accent:#8FB4DC; --code-bg:#23252B; color-scheme:dark;
}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.6 var(--font-body);
  padding-block:40px 80px;padding-inline:16px}
main{max-width:70ch;margin:0 auto}
h1,h2,h3{font-family:var(--font-ui);line-height:1.2;text-wrap:balance}
h2{margin-top:2.5em;padding-top:.6em;border-top:1px solid var(--rule)}
p{margin:.9em 0}
a{color:var(--accent)}
code,pre{font-family:var(--font-mono);font-size:.92em}
pre{background:var(--code-bg);padding:12px 14px;border-radius:4px;overflow-x:auto}
code:not(pre code){background:var(--code-bg);padding:.1em .3em;border-radius:3px}
figure{margin:1.6em 0}
figure img,figure svg{max-width:100%;height:auto;display:block}
figcaption{font-family:var(--font-ui);font-size:.9em;color:var(--fg-muted);margin-top:.5em}
table{border-collapse:collapse;font-variant-numeric:tabular-nums}
.table-wrap{overflow-x:auto}
th,td{padding:.4em .7em;border-bottom:1px solid var(--rule);text-align:left}
.meta{font-family:var(--font-ui);font-size:.9em;color:var(--fg-muted)}
nav.toc{font-family:var(--font-ui);font-size:.95em;border:1px solid var(--rule);padding:12px 18px;margin:1.6em 0}
nav.toc ul{margin:.3em 0;padding-left:1.2em}
.references li{margin:.4em 0;font-size:.95em}
input[type=range]{width:100%}
.math-display{overflow-x:auto;overflow-y:hidden}
</style>
</head>
<body>
<main>
  <h1 id="sparse-move-step-scale">Sparse-Move Step Scale</h1>
  <p class="meta">2026-10-10 · 12 min read · status: draft</p>
  <p>Opening paragraphs…</p>
  <nav class="toc"><ul><li><a href="#61-the-generator-and-what-k-means">6.1 The generator, and what k means</a></li></ul></nav>
  ...
  <h2 id="references">References</h2>
  <ol class="references"><li>…</li></ol>
</main>
</body>
</html>
```

Keep these properties whatever the visual treatment:

- **Self-contained.** CSS, JavaScript, data, and any library code are inline. Images and font files are embedded as `data:` URIs, or use system fonts. The page makes no network requests when opened or used. External citation and source links remain ordinary links the reader can follow. Keep the whole file under 16 MB.
- **Both themes.** Every color is a token defined first on bare `:root`, redefined under the two dark blocks shown above, and `body` sets its background from a token.
- **Readable column.** Running text stays near 70 characters wide with at least 16 px of side gutter. Only tables, code, and figures may be wider, each inside its own `overflow-x: auto` container. The page never scrolls horizontally.
- **Stable anchors.** Preserve explicit anchors and existing heading ids. Use the source renderer's Markdown slugs when known; otherwise use a consistent slug convention and check every in-document anchor link. Keep old ids as aliases when renaming a linked heading. An explicit anchor and a heading may share one target on the heading; each id occurs only once.
- **Metadata visible.** Front matter from a Markdown source becomes a short metadata line under the title and `<meta>` tags in the head. Values stay unchanged.
- **Exact code.** Code goes in `<pre><code>` with its decoded characters unchanged. Escape HTML-sensitive characters such as `<` and `&`.
- **Offline equations.** Render equations during document creation as native MathML or embedded SVG. Retain the exact original LaTeX in a MathML annotation or an HTML-escaped `data-tex` attribute on the equation container. Embed any supporting styles and fonts. Check both the retained source and the visible equation. If rendering is unavailable, preserve visible LaTeX and report the equation rendering as incomplete in the delivery note.

To render LaTeX offline, use the KaTeX command-line tool, installed with `npm install -g katex` (version 0.19.0 is present on this machine). It emits MathML that every current browser renders natively, with the source retained in an annotation:

```bash
echo '\prod_{j=1}^{m} P(g_j(x)\leq 0\mid x)' | katex -d -F mathml      # display equation
echo 'g_j(x) \leq 0' | katex -F mathml                                   # inline
```

Paste the `<math>…</math>` element into the page (the surrounding `<span class="katex">` can stay or go; no KaTeX stylesheet is needed for MathML). Keep `.katex-display`-style horizontal scrolling on wide display equations. If the tool is missing, keep the LaTeX visible between `$$` delimiters and say so in the delivery note.

## Document conventions

Model the page on a long-form technical blog post such as Lil'Log. The parts, in order:

1. **Title**, then one metadata line: date, estimated reading time (about 250 words a minute), author when known, and the source file for a rewrite.
2. **Opening paragraphs** that orient the reader and say what the document covers. No heading above them.
3. **Table of contents**: a nested list of anchor links to every h2 and h3, inside `<nav class="toc">`.
4. **Sections** with topic headings. The first sentence of a section states its first point.
5. **References**, when sources are cited: a numbered list, one entry per cited source, in the form Author et al. "Title." Venue Year, with the title linked. Use the available bibliographic details; preserve verification notes and identify missing details rather than inventing them. Every inline citation appears in this list. Keep non-paper sources in their appropriate form, such as a documentation title and link.

Inline citation markup:

```html
<p>Self-consistency (<a href="https://arxiv.org/abs/2203.11171">Wang et al. 2023</a>) picks the majority answer among several chains of thought.</p>
```

## Visual elements

Choose the form that teaches the mechanism best. All forms stay self-contained and keep the page complete at rest: a reader with JavaScript off, or a thumbnail, sees a finished page.

**Static figure.** Generate it with a script saved beside the document, as the main skill requires. Render to PNG at about twice the displayed width (1600 px wide is enough for a full-column figure), then embed it:

```bash
python3 -c 'import base64,sys;print("data:image/png;base64,"+base64.b64encode(open(sys.argv[1],"rb").read()).decode())' fig_step_vs_k.png
```

```html
<figure>
  <img src="data:image/png;base64,…" alt="Step scale against k for three concentrations" width="1600" height="900">
  <figcaption>Illustration with hypothetical values, not measured data. Each line is one concentration; read left to right to see the step scale shrink as k grows, and compare the lines to see that higher concentration keeps the scale larger.</figcaption>
</figure>
```

Set `width` and `height` to the image's pixel size so the layout does not jump while loading. If the plotting library is unavailable, keep the script, leave a placeholder paragraph where the figure belongs, and state in the delivery note that the figure was not rendered.

**Inline SVG diagram.** For boxes, arrows, and simple geometry, write the SVG inline with a `viewBox`, explicit fills, and colors taken from the theme tokens so it reads in both themes. Leave room inside the `viewBox` for the outermost labels.

**Interactive element or animation.** A slider that moves a parameter and redraws a curve, a stepper that walks through an algorithm, or an animation of a process are all welcome when they show something a static picture cannot. Rules:

- Scripts are inline. If a library is needed, embed a fixed version with its license notice, before the script that uses it.
- Embed a finished initial SVG or image in the HTML. It shows the mechanism before JavaScript runs; JavaScript updates that visual when the reader uses the controls.
- Give controls visible labels and a readout of the current value. Use `<input type="range">`, `<button>`, and `<select>` with stable `id`s.
- Honor `prefers-reduced-motion`: an animation offers a play button or a stepper instead of autoplaying for those readers.
- Keep the data small and inline. Do not fetch anything at runtime. Controls start disabled or hidden and become available only after initialization succeeds, leaving the initial visual visible if initialization fails.

**Pictures from the source.** A figure taken from a paper or page is embedded as a data URI like any image, and its caption ends with the source: `(Image source: <a href="…">Author et al. 2023</a>)`. Include it only when the license permits.

Every visual has a `<figcaption>` that carries the how-to-read guidance from the main skill.

## With the artifact-design skill

When the `artifact-design` skill is available, load it and let it decide palette, typefaces, and layout for this document, using the tokens above as the structure it fills in. Two of its instructions do not apply to a local file:

- Keep the full `<!doctype html>`, `<head>`, and `<body>` skeleton. That skill omits them because a publishing step adds them; nothing adds them here.
- Skip publishing, the `icon` parameter, and the `description` parameter. The deliverable is the file on disk.

The offline, self-contained requirements in this reference still apply to its visual choices. Embed fonts and libraries or use the baseline's system fonts and inline code.

Without that skill, use the baseline above as it stands.

## Before delivering

Run mechanical checks on every finished page:

- Check loaded resources separately from navigation links. Inspect scripts, stylesheet links, image sources and `srcset`, SVG image references, media, frames, CSS `url(...)` and `@import`, and JavaScript network calls. Loaded resources are inline or embedded; ordinary `<a href>` citation links may point to external sites.
- Confirm a full HTML skeleton, defined theme tokens, embedded images, unique ids, and resolving table-of-contents and other in-document anchor links. Confirm the file is under 16 MB.
- Compare decoded code text and retained LaTeX against the source. Confirm cited sources appear in References and source metadata keeps its values.

When browser inspection is available, also open the finished page at a narrow and a desktop width, in both themes. Disable network access and JavaScript to check that equations and initial visuals remain visible. Then enable JavaScript and try the controls. Inspect overflow, clipped labels, captions, and contrast. Mechanical checks complement this inspection; they do not establish visual readability.

In the delivery note, give the file path and name the generating scripts. Mention incomplete rendering or other unresolved issues briefly. If browser inspection was unavailable, say that the page was checked mechanically only.
