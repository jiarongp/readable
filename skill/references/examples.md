# Examples of readable technical writing

Read this when deciding how much to unpack a dense passage. These are patterns, not templates for every answer. The examples are illustrative, not reports about a particular project.

## Give technical terms a purpose

Source:

> A trust region constrains candidate generation around the incumbent to restrict the search to a local neighborhood.

Rewrite:

> The optimizer searches near the best solution found so far. This solution is called the **incumbent**.
>
> A **trust region** sets the bounds of this local search. The optimizer generates candidate solutions within those bounds.

The rewrite gives each term a role. It does not claim that a trust region freezes variables or guarantees better results. Those claims would need support.

## Explain the relationship after introducing the concepts

Source:

> The acquisition function ranks unevaluated candidates by expected improvement under a Gaussian process posterior conditioned on noisy observations, rather than by the posterior mean alone; a point with a worse predicted mean can therefore be selected because uncertainty increases its expected improvement, though this does not guarantee that the next evaluation improves the incumbent.

Rewrite:

> The optimizer needs to choose which candidate to evaluate next. An **acquisition function** gives each candidate a score for that decision.
>
> Here, the score is **expected improvement**: how much the candidate is expected to improve on the best result found so far. The calculation accounts for possible outcomes, including outcomes that offer no improvement.
>
> The calculation uses a Gaussian process model, which predicts both the objective value and uncertainty about that prediction. Its **posterior distribution** represents the model's updated beliefs about the objective after accounting for the noisy observations.
>
> The score uses this distribution, rather than only its mean prediction. A candidate with a worse mean prediction can still receive a higher score because its uncertainty leaves room for a better outcome.
>
> A high score does not guarantee an improvement. The actual result is known only after the candidate is evaluated.

The rewrite preserves the method, the role of noisy observations, the comparison with the mean, and the qualification. It is longer because those ideas need separate introductions.

## Preserve the conditions that make a claim true

Source:

> Assuming independent constraint models, feasibility is estimated by multiplying marginal satisfaction probabilities, which may be misleading when the constraint events are dependent.

Rewrite:

> We want to estimate the probability that a candidate satisfies all constraints.
>
> If the constraint models treat the constraint events as independent, we estimate this probability by multiplying the probability of satisfying each constraint.
>
> The independence assumption matters. If the constraint events are dependent, this product can give a misleading estimate.

“Multiply the probabilities to find feasibility” would remove the condition on which the calculation depends.

## Keep short sentences connected

Fragmented:

> The model is uncertain. The score increases. The candidate is selected.

Better:

> The candidate's uncertain prediction leaves room for a large improvement. That possibility can raise its expected improvement score, so the optimizer may select it.

Short sentences alone do not explain the relationship. The connected version also avoids turning a possibility into a guarantee.

## Rewrite a prompt without executing it

Source prompt:

> Inspect src/cache.py and tests/test_cache.py, report why simultaneous callers may compute the same missing key more than once despite the existing lock, propose a minimal correction that preserves the public API and error propagation, and do not edit files or run commands that write to disk; if the available code does not establish the cause, say what remains unknown rather than treating a plausible race as proven.

Rewritten prompt:

> Inspect `src/cache.py` and `tests/test_cache.py`.
>
> Investigate why simultaneous callers may compute the same missing key more than once, despite the existing lock. Report what the available code establishes about the cause.
>
> Propose a minimal correction. The correction must preserve the public API and error propagation.
>
> Do not edit files or run commands that write to disk.
>
> If the code does not establish the cause, explain what remains unknown. Do not present a plausible race as proven.

The rewrite makes the instructions easier to find. It preserves the investigation, the proposal, and the limits on actions. Rewriting this prompt does not authorize inspecting those files.

## Keep familiar material compact

Request:

> I know Python and NumPy. In two sentences, explain what this array operation does.

Response pattern:

> State the operation and its effect on the array. Use the second sentence for the important shape, axis, or behavior detail.

No introduction to Python or arrays is needed. The reader's stated background and requested length control how much context to add.
