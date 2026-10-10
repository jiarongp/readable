# Verdict: plan-sparse-cts-generator (2026-10-10, reader judgment pending)

Case: rewrite of a plan excerpt. Source in input.md (sparse_cts_plan.md §6.1–6.3 of the hdbo project, as of 2026-10-08); prompt in prompt.md; control (no skill) in control.md; a human-preferred rendering of the same material in target-excerpt.md. Skill output in skill/, produced by a fresh general-purpose subagent with the skill at commit da8c9b4 (Gary's rewrite of 2026-10-10).

Reps 1–10 ran against earlier skill versions (commit 69edaaf through the first HTML-output change). Their outputs and verdicts, and the rules each one verified, are in git history before the 2026-10-10 repository cleanup.

## Rep 11 (2026-10-10, after Gary's rewrite of the skill; output in skill/)

Fresh subagent, same prompt as rep 10. Loaded `artifact-design` and `dataviz`. Rendered all math offline with `katex -F mathml` (154 MathML elements, LaTeX retained), three figures in light and dark variants, no JavaScript at all. Took headless-Chrome screenshots itself at desktop and phone width and in dark theme, and fixed a display-equation alignment bug it found. Wrote a build.py and page_template.html alongside the deliverable.

Mechanical checks (evals/tools/check_page.py): all pass. No network loads, full skeleton, both theme blocks, 6 data-URI images, unique ids, 15/15 anchors resolve, TOC covers every heading, References present, all 5 display equations retained exactly. FACT/HYPOTHESIS/VERIFY labels and §2, §4, Step 0, Step 3 references kept.

| | words | p count | median p | p90 | max p | p >80 | sentence median / mean | visuals | headings |
|---|---|---|---|---|---|---|---|---|---|
| source | 779 | 10 | 75 | | 198 | 4 | 24.4 mean | 0 | 3 |
| target excerpt | 1041 | 17 | 43 | | 61 | 0 | 13.7 mean | 2 | |
| rep10 (prose only, this tool) | 1450 | 25 | 58 | 90 | 116 | 7 | 18.5 / 18.6 | 2 | 4 |
| rep11 (prose only, this tool) | 2174 | 30 | 71.5 | 118 | 130 | 13 | 22.0 / 24.7 | 3 | 14 |
| Lil'Log (2 posts) | | | 26–33 | 75–106 | | | 17–20 / 18–22 | 1 per ~250 w | 1 per ~450 w |

Observations for the reader:
- Density moved the wrong way on this rep: paragraphs are longer than rep 10 and than the source median; 13 paragraphs over 80 words; sentences averaging 24.7 words. One rep, so sampling may explain part of it. Candidate cause to test with more reps: the rewrite's document guidance now lives in three places (SKILL.md "Organize the explanation", calibration.md, html-page.md) and the paragraph rule competes with the new "make each paragraph advance the explanation" bullet.
- Heading every 155 words (h3 under every h2 subsection), visual every 724 words; captions of 140, 91 and 190 words. Inverse of the reference shape.
- The agent added a reference the source does not cite (Eriksson et al. 2019, TuRBO), flagged it in the delivery note and in the References entry.
- Extra files beside the deliverable (build.py, page_template.html). Useful for regeneration; not requested.
- Formats and offline rules: fully met, first rep to do so.

Reader (Gary): pending.
