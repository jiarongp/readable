"""Illustrative figures for sections 6.2 and 6.3 of the sparse-CTS plan rewrite.

Both figures are computed from the simplified models stated in the text.
They are illustrations, not measured data.

Figure 1 (step_scale.png): RMS step length against support size k, relative
to k = 1, for the coordinate-wise model (E||delta||^2 = k h^2 / 3) and the
unit-direction construction (||delta|| = r, independent of k).

Figure 2 (active_energy.png): sampled distribution of the active-space
energy ||P_A v||^2 under the isotropic-support model, for a sparse support
(k = 20) and a dense direction (k = d), with hypothetical d = 500, s = 10.
Given the overlap J = j, the energy of an isotropic unit vector on k
coordinates that lands on j of them is Beta(j/2, (k - j)/2); J itself is
hypergeometric. Sampling those two laws is exact for the model.
"""
import math

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = __file__.rsplit("/", 1)[0]
SPARSE = "#d55e00"  # orange
DENSE = "#0072b2"  # blue

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

# ---------------------------------------------------------------- figure 1
k = np.arange(1, 101)
fig, ax = plt.subplots(figsize=(5.2, 3.2))
ax.plot(k, np.sqrt(k), color=SPARSE, lw=2, label=r"coordinate-wise: $\sqrt{k}$")
ax.plot(k, np.ones_like(k, dtype=float), color=DENSE, lw=2, label="unit direction: 1")
ax.axvline(20, color="0.6", lw=1, ls=":")
ax.text(21, 9.3, "k = 20", color="0.4", va="top")
ax.set_xlabel("support size k (coordinates that move)")
ax.set_ylabel("RMS step length, relative to k = 1")
ax.set_xlim(0, 100)
ax.set_ylim(0, 10.5)
ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.25, 1.0))
fig.tight_layout()
fig.savefig(f"{OUT_DIR}/step_scale.png", dpi=160)
plt.close(fig)

# ---------------------------------------------------------------- figure 2
rng = np.random.default_rng(0)
d, s, n = 500, 10, 200_000


def active_energy(k):
    """Sample ||P_A v||^2 for an isotropic direction on a uniform random k-subset."""
    j = rng.hypergeometric(ngood=s, nbad=d - s, nsample=k, size=n)
    e = np.zeros(n)
    for jj in np.unique(j):
        m = j == jj
        if jj == 0:
            continue
        if jj == k:
            e[m] = 1.0
        else:
            e[m] = rng.beta(jj / 2, (k - jj) / 2, size=m.sum())
    return e


sparse = active_energy(20)
dense = active_energy(d)
p_zero = np.mean(sparse == 0)
p_zero_exact = math.comb(d - s, 20) / math.comb(d, 20)

bins = np.arange(0, 0.25 + 1e-9, 0.01)
fig, ax = plt.subplots(figsize=(5.2, 3.4))
ax.hist(dense, bins=bins, weights=np.full(n, 1 / n), color=DENSE, alpha=0.75,
        label=f"dense, k = d = {d}")
ax.hist(sparse[sparse > 0], bins=bins, weights=np.full((sparse > 0).sum(), 1 / n),
        color=SPARSE, alpha=0.75, label="sparse, k = 20 (energy > 0)")
first_bin = np.mean((sparse > 0) & (sparse < 0.01))
ax.bar(0.005, p_zero, bottom=first_bin, width=0.01, color="none", edgecolor=SPARSE,
       hatch="///", lw=1.2, label=f"sparse, exactly 0 ({p_zero:.0%} of candidates)")
ax.axvline(s / d, color="0.3", lw=1, ls="--")
ax.text(s / d + 0.026, 0.56, f"common mean\ns/d = {s / d:.2f}", color="0.3", va="top")
ax.annotate("", xy=(s / d + 0.001, 0.50), xytext=(s / d + 0.025, 0.50), arrowprops=dict(arrowstyle="->", color="0.3", lw=1))
ax.set_xlabel(r"active-space energy $\|P_A v\|^2$ of one candidate")
ax.set_ylabel("fraction of candidates per bin")
ax.set_xlim(0, 0.25)
ax.set_ylim(0, 0.85)
ax.legend(frameon=False, loc="upper right")
fig.tight_layout()
fig.savefig(f"{OUT_DIR}/active_energy.png", dpi=160)
plt.close(fig)

print(f"P(J = 0) for d={d}, s={s}, k=20: exact {p_zero_exact:.4f}, sampled {p_zero:.4f}, "
      f"approx 1 - e^(-ks/d) hit chance {1 - math.exp(-20 * s / d):.4f}")
print(f"mean energy: sparse {sparse.mean():.4f}, dense {dense.mean():.4f}, s/d = {s / d}")
