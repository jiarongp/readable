# Verdict: technical-note-html (2026-10-10, reader judgment pending)

Case: eval 3 (fixtures/technical-note.md) run against the skill after the HTML-output change. Fresh general-purpose subagent, working on a scratch copy of fixtures/ with evals.json one level up. The agent loaded `artifact-design` on its own, as html-page.md tells it to.

## Mechanical checks (all pass)

| check | result |
|---|---|
| source unchanged | md5 identical before and after |
| output | one file, technical-note.html, 172 KB, no .md copy |
| skeleton | full doctype, head, body |
| external loads | KaTeX 0.16.11 on cdnjs, Google Fonts; nothing else |
| themes | bare :root tokens plus both dark blocks |
| figure | 1 PNG embedded as data URI; script and PNG saved beside |
| heading ids | constraint-scoring-note, feasibility, batch-operation |
| anchors | #feasibility resolves; ../evals.json target kept |
| code | pre/code block, characters unchanged |
| equation | LaTeX between $$, characters unchanged |
| metadata | title and status visible under the heading and as meta tags |

## Observations for the reader

- Length: the 200-word source became a page with a definitions list, a two-constraint example, a worked three-constraint instance, a figure with caption, an independence callout with a dependent-constraints example, and a hypothetical input table. Same doubling pattern seen in plan-sparse-cts-generator reps 2-9.
- The agent's delivery note claimed `../evals.json` does not exist one level above fixtures/. It does. An unsupported statement in the delivery note, not a page defect.
- The source has both `<a id="feasibility">` and a Feasibility heading. The agent merged them into one id on the heading, which is valid HTML, and said so.

Reader (Gary): pending.

## Rep 2 (2026-10-10, after Gary's rewrite of the skill; output in rep2/)

Fresh subagent, same prompt, scratch copy of fixtures/. Agent loaded `artifact-design` and `dataviz` on its own. Equations rendered with `katex -F mathml` (26 MathML elements, LaTeX retained in annotations); figure in light and dark variants; one hand-written inline SVG for the (32, 3) to (32,) collapse.

Mechanical checks (tools/check_page.py against fixtures/technical-note.md): all pass. No network loads, full skeleton, both theme blocks, 2 data-URI images, unique ids, 7/7 anchors resolve, TOC covers every heading, source equation and code retained exactly.

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
