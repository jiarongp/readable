"""Illustrative figure for sections 6.2 and 6.3 of the sparse-CTS plan.

Computed from the model equations in the text, not from measured data.
Run:  python3 make_figure.py   ->  writes k_tradeoff.png next to this file.
"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "k_tradeoff.png")

# ---- Panel (a): step length versus support size k (section 6.2) ------------
# Coordinate-wise model: each of k coordinates moves by U(-h, h), so the RMS
# step is h * sqrt(k / 3).  Unit-direction model: ||delta|| = r, r ~ U(0, R),
# so the RMS step is R / sqrt(3) for every k.  Both scales set to 1 here.
h = 1.0
R = 1.0
ks_a = list(range(1, 101))
rms_coordwise = [h * math.sqrt(k / 3.0) for k in ks_a]
rms_unitdir = [R / math.sqrt(3.0) for _ in ks_a]

# ---- Panel (b): hit probability and energy per hit (section 6.3) -----------
# Hypothetical setting: d = 500 coordinates, s = 10 of them active.
d, s = 500, 10


def p_hit(k):
    """P(J >= 1) for hypergeometric J = |S ∩ A|, S a uniform k-subset."""
    # P(J = 0) = C(d - s, k) / C(d, k)
    p0 = math.comb(d - s, k) / math.comb(d, k)
    return 1.0 - p0


ks_b = list(range(1, d + 1))
hit = [p_hit(k) for k in ks_b]
avg_energy = [s / d for _ in ks_b]                      # E||P_A v||^2 = s/d, all k
energy_per_hit = [(s / d) / p for p in hit]             # E[J/k | J >= 1]

# ---- Draw -------------------------------------------------------------------
fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(10, 3.8))

ax_a.plot(ks_a, rms_coordwise, label="coordinate-wise: $h\\sqrt{k/3}$")
ax_a.plot(ks_a, rms_unitdir, label="unit direction: $R/\\sqrt{3}$ (constant)")
ax_a.set_xlabel("support size $k$ (coordinates moved)")
ax_a.set_ylabel("root-mean-square step length")
ax_a.set_title("(a) Step length grows with $k$ only in the\ncoordinate-wise model ($h = R = 1$)")
ax_a.legend(frameon=False)

ax_b.plot(ks_b, hit, label="hit probability $P(J \\geq 1)$")
ax_b.plot(ks_b, energy_per_hit, label="active energy per hit $\\mathbb{E}[J/k \\mid J \\geq 1]$")
ax_b.plot(ks_b, avg_energy, linestyle="--", label="average active energy $s/d$ (all $k$)")
ax_b.set_xscale("log")
ax_b.set_xlabel("support size $k$ (log scale)")
ax_b.set_ylabel("probability or fraction of energy")
ax_b.set_title("(b) Random support, $d = 500$, $s = 10$ active:\nhits get likelier, each hit gets weaker")
ax_b.legend(frameon=False, fontsize=8)

for ax in (ax_a, ax_b):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

fig.tight_layout()
fig.savefig(OUT, dpi=160)
print("wrote", OUT)
