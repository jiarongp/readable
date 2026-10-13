# Verdict: sparse-cts-reader-level (2026-10-13)

Case: an HTML rewrite of an HDBO idea note (sparse cylindrical Thompson sampling) in the maintainer's project, written with the skill at 3b55470. The skill inferred the reader instead of asking. The page came out at 29 minutes for a reader with basic Bayesian-optimization knowledge.

Reader (Gary), on the first version: the document "assume[s] a wrong level of the reader, which should ask me first at the beginning"; "the read time is too long, 29 min"; "the longer I spend time reading, the more I forget about what actually we are doing".

The second version was written after asking three questions (background: knows GP regression and Thompson sampling; target: about 10 minutes; cut: the belief ledger and the step-by-step test chain). It states three guiding questions up front, opens each section with a recap and a tracker of those questions, and moves derivations, check tables and side details into collapsed `<details>` boxes.

Templates are in `before/` and `after/`. The built pages (2–3 MB each, with embedded fonts and figures) are not committed. `after/build_sparse_cts_html.py` builds them inside the HDBO repository and measures reading time on the main path only.

Mechanical checks (`evals/tools/check_page.py`, built pages): all pass for both.

| | words in paragraphs | paragraphs | median p | p90 | max p | >80 | visuals | headings | main-path read time |
|---|---|---|---|---|---|---|---|---|---|
| before | 5730 | 69 | 77 | 136 | 263 | 33 | 11 | 19 | 29 min as displayed |
| after | 3325 | 50 | 61.5 | 104 | 154 | 10 | 7 | 13 | 11 min (2,835 words) |

`check_page.py` counts paragraphs inside the collapsed boxes too, so its word count for "after" exceeds the main path.

Rule changes made from this case (SKILL.md, html-page.md):
- Ask before writing a document: the reader's background, the target reading time, and what may be cut.
- Keep the goal in view in long documents: guiding questions up front, a recap sentence and a question tracker per section.
- Fit the agreed reading time with collapsed "More detail" boxes; measure reading time on the main path.

Reader (Gary) on the second version: pending.
