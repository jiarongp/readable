<!-- Skill version: after adding paragraph-contract, picture-before-mechanism, and figure rules (2026-10-08) -->

**Short answer.** `bounds` turns the problem into a box-constrained one: each coordinate `x[i]` must stay in `[lb[i], ub[i]]`. L-BFGS-B enforces this inside the algorithm, not as a penalty: it never evaluates `fun` outside the box, it freezes coordinates that sit on a bound and optimizes only the free ones, and it declares convergence using the *projected* gradient instead of the raw gradient. A coordinate with `lb[i] == ub[i]` is a special case of this: it is pinned at that value from the first iteration, never moves, and `res.x[i]` comes back equal to it.

## What `bounds` is

`bounds` is one `(min, max)` pair per coordinate (a list of tuples or a `scipy.optimize.Bounds` object). `None` or `±np.inf` means "no bound on that side". The bounds are independent per coordinate, so they describe an axis-aligned box; L-BFGS-B cannot express anything coupling coordinates, like `x[0] + x[1] <= 1`.

Two things happen before the first iteration:

- SciPy raises `ValueError` if any `lb[i] > ub[i]`.
- `x0` is clipped into the box, so the optimizer starts from a feasible point even if you passed one outside it.

## What the bounds do during the iterations

L-BFGS-B is still a quasi-Newton method: each iteration builds a quadratic model of `fun` from the current gradient and a limited-memory BFGS approximation of the Hessian (the last `maxcor` steps, default 10). The box changes how a step is chosen from that model. One iteration goes roughly like this:

1. **Find which coordinates to freeze.** Follow the steepest-descent direction, but clipped to the box: a coordinate that reaches a bound stops there while the others keep moving. Along this bent path the algorithm finds the first local minimizer of the quadratic model, called the *generalized Cauchy point*. Coordinates sitting on a bound there form the *active set*.
2. **Optimize the free coordinates.** With the active coordinates held fixed, minimize the quadratic model over the remaining coordinates only, then clip the result back into the box if it stepped out.
3. **Line search.** Search along the direction from the current point toward that candidate, using strong Wolfe conditions. The maximum step length is capped so every trial point stays inside the box. This is why `fun` and `jac` are never called at infeasible points.
4. **Update the L-BFGS memory** with the new step and gradient change, as in unconstrained L-BFGS.

If you don't pass `jac`, the gradient comes from finite differences. Those differences also respect the box: when a forward step would leave the box, SciPy uses a backward step instead, so even the probe points are feasible.

## How convergence changes

Without bounds you stop when the gradient is near zero. With bounds, a coordinate pressed against a bound may have a large gradient that points *out* of the box, and that is a perfectly good solution. So L-BFGS-B uses the **projected gradient**: for each coordinate, take the gradient component, but set it to zero if it points outward from a bound the coordinate is sitting on. The stop test is `max_i |projected_gradient[i]| <= gtol` (option name `gtol`, default `1e-5`), alongside the usual relative-decrease test `ftol` and the `maxiter` / `maxfun` limits.

A consequence that catches people: `res.jac` is the *raw* gradient at the solution. Nonzero entries there are expected for coordinates on an active bound; they are not a sign that the optimizer failed.

A small hypothetical example makes this concrete. Minimize `f(x, y) = (x - 3)**2 + (y - 1)**2` with `bounds=[(0, 2), (0.5, 0.5)]`. The unconstrained minimum is `(3, 1)`, which is outside the box. L-BFGS-B returns `x ≈ 2` (the upper bound) and `y = 0.5` (the pinned value). The raw gradient there is `(-2, -1)`, so `res.jac ≈ [-2, -1]`; both components point outward across a bound, so the projected gradient is `(0, 0)` and the run reports success.

## A coordinate with equal bounds

When `lb[i] == ub[i]`, the box has zero width in that direction. The L-BFGS-B code recognizes this directly: in its bookkeeping the variable is classified as "always fixed" rather than as a bound that might become active or inactive. In practice that means:

- `x0[i]` is clipped to the common value before the first iteration, and the coordinate is never moved afterward, so `res.x[i]` equals it exactly.
- The coordinate is excluded from the free set in step 2 of every iteration, so it does not take part in the quasi-Newton update or the line search.
- Its projected-gradient component is always zero, so it never prevents convergence, whatever the raw gradient `res.jac[i]` is.

`fun` and `jac` are still called with the full-length vector, so your code sees the fixed value in place; nothing is removed from the problem dimension. This is a convenient way to fix a parameter without rewriting the objective. The one thing I would check on your SciPy version before relying on it is the finite-difference path: with `jac=None`, the gradient estimate for a zero-width coordinate has no room to step, and I'm not certain every release handles that component cleanly. Passing an explicit `jac` sidesteps the question, and a quick test with a toy function on your install settles it either way.
