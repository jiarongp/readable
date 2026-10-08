"""Illustrative figures for sections 6.2 and 6.3 of the sparse-CTS plan.

Both figures are computed from the formulas in the text with hypothetical
parameter values; neither shows measured data.

Run:  python3 make_figures.py
Writes fig_step_vs_k.png and fig_hit_tradeoff.png next to this script.
"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Figure 1 (section 6.2): root-mean-square step length against support size k
# ---------------------------------------------------------------------------
h = 1.0   # half-width of the per-coordinate uniform displacement U(-h, h)
R = 1.0   # radius cap of the unit-direction construction, r ~ U(0, R)
ks = list(range(1, 101))
rms_coordinatewise = [math.sqrt(k * h * h / 3.0) for k in ks]   # sqrt(E||delta||^2) = h sqrt(k/3)
rms_unit_direction = [math.sqrt(R * R / 3.0) for _ in ks]       # sqrt(E r^2) = R / sqrt(3)

fig, ax = plt.subplots(figsize=(6.0, 3.6))
ax.plot(ks, rms_coordinatewise, color="#1f5f8b", lw=2,
        label=r"coordinate-wise model: $h\sqrt{k/3}$  (h = 1)")
ax.plot(ks, rms_unit_direction, color="#c0392b", lw=2, ls="--",
        label=r"unit-direction construction: $R/\sqrt{3}$  (R = 1)")
ax.set_xlabel("support size $k$ (number of moving coordinates)")
ax.set_ylabel("root-mean-square step length")
ax.set_title("Step length against $k$ for the two constructions")
ax.grid(alpha=0.3)
ax.legend(loc="upper left", frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_step_vs_k.png"), dpi=150)
plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 2 (section 6.3): hit probability versus energy per hit, d = 500, s = 5
# ---------------------------------------------------------------------------
d, s = 500, 5


def p_hit(k):
    """P(J >= 1) for hypergeometric J = |S ∩ A|, |S| = k, |A| = s, in d dims."""
    return 1.0 - math.comb(d - s, k) / math.comb(d, k)


ks2 = list(range(1, d + 1))
hit = [p_hit(k) for k in ks2]
avg_energy = s / d                                   # E||P_A v||^2, every k
energy_per_hit = [avg_energy / p for p in hit]       # E[||P_A v||^2 | J >= 1]
flat = [avg_energy for _ in ks2]

fig, ax = plt.subplots(figsize=(6.0, 3.8))
ax.plot(ks2, hit, color="#1f5f8b", lw=2, label=r"hit probability $P(J \geq 1)$")
ax.plot(ks2, energy_per_hit, color="#c0392b", lw=2,
        label=r"mean active-space energy given a hit")
ax.plot(ks2, flat, color="#555555", lw=1.5, ls=":",
        label=r"product = $s/d$ (same for every $k$)")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("support size $k$ (log scale)")
ax.set_ylabel("value (log scale)")
ax.set_title("Hit probability and energy per hit, $d = 500$, $s = 5$ (hypothetical)")
ax.grid(alpha=0.3, which="both")
ax.legend(loc="center right", frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_hit_tradeoff.png"), dpi=150)
plt.close(fig)

print("wrote fig_step_vs_k.png and fig_hit_tradeoff.png")
