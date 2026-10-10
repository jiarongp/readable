---
title: Constraint scoring note
status: draft
---

# Constraint scoring note

This note explains how we score a candidate on whether it is likely to satisfy a set of constraints. For each candidate `x` we have a probability of satisfying each constraint, and we combine those probabilities into one **feasibility** score. The note covers the probability calculation, the implementation that scores a batch of candidates at once, and the limits of what the score tells us.

The [evaluation cases](../evals.json) accompany this note.

Contents:

- [Feasibility](#feasibility): how the score is calculated and the assumption it relies on
- [Batch operation](#batch-operation): how the implementation scores 32 candidates in one call
- [Limitations](#limitations): what the score does and does not establish

<a id="feasibility"></a>

## Feasibility

We want the probability that candidate `x` satisfies every constraint at once. There are `m` constraints. Each constraint `j` has a function `g_j`, and the candidate satisfies constraint `j` when `g_j(x) <= 0`. For each constraint we have the probability that this holds, conditional on the candidate: `P(g_j(x) <= 0 | x)`.

To combine these `m` probabilities, we assume the constraint events are **independent conditional on `x`**: given the candidate, knowing that one constraint is satisfied tells us nothing about whether another is. Under this assumption, the probability that all constraints hold is the product of the individual satisfaction probabilities:

$$
P(\mathrm{feasible}\mid x)=\prod_{j=1}^{m}P(g_j(x)\leq 0\mid x)
$$

Each factor is the probability of satisfying one constraint at `x`, and the product is the probability of satisfying all of them. As a hypothetical example, with three constraints and satisfaction probabilities 0.9, 0.8, and 0.5, the feasibility is 0.9 × 0.8 × 0.5 = 0.36. Because every factor is at most 1, each additional constraint can only lower the score, and a single unlikely constraint pulls the score down the most.

The independence assumption matters. If the constraint events are dependent, the product can misstate the true feasibility in either direction. As a hypothetical case, suppose two constraints are always satisfied or violated together, each with probability 0.9. The true probability that both hold is 0.9, but the product gives 0.81. Dependence between constraint events can therefore invalidate this calculation.

## Batch operation

The implementation scores a batch of candidates in one call rather than one candidate at a time. The batch size is 32; the reason for that choice is not recorded.

The input, `probabilities`, is an array with shape `(32, 3)`: one row per candidate, because there are 32 candidates, and one column per constraint, because there are 3 constraints. Entry `[i, j]` is the probability that candidate `i` satisfies constraint `j`.

```python
def feasibility_score(probabilities):
    return probabilities.prod(axis=1)
```

`prod(axis=1)` multiplies the entries along each row, so a candidate's three probabilities collapse into one feasibility score. The result is a score vector with shape `(32,)`, one score per candidate. This is the product formula from [Feasibility](#feasibility) applied to every row at once.

A hypothetical two-row slice of the input and its output (the real batch has 32 rows):

```
probabilities                        feasibility_score(probabilities)
rows: candidates, columns: constraints
[[0.9, 0.8, 0.5],          ->        [0.36,
 [0.7, 0.7, 0.7]]                     0.343]
```

The function applies the product directly. It does not check whether the independence assumption is justified for these constraints, and nothing else in the implementation establishes that either.

## Limitations

- **Independence is assumed, not verified.** The product in [Feasibility](#feasibility) is valid only when the constraint events are independent given `x`. Dependence between constraint events can invalidate the calculation, and the implementation does not establish whether the assumption holds.
- **The score is not a guarantee.** Even under the assumption, the result is a probability. A high score means the candidate is likely to satisfy the constraints, not that the selected candidate will satisfy them.
- **The batch size is an unrecorded choice.** The batch size is 32, and the reason for that choice is not recorded.
