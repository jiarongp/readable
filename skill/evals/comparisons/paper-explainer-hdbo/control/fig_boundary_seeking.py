"""Toy 1-D illustration of Theorem 1 of Doumont et al. (2025) and of why the
spherical projection escapes it.

Both panels use the SAME four synthetic observations and the SAME Bayesian
linear regression machinery (Gaussian prior on weights, Gaussian noise).
Left: features phi(x) = [1, x]  -> standard linear kernel.
Right: features phi(x) = [1, P(x)] with P the inverse stereographic
projection of Eq. (4), P(x) = [2x, x^2 - 1] / (x^2 + 1).

This is our own toy computation to illustrate the mechanism; it is not a
figure from the paper. Run with:
  uv run --offline --no-project --with matplotlib --with numpy python3 fig_boundary_seeking.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from math import erf, sqrt, exp, pi

# ---- synthetic data on the centred domain [-1, 1] ---------------------------
X = np.array([-0.7, -0.3, 0.2, 0.6])
Y = np.array([-0.35, 0.05, 0.45, 0.55])
NOISE_VAR = 0.02 ** 2
PRIOR_VAR = 1.0
grid = np.linspace(-1, 1, 801)


def feats_linear(x):
    x = np.atleast_1d(x)
    return np.stack([np.ones_like(x), x], axis=1)


def feats_sphere(x):
    x = np.atleast_1d(x)
    d = x ** 2 + 1
    return np.stack([np.ones_like(x), 2 * x / d, (x ** 2 - 1) / d], axis=1)


def posterior(feats):
    Phi = feats(X)
    A = Phi.T @ Phi / NOISE_VAR + np.eye(Phi.shape[1]) / PRIOR_VAR
    S = np.linalg.inv(A)
    m = S @ Phi.T @ Y / NOISE_VAR
    Pg = feats(grid)
    mu = Pg @ m
    var = np.einsum("ij,jk,ik->i", Pg, S, Pg)
    return mu, np.sqrt(np.maximum(var, 1e-12))


def norm_cdf(z):
    return 0.5 * (1 + np.vectorize(erf)(z / sqrt(2)))


def norm_pdf(z):
    return np.exp(-0.5 * z ** 2) / sqrt(2 * pi)


def expected_improvement(mu, sd, best):
    z = (mu - best) / sd
    return (mu - best) * norm_cdf(z) + sd * norm_pdf(z)


fig, axes = plt.subplots(2, 2, figsize=(9, 5.6), sharex=True,
                         gridspec_kw={"height_ratios": [2, 1.2]})
titles = ["Standard linear kernel (features [1, x])",
          "Spherical linear kernel (features [1, P(x)])"]
for col, (feats, title) in enumerate(zip([feats_linear, feats_sphere], titles)):
    mu, sd = posterior(feats)
    ei = expected_improvement(mu, sd, Y.max())
    xstar = grid[np.argmax(ei)]

    ax = axes[0, col]
    ax.fill_between(grid, mu - 2 * sd, mu + 2 * sd, color="#9ecae1", alpha=0.6,
                    label="posterior mean ± 2 sd")
    ax.plot(grid, mu, color="#08519c", lw=1.8)
    ax.scatter(X, Y, color="black", zorder=5, s=28, label="observations")
    ax.axvline(xstar, color="#d62728", ls="--", lw=1.2)
    ax.set_title(title, fontsize=10.5)
    ax.set_ylabel("f(x)")
    ax.set_ylim(-1.3, 1.6)
    if col == 0:
        ax.legend(loc="upper left", fontsize=8.5, frameon=False)

    ax = axes[1, col]
    ax.plot(grid, ei, color="#d62728", lw=1.8)
    ax.axvline(xstar, color="#d62728", ls="--", lw=1.2)
    ax.annotate(f"argmax EI at x = {xstar:+.2f}", xy=(xstar, ei.max()),
                xytext=(0.0 if col == 0 else 0.22, 0.85),
                textcoords="axes fraction", fontsize=9,
                ha="left" if col == 0 else "center",
                arrowprops=dict(arrowstyle="->", color="#555"))
    ax.set_ylabel("EI(x)")
    ax.set_xlabel("x  (search space [-1, 1])")
    ax.set_xlim(-1, 1)
    ax.set_ylim(bottom=0)

fig.suptitle("Toy illustration (our computation, not from the paper): the same four points, "
             "two Bayesian linear models", fontsize=10, y=0.995)
fig.tight_layout()
fig.savefig("fig_boundary_seeking.png", dpi=160)
print("argmax summary written; done")
