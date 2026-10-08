**Short answer.** `bounds` turns L-BFGS-B into a box-constrained optimizer: every point it evaluates `fun` at lies inside the box `lb <= x <= ub`, and the convergence test ignores gradient components that push against a bound. A coordinate with `lb == ub` is treated as fixed: it stays at that value for the whole run, the optimizer never moves it, and your gradient entry for it is ignored. Details and caveats below.

## What `bounds` does

`bounds` is one `(lower, upper)` pair per coordinate (or a `scipy.optimize.Bounds` object). `None` or `±np.inf` means "no bound on that side." The bounds are hard constraints, not a penalty. L-BFGS-B keeps every iterate feasible, which matters when `fun` is undefined or meaningless outside the box, for example a log of a variance that must stay positive. SciPy also clips `x0` into the box before the first evaluation, so a starting point outside the box is moved onto the nearest face rather than rejected.

Inside each iteration, the bounds show up in three places:

1. **Choosing the active set.** L-BFGS-B builds a quadratic model of `fun` from its limited-memory BFGS Hessian approximation. It then walks along the *projected* steepest-descent path: the negative gradient direction, but with each coordinate stopped when it reaches its bound. The first local minimizer of the quadratic model along this piecewise-linear path is called the generalized Cauchy point. Any coordinate that hit a bound on the way there is marked *active* and held at that bound for the rest of the iteration.

2. **Minimizing over the free variables.** With the active coordinates frozen, the quadratic model is minimized over the remaining free coordinates only (the subspace step). If that step would leave the box, it is cut back so it does not.

3. **Line search.** Finally, a line search runs from the current point toward the subspace solution. The maximum step length is capped so the trial point stays inside the box.

Each iteration recomputes the active set, so a coordinate can arrive at a bound, sit there for several iterations, and leave again if the gradient later points back into the interior.

**Convergence** uses the *projected gradient*. For coordinate `i`, the projected component is `g_i` unless `x_i` is at a bound and `g_i` points outward (at the lower bound with `g_i > 0`, or at the upper bound with `g_i < 0`), in which case it is 0. The run stops when `max |projected g| <= pgtol` (default `1e-5`) or when the relative decrease in `fun` falls below `ftol` (default about `2.2e-9`, from `factr * machine epsilon`). So a solution pinned to a bound with a large raw gradient still counts as converged, which is the correct behavior for a constrained minimum. If you inspect `res.jac` afterward and see a big entry, check whether that coordinate is at a bound before concluding the optimizer stopped early.

## A coordinate with equal bounds

If `lb[i] == ub[i]`, the box has zero width in that direction. The projected-gradient path has no room to move in coordinate `i`, so the coordinate is active from the first iteration and never enters the subspace step. Its projected gradient component is always 0, so it never contributes to the stopping test. Concretely:

- `x[i]` keeps the exact value `lb[i]` in every call to `fun` and `jac`, and `res.x[i]` equals it exactly, not approximately.
- Your objective still receives the full vector including `x[i]`, and your gradient is still expected to have an entry at position `i`. That entry is read but has no effect on the iterates.
- The remaining coordinates are optimized as if coordinate `i` were a constant.

This is a common way to freeze a parameter without changing the objective's signature or re-indexing the gradient. The alternative is to drop the coordinate and close over its value in the objective; both give the same optimum over the free coordinates, so the choice is about convenience.

One caveat I am not certain about: if you let SciPy estimate the gradient by finite differences instead of supplying `jac`, the difference step for a zero-width coordinate cannot be taken. Recent SciPy versions handle this case, but I would not rely on it in older versions without checking, since a `nan` gradient entry can propagate. If the project uses finite-difference gradients with equal bounds, it is worth a quick test on your installed version, or supply an analytic gradient and set that component to any finite value.
