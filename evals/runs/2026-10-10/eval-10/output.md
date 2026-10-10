Wrote `/Users/gary/workspace/readable/skill/evals/runs/2026-10-10/eval-10/offline-example.html`, one self-contained page (about 21 KB) with no external resources.

- The equation is rendered as native MathML with the KaTeX command-line tool (0.19.0), so it reads offline and without JavaScript. The LaTeX source is retained in each `<annotation encoding="application/x-tex">` element; the display equation's container also carries `data-tex="y = x + 1"`, and the inline uses of `x + 1` carry `data-tex="x + 1"`.
- The two examples, x = 0 giving y = 1 and x = 2 giving y = 3, are labeled as hypothetical in the text and the table.
- The inline SVG draws the line through (0, 1) and (2, 3) with a marked point at (1, 2) and dashed guides to both axes. It is complete at rest. The slider (x from 0 to 2, step 0.1) starts disabled and is enabled by the inline script, which moves the point, its label, the guides, and the readout. With JavaScript off, a note under the slider says the point stays at x = 1.
- No figure scripts: the SVG is written directly in the HTML. No sources are cited, so there is no References section.

Checks: no external loads, unique ids, table-of-contents anchors resolve, and the script parses. Headless Chrome screenshots at desktop width in light and dark themes and at 400 px width looked right. I did not operate the slider in a browser; its behavior was checked by reading the script only.
