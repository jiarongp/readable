---
title: Constraint scoring note
status: draft
---

# Constraint scoring note

This note describes candidate scoring, the batch operation, and the limitations; the batch size is 32 and the reason for that choice is not recorded. The [evaluation cases](../evals.json) accompany this note. See [feasibility](#feasibility) for the probability calculation.

<a id="feasibility"></a>

## Feasibility

Assuming independence of the constraint events conditional on the candidate x, feasibility is calculated as the product of the individual satisfaction probabilities, where m is the number of constraints and g_j(x) <= 0 indicates satisfaction of constraint j, but dependence between constraint events can invalidate this calculation.

$$
P(\mathrm{feasible}\mid x)=\prod_{j=1}^{m}P(g_j(x)\leq 0\mid x)
$$

## Batch operation

The implementation multiplies the entries in each row of probabilities, which has shape (32, 3) because there are 32 candidates and 3 constraints, to return a score vector with shape (32,), without establishing whether the independence assumption is justified.

```python
def feasibility_score(probabilities):
    return probabilities.prod(axis=1)
```

The result is a score under the stated assumption, not a guarantee that the selected candidate will satisfy the constraints.
