Rewritten note saved beside the source as `fixtures/technical-note.html` (full path: `/Users/gary/workspace/readable/skill/evals/runs/2026-10-10/eval-3/fixtures/technical-note.html`). The source `technical-note.md` is unchanged.

The page is one self-contained HTML file that reads offline, without JavaScript, in light and dark themes. The equations are rendered to MathML with the original LaTeX retained in annotations, the code block is verbatim, and the `../evals.json` link, the `#feasibility` anchor, and the front-matter values (title, `status: draft`) are preserved. The rewrite adds a Limitations section, since the source says the note covers the limitations but had no section for them; its contents come only from the source's own qualifications.

Two visuals were added, both labelled as illustrations with hypothetical values:

- `fixtures/fig_product_vs_m.py` generates the figure showing how the product score falls as constraints are added. Re-render with `uv run --offline --no-project --with matplotlib --with numpy python3 fig_product_vs_m.py`; the PNG (`fig_product_vs_m.png`) is embedded in the page as a data URI.
- An inline SVG diagram of the `(32, 3)` array collapsing to the `(32,)` score vector under `prod(axis=1)`.

Two gaps in the source are named in the page rather than filled in: it does not say where the satisfaction probabilities come from, and it does not name the array library (the explanation of `prod(axis=1)` uses NumPy's conventions, which the stated shapes follow). The page was checked mechanically only (anchors, unique ids, no external loads, exact code and LaTeX against the source); no browser was available for a visual inspection.
