## What `bounds` does in `minimize(..., method="L-BFGS-B")`

`bounds` is a box constraint: one `(lower, upper)` pair per coordinate of `x` (or a `scipy.optimize.Bounds` object). `None` or `±inf` on a side means "unbounded on that side". L-BFGS-B is not "L-BFGS plus clipping afterwards"; the bounds are built into every step of the algorithm, and the solver only ever visits feasible points.

Concretely, during the run:

1. **Starting point.** `x0` is projected (clipped) into the box before the first function evaluation. Recent SciPy versions warn when it had to clip.

2. **Each iteration is a projected quasi-Newton step.**
   - It first walks along the steepest-descent direction, projected onto the box, and finds the *generalized Cauchy point*. Along that path, coordinates that hit a bound get pinned there. This gives an "active set": coordinates stuck at a bound for this iteration.
   - It then does a subspace minimization over only the *free* coordinates, using the limited-memory BFGS approximation of the Hessian (built from the last `maxcor` pairs of steps and gradient differences). The result is projected back into the box.
   - It runs a line search (Moré–Thuente) along the resulting direction, with the maximum step capped so that the trial points stay inside the box.
   
   So the box is respected at the level of search directions and step lengths, not by evaluating `f` outside and rejecting.

3. **Your objective and gradient are only ever called at feasible `x`.** That is why people lean on L-BFGS-B when `f` is undefined outside a region (log of a negative number, a covariance that must stay positive, etc.). If you let SciPy estimate the gradient by finite differences (`jac=None`), it also respects the bounds: near a bound it switches to a one-sided difference so the probe points stay inside the box.

4. **Convergence is measured with the projected gradient.** The `gtol`/`pgtol` test uses `max |proj_g_i|`, where for a coordinate sitting at a bound with the gradient pushing it further *out* of the box, the component is treated as zero. So a solution pressed against a bound counts as converged even though the raw gradient there is nonzero. The returned `res.x` always satisfies the bounds; `res.jac` is the raw gradient, so do not expect it to be ~0 at active bounds.

Things that do *not* happen: no penalty terms are added to `f`, no Lagrange multipliers are returned, and `Bounds(..., keep_feasible=...)` has no effect for this method since it is always feasible anyway.

## A coordinate with `lower == upper`

That coordinate is simply **fixed**. The L-BFGS-B code (the original Fortran, and SciPy's C translation since 1.15) checks `l(i) == u(i)` and marks that variable as "always at a bound". Consequences:

- `x0[i]` is overwritten by the fixed value (via the initial clipping), whatever you passed in.
- The coordinate is never in the free set, so its search direction component is always 0 and it never moves. The L-BFGS curvature pairs `(s, y)` have `s_i = 0` there, so it does not pollute the Hessian approximation.
- Its gradient component is ignored for convergence: the projected gradient on a fixed coordinate is identically 0 (whichever sign the gradient has, it is "pushing out" of a zero-width box).
- Your `jac` is still called with the full-length `x` and should still return a *finite* number for that component (the value is irrelevant, but NaN there can confuse the projected-gradient bookkeeping). With finite-difference gradients, SciPy treats the zero-width interval as a zero step and effectively reports 0 for that component; very old SciPy versions could emit divide-by-zero warnings here, so if you see those, that is the cause.

In practice, equal bounds are the idiomatic way to freeze a subset of parameters without rewriting the objective or re-indexing the vector. The only cost is that the problem dimension is not reduced: the solver still carries those coordinates around, which is negligible unless you are fixing most of a very large vector, in which case a wrapper that slices out the free coordinates is cleaner.

Quick illustration:

```python
from scipy.optimize import minimize
import numpy as np

f = lambda x: (x[0] - 3)**2 + (x[1] + 1)**2
res = minimize(f, x0=[10.0, 10.0], method="L-BFGS-B",
               bounds=[(0, 1), (2, 2)])   # x1 frozen at 2
print(res.x)    # [1., 2.]  -> x0 pinned at its upper bound, x1 never moved
print(res.jac)  # ~[-4., 6.] -> raw gradient, nonzero at the active bounds
```
