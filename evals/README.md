# Development evidence for the readable skill

The eval definitions (`evals.json`) and their fixture stay in `skill/evals/`, because the eval runner reads them next to `SKILL.md`. Everything here is the evidence those evals and the comparison cases produced, kept out of `skill/` so the marketplace copy stays small.

- `comparisons/<case>/`: one case per folder, same shape in each. The input or prompt, a control output written without the skill where one exists, the skill output in `skill/`, and `verdict.md` with the mechanical measurements and the reader's judgment. Each verdict names the skill commit it was run against. Outputs from earlier skill versions are in git history before the 2026-10-10 cleanup.
- `runs/<date>/`: a full sweep of `evals.json`, one fresh subagent per eval, with `results.md` grading every assertion and `grade.py` as the helper.
- `tools/check_page.py <page.html> [source.md]`: mechanical checks for an HTML document. Network loads, skeleton, theme tokens, ids and anchors, table of contents, References, retained LaTeX against the source, and density statistics. Exit code 1 on a hard failure.
