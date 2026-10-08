"""Illustrative figures for sections 6.2 and 6.3 of the sparse CTS plan.

Both figures are computed from the formulas in the text with hypothetical
parameter values. They are not measured data.

Run from this folder:
    uv run --offline --no-project --with matplotlib --with numpy python3 make_figures.py
"""
from math import comb

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Figure 1: typical step length versus support size k (section 6.2)
# ---------------------------------------------------------------------------
h = 0.1        # hypothetical half-width of each coordinate displacement
R = 0.45       # hypothetical radius cap for the unit-direction construction
k = np.arange(1, 101)

rms_coord = np.sqrt(k * h**2 / 3)            # sqrt(E||delta||^2) = sqrt(k h^2 / 3)
rms_unit = np.full_like(k, np.sqrt(R**2 / 3), dtype=float)  # sqrt(R^2 / 3) for every k

fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.plot(k, rms_coord, color="#c0392b", lw=2,
        label=r"coordinate-wise: $\sqrt{k h^2/3}$  ($h = 0.1$)")
ax.plot(k, rms_unit, color="#2c3e50", lw=2, ls="--",
        label=r"unit direction: $\sqrt{R^2/3}$  ($R = 0.45$)")
ax.axvline(20, color="grey", lw=0.8, ls=":")
ax.text(21, 0.03, "TuRBO: about 20\ncoordinates move", fontsize=8, color="grey")
ax.set_xlabel("support size $k$ (number of moving coordinates)")
ax.set_ylabel("root-mean-square step length")
ax.set_xlim(1, 100)
ax.set_ylim(0, 0.65)
ax.legend(loc="upper left", fontsize=9, frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("fig_step_vs_k.png", dpi=160)
plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 2: what a random support does to the active subspace (section 6.3)
# ---------------------------------------------------------------------------
d, s = 500, 10            # hypothetical problem size and active-set size
ks = np.unique(np.round(np.logspace(0, np.log10(d), 60)).astype(int))

def p_hit(kk):
    """P(J >= 1) = 1 - C(d-s, kk) / C(d, kk), exact hypergeometric."""
    return 1.0 - comb(d - s, kk) / comb(d, kk)

p = np.array([p_hit(int(kk)) for kk in ks])
mean_energy = np.full_like(p, s / d)          # E||P_A v||^2 = s/d for every k
energy_given_hit = mean_energy / p            # E[||P_A v||^2 | J >= 1]
approx = 1 - np.exp(-ks * s / d)              # small-k, small-s approximation

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 3.8))

ax1.plot(ks, p, color="#2c3e50", lw=2, label="exact hypergeometric")
ax1.plot(ks, approx, color="#c0392b", lw=1.5, ls="--",
         label=r"$1 - e^{-ks/d}$")
ax1.set_xscale("log")
ax1.set_xlabel("support size $k$ (log scale)")
ax1.set_ylabel(r"$P(J \geq 1)$: support touches an active coordinate")
ax1.set_ylim(0, 1.05)
ax1.legend(loc="upper left", fontsize=9, frameon=False)
ax1.set_title("(a) hit probability rises with $k$", fontsize=10)

ax2.plot(ks, energy_given_hit, color="#c0392b", lw=2,
         label=r"given a hit: $\mathbb{E}[\|P_A v\|^2 \mid J \geq 1]$")
ax2.plot(ks, mean_energy, color="#2c3e50", lw=2, ls="--",
         label=r"over all candidates: $\mathbb{E}\|P_A v\|^2 = s/d$")
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_xlabel("support size $k$ (log scale)")
ax2.set_ylabel("fraction of direction energy in active subspace")
ax2.legend(loc="upper right", fontsize=9, frameon=False)
ax2.set_title("(b) energy per hit falls with $k$; the average is flat", fontsize=10)

for ax in (ax1, ax2):
    ax.spines[["top", "right"]].set_visible(False)
fig.suptitle(f"Illustration from the formulas, hypothetical $d = {d}$, $s = {s}$",
             fontsize=10)
fig.tight_layout()
fig.savefig("fig_support_tradeoff.png", dpi=160)
plt.close(fig)
print("wrote fig_step_vs_k.png and fig_support_tradeoff.png")
