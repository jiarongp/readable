"""Illustrative figures for sections 6.2 and 6.3 of the sparse-CTS plan.

Both figures plot closed-form quantities from the simplified models in the
text; they are illustrations, not measured data.

Figure 1 (step_length_vs_k.png): root-mean-square step length against the
support size k for the coordinate-wise model (h * sqrt(k / 3)) and the
unit-direction model (R / sqrt(3)), with the hypothetical choice h = R = 1.

Figure 2 (support_hit_vs_k.png): for d = 500 and a hypothetical active set
of size s = 10, the probability that a uniformly random k-subset touches at
least one active coordinate (exact hypergeometric, with the 1 - exp(-ks/d)
approximation), and the typical active component per hit, about 1/sqrt(k),
against the dense value 1/sqrt(d).
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from math import comb

BLUE = "#2a78d6"    # categorical slot 1
ORANGE = "#eb6834"  # categorical slot 2
INK = "#1a1a19"
MUTED = "#6b6a63"
GRID = "#e6e5e0"
SURFACE = "#fcfcfb"

plt.rcParams.update({
    "font.size": 10,
    "axes.edgecolor": MUTED,
    "axes.labelcolor": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "text.color": INK,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
})


def style(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


# ---------------------------------------------------------------- figure 1
k = np.arange(1, 51)
h = 1.0  # hypothetical half-width of the per-coordinate displacement
R = 1.0  # hypothetical radius cap

rms_coord = h * np.sqrt(k / 3.0)
rms_unit = np.full_like(k, R / np.sqrt(3.0), dtype=float)

fig, ax = plt.subplots(figsize=(6.4, 3.6))
ax.plot(k, rms_coord, color=ORANGE, linewidth=2)
ax.plot(k, rms_unit, color=BLUE, linewidth=2)
ax.text(50.8, rms_coord[-1], "coordinate-wise\n(RAASP-like):  $h\\sqrt{k/3}$",
        color=INK, va="center", ha="left", fontsize=9)
ax.text(50.8, rms_unit[-1], "unit-direction\n(sparse CTS):  $R/\\sqrt{3}$",
        color=INK, va="center", ha="left", fontsize=9)
ax.axvline(20, color=GRID, linewidth=1)
ax.text(20.5, 3.9, "k = 20", color=MUTED, fontsize=8.5, va="top")
ax.set_xlabel("support size $k$ (number of perturbed coordinates)")
ax.set_ylabel("root-mean-square step length\n(units of $h = R = 1$)")
ax.set_xlim(0, 50)
ax.set_ylim(0, 4.2)
style(ax)
fig.subplots_adjust(left=0.14, right=0.72, bottom=0.17, top=0.95)
fig.savefig("step_length_vs_k.png", dpi=160)
plt.close(fig)

# ---------------------------------------------------------------- figure 2
d = 500
s = 10  # hypothetical active-set size
k = np.arange(1, 101)


def p_hit_exact(kk):
    return 1.0 - comb(d - s, kk) / comb(d, kk)


p_exact = np.array([p_hit_exact(int(kk)) for kk in k])
p_approx = 1.0 - np.exp(-k * s / d)
per_hit = 1.0 / np.sqrt(k)
dense = 1.0 / np.sqrt(d)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.0, 3.6))

ax1.plot(k, p_exact, color=BLUE, linewidth=2)
ax1.plot(k, p_approx, color=BLUE, linewidth=1.2, linestyle=(0, (3, 3)))
ax1.text(22, 0.80, "exact (hypergeometric)", color=INK, fontsize=8.5,
         ha="left", va="bottom")
ax1.text(62, 0.58, "approximation $1 - e^{-ks/d}$", color=MUTED,
         fontsize=8.5, ha="left", va="top")
ax1.axvline(20, color=GRID, linewidth=1)
ax1.text(20.5, 0.98, "k = 20", color=MUTED, fontsize=8.5, va="top")
ax1.set_xlabel("support size $k$")
ax1.set_ylabel("probability the support touches\nat least one active coordinate")
ax1.set_xlim(0, 100)
ax1.set_ylim(0, 1.0)
ax1.set_title("(a) hit probability rises with $k$", fontsize=10, loc="left")
style(ax1)

ax2.plot(k, per_hit, color=BLUE, linewidth=2)
ax2.axhline(dense, color=MUTED, linewidth=1.2, linestyle=(0, (3, 3)))
ax2.text(24, 0.30, "sparse, per hit: $\\approx 1/\\sqrt{k}$",
         color=INK, fontsize=8.5, ha="left", va="bottom")
ax2.text(24, dense + 0.02, "dense, every candidate: $\\approx 1/\\sqrt{d}$",
         color=INK, fontsize=8.5, ha="left", va="bottom")
ax2.axvline(20, color=GRID, linewidth=1)
ax2.text(20.5, 0.98, "k = 20", color=MUTED, fontsize=8.5, va="top")
ax2.set_xlabel("support size $k$")
ax2.set_ylabel("typical active component of $v$")
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 1.0)
ax2.set_title("(b) size per hit falls with $k$", fontsize=10, loc="left")
style(ax2)

fig.subplots_adjust(left=0.09, right=0.98, bottom=0.17, top=0.9, wspace=0.45)
fig.savefig("support_hit_vs_k.png", dpi=160)
plt.close(fig)

print("k=20: exact P(J>=1) = %.3f, approx = %.3f, E[J] = %.2f, 1/sqrt(k) = %.3f, 1/sqrt(d) = %.3f"
      % (p_hit_exact(20), 1 - np.exp(-20 * s / d), 20 * s / d, 1 / np.sqrt(20), dense))
