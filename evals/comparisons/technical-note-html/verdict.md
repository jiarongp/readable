# Verdict: technical-note-html (2026-10-10, reader judgment pending)

Case: eval 3 of skill/evals/evals.json (fixtures/technical-note.md), a rewrite that must keep metadata, links, anchors, equation and code. Source copy in input.md. Skill output in skill/, produced by a fresh general-purpose subagent working on a scratch copy of fixtures/, with the skill at commit da8c9b4 (Gary's rewrite of 2026-10-10).

Rep 1 ran against the skill before the offline rule (KaTeX loaded from a CDN). Its output and verdict are in git history before the 2026-10-10 repository cleanup.

## Rep 2 (2026-10-10, after Gary's rewrite of the skill; output in skill/)

Fresh subagent, same prompt, scratch copy of fixtures/. Agent loaded `artifact-design` and `dataviz` on its own. Equations rendered with `katex -F mathml` (26 MathML elements, LaTeX retained in annotations); figure in light and dark variants; one hand-written inline SVG for the (32, 3) to (32,) collapse.

Mechanical checks (evals/tools/check_page.py against skill/evals/fixtures/technical-note.md): all pass. No network loads, full skeleton, both theme blocks, 2 data-URI images, unique ids, 7/7 anchors resolve, TOC covers every heading, source equation and code retained exactly.

| | words | paragraphs | median p | p90 | max p | >80 | visuals | headings |
|---|---|---|---|---|---|---|---|---|
| source | ~200 | 5 | | | | | 0 | 2 |
| rep 1 (KaTeX CDN era) | not measured by this tool | | | | | | 1 | 3 |
| rep 2 | 1018 | 23 | 43 | 78 | 83 | 1 | 2 | 5 |
| Lil'Log reference | | | 26–33 | 75–106 | | | 1 per ~250 words | 1 per ~450 words |

Observations for the reader:
- Five sections for a 200-word source, including two new ones: "When the constraints are not independent" (two-event bounds with a short derivation, a figure, a table) and "What the score does and does not promise". The bounds are standard probability, not from the source; the agent labeled them as added background. Judge whether this is supported context or an unsupported addition.
- Headings every 203 words, denser than the reference; visuals every 509 words, sparser.
- Delivery note is accurate this time (no false claim about ../evals.json). It states that the page was checked mechanically only.
- No References section because nothing is cited, which the rule permits.

Reader (Gary): pending.
