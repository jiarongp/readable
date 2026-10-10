# Verdict: paper-explainer-hdbo (2026-10-10, reader judgment pending)

Case: direct write from a prompt (not a rewrite). Prompt in prompt.md. Source: arXiv HTML and text extraction of Doumont et al. 2025 (arXiv 2512.00170) in paper/. Fresh general-purpose subagents, control (no skill) and skill (Gary's rewritten SKILL.md of 2026-10-10, with html-page.md naming the katex CLI).

## Outputs

| | format | files | words | prose paras | median p | p90 | max | >80 | sentence median / mean | visuals | headings |
|---|---|---|---|---|---|---|---|---|---|---|---|
| control | Markdown + PNG | note, fig script, PNG | 3663 total (1446 prose, 1992 in lists) | 31 | 29 | 107 | 167 | 8 | 16 / 19.8 | 1 | 16 |
| skill | HTML | note, template, build script, fig script, 3 PNG | 3893 prose | 68 | 55.5 | 92 | 114 | 15 | 23 / 24.8 | 3 (1 per 1297 w) | 18 (1 per 216 w) |
| Lil'Log (2 posts) | | | | | 26–33 | 75–106 | | | 17–20 / 18–22 | 1 per ~250 w | 1 per ~450 w |

## Mechanical checks on the skill output (evals/tools/check_page.py): all pass

No network loads, full skeleton, both theme blocks, 3 data-URI images, unique ids, 45/45 anchors resolve, TOC covers every heading, References present. 172 equations as MathML with retained LaTeX. 392 KB.

## Observations for the reader

Skill output:
- Follows the Lil'Log shape: orienting paragraphs, TOC, topic headings that state the point ("A plain linear kernel only ever picks corners"), author-year citations, numbered References (23 entries), a labeled "my own reading" section separated from the paper's claims.
- Citations link to the References list (#ref-…) rather than directly to arXiv as Lil'Log does. Only 5 References entries carry arXiv links; the note states above the list that links other than the paper's were added from memory and are unverified. The checker confirms the ids are not in the paper text (its bibliography has no arXiv ids), so they are unverified in both directions.
- Flags a likely typo in the paper (√(3/D) vs √(D/3) lengthscale) as an aside. Worth checking against the PDF; if right, it is a useful catch; if wrong, it is an invented error.
- Density: median paragraph 55 words, 15 paragraphs over 80, mean sentence 24.8. Same direction as plan-sparse-cts-generator, and above both the control and the reference. Visuals sparse for the length.
- Three figures are the agent's own illustrations (boundary seeking, D=1 projection, thin-shell Monte Carlo), each labeled as such.
- Extra files: template and build script, as in plan-sparse-cts-generator.

Control:
- Markdown with a TL;DR and 16 headings; more than half of its words are in bullet lists. Numbered-section headings ("3.1 The kernel"). No citation links at all. One figure. Its prose paragraphs are shorter (median 29) because most content went into lists.
- Also separates the authors' open questions from its own caveats, and also notes the abstract's "outperforms" versus the body's "matches".

Pattern across today's three skill reps: formats and offline rules are met every time; prose gets wordier as the document gets longer (technical-note-html median 43 / mean sentence 18.9; plan-sparse-cts-generator median 71.5 / 24.7; this one 55.5 / 24.8).

Reader (Gary): pending.
