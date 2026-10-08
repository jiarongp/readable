"""Illustration for section 6.3: hit probability versus energy per hit.

Hypothetical parameters: d = 500 coordinates, s = 10 active coordinates.
The curves are computed from the hypergeometric formulas in the text,
not measured from an optimizer run.
"""
from math import comb, exp

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

d, s = 500, 10
ks = np.arange(1, d + 1)

# Exact P(J >= 1) = 1 - C(d-s, k) / C(d, k), and the small-k, small-s approximation.
p_hit = np.array([1 - comb(d - s, k) / comb(d, k) for k in ks])
p_hit_approx = np.array([1 - exp(-k * s / d) for k in ks])

# Mean active-space energy per candidate is s/d for every k (FACT under isotropy).
# Conditional on hitting at least one active coordinate it is (s/d) / P(J >= 1).
energy_all = np.full_like(p_hit, s / d)
energy_per_hit = (s / d) / p_hit

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 3.7), constrained_layout=True)

c_hit, c_energy, c_ref = "#1f77b4", "#d62728", "#7f7f7f"

ax1.plot(ks, p_hit, color=c_hit, lw=2, label=r"exact $P(J \geq 1)$")
ax1.plot(ks, p_hit_approx, color=c_hit, lw=1.2, ls="--", label=r"$1 - e^{-ks/d}$")
ax1.set_xscale("log")
ax1.set_ylim(0, 1.02)
ax1.set_xlabel(r"support size $k$")
ax1.set_ylabel("probability the support touches $A$")
ax1.set_title("(a) Hit probability rises with $k$", fontsize=10)
ax1.legend(frameon=False, fontsize=9, loc="upper left")

ax2.plot(ks, energy_per_hit, color=c_energy, lw=2,
         label=r"mean $\|P_A v\|^2$ given a hit ($J \geq 1$)")
ax2.plot(ks, energy_all, color=c_energy, lw=1.2, ls="--",
         label=r"mean $\|P_A v\|^2$ over all candidates $= s/d$")
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_xlabel(r"support size $k$")
ax2.set_ylabel("fraction of direction energy on $A$")
ax2.set_title("(b) Energy per hit falls with $k$; the average does not", fontsize=10)
ax2.legend(frameon=False, fontsize=9, loc="upper right")

for ax in (ax1, ax2):
    ax.axvline(20, color=c_ref, lw=0.8, ls=":")
    ax.text(20, ax.get_ylim()[1], " $k=20$", color=c_ref, fontsize=8, va="top", ha="left")
    ax.spines[["top", "right"]].set_visible(False)

fig.suptitle(r"Random $k$-subset support, $d=500$, $s=10$ (hypothetical values)", fontsize=10)
fig.savefig("support_tradeoff.png", dpi=150)
print("P(J>=1) at k=1,20,100:", [round(float(p_hit[k - 1]), 3) for k in (1, 20, 100)])
print("energy per hit at k=20:", round(float(energy_per_hit[19]), 4), " 1/k =", 1 / 20)
