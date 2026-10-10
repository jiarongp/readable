# Repository restructure for the readable skill (2026-10-10)

Design record for the cleanup that prepared this repository to be the public home of the skill at github.com/jiarongp/readable. Decisions were made by Gary in an interview; this file records them and the resulting layout.

## Goal

The repository is consumed by the jiarongp/claude-marketplace, which copies the `skill/` folder whole (sources.json, path `skill`) and links it into `~/.claude/skills` and `~/.agents/skills`. The repository must therefore keep `skill/` as the installable unit, keep it small, and hold development evidence and documentation outside it. Research material from another project that had accumulated in the working tree had to go.

## Decisions

- **Home remote.** jiarongp/readable is the home (`origin`). dharmsen/readable, where the first version was merged, stays as `upstream`.
- **Research material.** The untracked `docs/`, `studies/`, `lfbo_sparse_moves_plan.md` and `Sparse-Move Step Scale.html` (about 1.6 GB) were a diverged partial copy of the hdbo project. Deleted outright; canonical copies live elsewhere. This included the skill's former calibration target `docs/readable/sparse_cts.md`; the excerpt kept in the sparse-cts comparison case is the retained trace of it.
- **Development material out of `skill/`.** Comparison cases, run outputs and tools move to a root `evals/` folder. `skill/evals/` keeps `evals.json` and its fixture, because the eval runner reads them beside `SKILL.md`.
- **Only current-skill evidence.** Comparison cases keep only outputs produced by the skill at commit da8c9b4: plan-sparse-cts-generator rep 11, technical-note-html rep 2, and paper-explainer-hdbo. Earlier reps and the api-lbfgsb-bounds case are deleted; their verdicts are trimmed to the surviving rep with a line pointing at git history. Each surviving rep folder is named `skill/`, so every case has the same shape: input or prompt, control, skill, verdict.
- **requirements.md dropped.** It was the original brief the skill was written from, and its uncommitted rewrite duplicated SKILL.md's rules in a second form that no agent reads. SKILL.md is the authoritative statement. The README carries a short principles summary and links to it.
- **refs.md to docs/references.md**, with its uncommitted edits, pointing to SKILL.md instead of the removed requirements file.
- **README** with purpose, principles summary, install (marketplace and direct symlink), layout, and development workflow. **.gitignore** for the `.remember/` plugin state, local settings, `.DS_Store`, `__pycache__/`.
- **Branches.** readable-v2 fast-forwards main; add-readable-skill and worktree-readable-skill, both fully contained in it, are deleted. main is pushed to origin (jiarongp).

## Resulting layout

```
README.md
.gitignore
skill/            SKILL.md, references/, agents/openai.yaml, evals/{evals.json, fixtures/}
evals/            README.md, comparisons/<case>/, runs/<date>/, tools/check_page.py
docs/             references.md, superpowers/specs/ (this record)
```

## Verification performed

`git status` clean apart from ignored paths; `skill/` at 68 KB; no file references `skill/evals/comparisons` or `documents/`; `evals/tools/check_page.py` runs from its new path against the technical-note case; `~/.claude/skills/readable` still resolves to `skill/`.
