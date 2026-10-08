"""Illustrative figures for the rewritten sections 6.1-6.3.

Both figures plot closed-form expressions from the text with hypothetical
parameter values. They are illustrations, not measured data.

Run:  uv run --offline --with matplotlib python make_figures.py
  or: python3 make_figures.py   (needs matplotlib installed)
"""

from math import comb, exp, sqrt
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Figure 1: typical step length against support size k (section 6.2).
# Coordinate-wise model: E||delta||^2 = k h^2 / 3  ->  RMS step = h sqrt(k/3).
# Unit-direction model: ||delta|| = r, r ~ U(0, R) -> RMS step = R / sqrt(3).
# Hypothetical scale: h = R = 1.
# ---------------------------------------------------------------------------
d = 500
ks = list(range(1, d + 1))
h = R = 1.0
rms_coord = [h * sqrt(k / 3.0) for k in ks]
rms_unit = [R / sqrt(3.0) for _ in ks]

fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.plot(ks, rms_coord, color="#c0392b", lw=2,
        label=r"coordinate-wise: $h\sqrt{k/3}$ (grows like $\sqrt{k}$)")
ax.plot(ks, rms_unit, color="#2c3e50", lw=2, ls="--",
        label=r"unit direction: $R/\sqrt{3}$ (constant in $k$)")
ax.axvline(20, color="grey", lw=1, ls=":")
ax.text(21, max(rms_coord) * 0.55, "k = 20 (TuRBO default)", color="grey",
        fontsize=9, va="top")
ax.set_xscale("log")
ax.set_xlabel("support size $k$ (log scale)")
ax.set_ylabel("RMS step length  (units of $h = R$)")
ax.set_title("Step length against support size, hypothetical $h = R = 1$")
ax.legend(loc="upper left", fontsize=9)
ax.grid(alpha=0.3, which="both")
fig.tight_layout()
fig.savefig(OUT / "fig_step_vs_k.png", dpi=150)
plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 2: hit probability and per-hit concentration against k (section 6.3).
# Hit probability: exact hypergeometric P(J >= 1) = 1 - C(d-s, k) / C(d, k),
# with the approximation 1 - exp(-k s / d) shown for comparison.
# Per-hit active component: about 1/sqrt(k); dense reference 1/sqrt(d).
# Hypothetical: d = 500 (from the text), s = 10 (chosen for illustration).
# ---------------------------------------------------------------------------
s = 10


def p_hit_exact(k: int) -> float:
    if k > d - s:
        return 1.0
    return 1.0 - comb(d - s, k) / comb(d, k)


p_exact = [p_hit_exact(k) for k in ks]
p_approx = [1.0 - exp(-k * s / d) for k in ks]
per_hit = [1.0 / sqrt(k) for k in ks]

fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.plot(ks, p_exact, color="#1f77b4", lw=2,
        label=r"hit probability $P(J \geq 1)$, exact hypergeometric")
ax.plot(ks, p_approx, color="#1f77b4", lw=1, ls=":",
        label=r"approximation $1 - e^{-ks/d}$")
ax.plot(ks, per_hit, color="#c0392b", lw=2,
        label=r"active component per hit, about $1/\sqrt{k}$")
ax.axhline(1.0 / sqrt(d), color="#c0392b", lw=1, ls="--",
           label=r"dense direction: every candidate about $1/\sqrt{d}$")
ax.axvline(20, color="grey", lw=1, ls=":")
ax.text(21, 0.98, "k = 20", color="grey", fontsize=9, va="top")
ax.set_xscale("log")
ax.set_xlabel("support size $k$ (log scale)")
ax.set_ylabel("value (both quantities lie in [0, 1])")
ax.set_title(f"Hit probability and per-hit concentration, hypothetical d = {d}, s = {s}")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=8,
          frameon=False)
ax.grid(alpha=0.3, which="both")
fig.tight_layout()
fig.savefig(OUT / "fig_hit_vs_concentration.png", dpi=150, bbox_inches="tight")
plt.close(fig)

print("wrote", OUT / "fig_step_vs_k.png")
print("wrote", OUT / "fig_hit_vs_concentration.png")
