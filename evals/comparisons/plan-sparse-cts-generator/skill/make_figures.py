#!/usr/bin/env python3
"""Figures for the HTML rewrite of sparse_cts_plan.md sections 6.1-6.3.

Run from this directory:
    uv run --offline --no-project --with matplotlib --with numpy python3 make_figures.py

Writes, for theme in {light, dark}:
    fig1_construction_<theme>.png   geometry of x = c + r v, and k = 1 versus k = d pools in d = 2
    fig2_step_vs_k_<theme>.png      RMS step against k for the two step models of section 6.2
    fig3_random_support_<theme>.png hit probability and active-space energy distribution (section 6.3)

Every number plotted is either an evaluated formula from the plan or a Monte Carlo
sample from the model the plan states. Nothing here is measured optimizer data.
The script also prints the numbers quoted in the text.
"""
import math

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle  # noqa: E402

THEMES = {
    "light": dict(ink="#1B2129", ink2="#5A6472", grid="#D5DBE2", axis="#B8C1CA",
                  s1="#2a78d6", s2="#eb6834", s3="#1baf7a"),
    "dark": dict(ink="#E3E8ED", ink2="#9AA6B2", grid="#2C3540", axis="#3E4A56",
                 s1="#3987e5", s2="#d95926", s3="#199e70"),
}

DPI = 160
SEED = 20261010


def style(t):
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 10.5,
        "text.color": t["ink"],
        "axes.labelcolor": t["ink2"],
        "axes.edgecolor": t["axis"],
        "axes.linewidth": 0.8,
        "axes.facecolor": "none",
        "figure.facecolor": "none",
        "savefig.facecolor": "none",
        "xtick.color": t["ink2"],
        "ytick.color": t["ink2"],
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "grid.color": t["grid"],
        "grid.linewidth": 0.6,
        "axes.grid": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "legend.fontsize": 9.5,
    })


def save(fig, name):
    fig.savefig(name, dpi=DPI, bbox_inches="tight", pad_inches=0.15, transparent=True)
    plt.close(fig)


# ---------------------------------------------------------------- figure 1
def fig1(t, theme):
    rng = np.random.default_rng(SEED)
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(10, 4.6))

    # Left: the construction x = c + r v with a wall and R_max.
    R_max = 1.0
    wall = 0.78
    ax.set_aspect("equal")
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.axis("off")
    ax.axvspan(wall, 1.3, color=t["grid"], alpha=0.6, lw=0)
    ax.plot([wall, wall], [-1.3, 1.3], color=t["ink2"], lw=1.2)
    ax.text(wall + 0.05, 1.12, "wall", color=t["ink2"], fontsize=9.5)
    ax.add_patch(Circle((0, 0), R_max, fill=False, ec=t["ink2"], lw=0.9, ls=(0, (4, 3))))
    ax.text(-0.06, -R_max - 0.14, r"$R_{\max}$", color=t["ink2"], fontsize=10, ha="center")

    ang = math.radians(38)
    v = np.array([math.cos(ang), math.sin(ang)])
    r = 0.8
    x = r * v
    ax.plot([0, x[0]], [0, x[1]], color=t["ink2"], lw=0.9)
    ax.annotate("", xy=0.45 * v, xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=t["s1"], lw=2.0, mutation_scale=14))
    ax.plot(0, 0, "o", color=t["ink"], ms=6)
    ax.plot(x[0], x[1], "o", color=t["s2"], ms=7)
    ax.text(-0.08, -0.14, "c  (incumbent)", color=t["ink"], fontsize=10, ha="right")
    ax.text(0.30, 0.37, "v  (unit direction)", color=t["s1"], fontsize=10, ha="right", va="bottom")
    ax.text(x[0] + 0.06, x[1] - 0.02, "x = c + r v", color=t["ink"], fontsize=10, va="center")
    mid = 0.63 * v
    ax.text(mid[0] + 0.05, mid[1] - 0.08, "r", color=t["ink2"], fontsize=10.5, style="italic")
    ax.set_title("One CTS candidate", color=t["ink"], fontsize=11, loc="left")

    # Right: pools in d = 2 with the same radial law, k = 1 and k = 2 = d.
    bx.set_aspect("equal")
    bx.set_xlim(-1.2, 1.2)
    bx.set_ylim(-1.2, 1.2)
    bx.axis("off")
    bx.add_patch(Circle((0, 0), 1.0, fill=False, ec=t["ink2"], lw=0.9, ls=(0, (4, 3))))
    bx.text(0, -1.14, "R", color=t["ink2"], fontsize=10, ha="center")
    bx.plot(0, 0, "o", color=t["ink"], ms=6)

    n_dense, n_sparse = 220, 120
    th = rng.uniform(0, 2 * math.pi, n_dense)
    rd = rng.uniform(0, 1, n_dense)
    bx.scatter(rd * np.cos(th), rd * np.sin(th), s=16, color=t["s1"], alpha=0.65, lw=0,
               label="k = 2 = d: dense CTS, any direction")
    axis = rng.integers(0, 2, n_sparse)
    sign = rng.choice([-1.0, 1.0], n_sparse)
    rs = rng.uniform(0, 1, n_sparse)
    px = np.where(axis == 0, sign * rs, 0.0)
    py = np.where(axis == 1, sign * rs, 0.0)
    bx.scatter(px, py, s=18, color=t["s2"], alpha=0.9, lw=0,
               label="k = 1: coordinate-like, along an axis")
    bx.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=1, handletextpad=0.4)
    bx.set_title("Two pools, same radial law r ~ U(0, R)", color=t["ink"], fontsize=11, loc="left")

    save(fig, f"fig1_construction_{theme}.png")


# ---------------------------------------------------------------- figure 2
def fig2(t, theme):
    k = np.arange(1, 101)
    unit = np.ones_like(k, dtype=float)
    indep = np.sqrt(k)
    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.grid(axis="y")
    ax.axvline(20, color=t["grid"], lw=1.0)
    ax.plot(k, indep, color=t["s2"], lw=2.0, label="independent coordinates, each U(−h, h): grows like √k")
    ax.plot(k, unit, color=t["s1"], lw=2.0, label="unit direction, ‖δ‖ = r: the same for every k")
    ax.plot([20], [math.sqrt(20)], "o", color=t["s2"], ms=7)
    ax.plot([20], [1.0], "o", color=t["s1"], ms=7)
    ax.annotate(f"k = 20: √20 ≈ {math.sqrt(20):.1f}×", xy=(20, math.sqrt(20)), xytext=(26, math.sqrt(20) + 0.25),
                color=t["ink"], fontsize=9.5)
    ax.annotate("k = 20: 1×", xy=(20, 1.0), xytext=(26, 1.45), color=t["ink"], fontsize=9.5)
    ax.text(100, indep[-1] + 0.25, "grows like √k", color=t["ink"], ha="right", fontsize=9.5)
    ax.text(100, 1.0 + 0.25, "constant", color=t["ink"], ha="right", fontsize=9.5)
    ax.set_xlabel("support size k (number of coordinates that move)")
    ax.set_ylabel("RMS step, relative to k = 1")
    ax.set_xlim(0, 102)
    ax.set_ylim(0, 11)
    ax.legend(loc="upper left")
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(t["axis"])
    save(fig, f"fig2_step_vs_k_{theme}.png")


# ---------------------------------------------------------------- figure 3
def p_j0_exact(d, s, k):
    """P(J = 0): a uniform k-subset of d misses all s active coordinates."""
    if k > d - s:
        return 0.0
    return math.comb(d - s, k) / math.comb(d, k)


def simulate_active_energy(d, s, k, n, rng):
    """||P_A v|| for v isotropic on a uniform random k-support; A = first s coordinates."""
    out = np.empty(n)
    for i in range(n):
        S = rng.choice(d, size=k, replace=False)
        g = rng.standard_normal(k)
        g /= np.linalg.norm(g)
        active = S < s
        out[i] = math.sqrt(float(np.sum(g[active] ** 2)))
    return out


def fig3(t, theme, numbers):
    d, s = 500, 10
    rng = np.random.default_rng(SEED + 1)
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(10, 4.4))

    # Left: probability of touching at least one active coordinate.
    ks = np.arange(1, 501)
    exact = np.array([1.0 - p_j0_exact(d, s, k) for k in ks])
    approx = 1.0 - np.exp(-ks * s / d)
    ax.grid(axis="y")
    ax.set_xscale("log")
    ax.plot(ks, approx, color=t["ink2"], lw=1.2, label="approximation 1 − exp(−ks/d)")
    ax.plot(ks, exact, color=t["s3"], lw=2.0, label="exact hypergeometric P(J ≥ 1)")
    p20 = 1.0 - p_j0_exact(d, s, 20)
    ax.plot([20], [p20], "o", color=t["s3"], ms=7)
    ax.annotate(f"k = 20: P(J ≥ 1) ≈ {p20:.2f}", xy=(20, p20), xytext=(3.2, 0.62), color=t["ink"], fontsize=9.5,
                arrowprops=dict(arrowstyle="-", color=t["axis"], lw=0.8))
    ax.set_xlabel("support size k (log scale)")
    ax.set_ylabel("P(support touches an active coordinate)")
    ax.set_ylim(0, 1.05)
    ax.set_xticks([1, 10, 20, 100, 500])
    ax.set_xticklabels(["1", "10", "20", "100", "500"])
    ax.legend(loc="lower right")
    ax.set_title(f"d = {d}, s = {s}", color=t["ink"], fontsize=11, loc="left")

    # Right: distribution of the active-space energy ||P_A v||.
    n = 40000
    D20 = simulate_active_energy(d, s, 20, n, rng)
    D500 = simulate_active_energy(d, s, 500, n, rng)
    ts = np.linspace(0, 0.6, 400)
    surv20 = np.array([(D20 > u).mean() for u in ts])
    surv500 = np.array([(D500 > u).mean() for u in ts])
    shared = math.sqrt(s / d)
    bx.grid(axis="y")
    bx.axvline(shared, color=t["grid"], lw=1.0)
    bx.text(shared + 0.012, 0.76, f"√(s/d) ≈ {shared:.2f}\nroot of the shared\nmean of ‖P_A v‖²",
            color=t["ink2"], fontsize=8.8, va="top")
    bx.plot(ts, surv500, color=t["s1"], lw=2.0, label="k = 500 (dense): every candidate near 0.14")
    bx.plot(ts, surv20, color=t["s2"], lw=2.0, label="k = 20 (sparse): most at zero, the rest larger")
    bx.annotate(f"{surv20[0]*100:.0f}% of sparse\ncandidates have\n‖P_A v‖ > 0", xy=(0.0, surv20[0]),
                xytext=(0.24, 0.36), color=t["ink"], fontsize=9.3,
                arrowprops=dict(arrowstyle="-", color=t["axis"], lw=0.8))
    bx.set_xlabel("threshold u for the active-space energy ‖P_A v‖")
    bx.set_ylabel("fraction of candidates with ‖P_A v‖ > u")
    bx.set_xlim(0, 0.6)
    bx.set_ylim(0, 1.05)
    bx.legend(loc="upper right")
    bx.set_title(f"{n:,} simulated directions per k", color=t["ink"], fontsize=11, loc="left")
    save(fig, f"fig3_random_support_{theme}.png")

    if theme == "light":
        numbers["P(J=0), d=500 s=10 k=20 exact"] = p_j0_exact(d, s, 20)
        numbers["P(J>=1) exact"] = p20
        numbers["P(J>=1) approx 1-exp(-ks/d)"] = 1 - math.exp(-20 * s / d)
        numbers["E[J] = ks/d"] = 20 * s / d
        numbers["mean ||P_A v||^2, k=20 (sim)"] = float((D20 ** 2).mean())
        numbers["mean ||P_A v||^2, k=500 (sim)"] = float((D500 ** 2).mean())
        numbers["s/d"] = s / d
        numbers["P(||P_A v|| > 0.2), k=20 (sim)"] = float((D20 > 0.2).mean())
        numbers["P(||P_A v|| > 0.2), k=500 (sim)"] = float((D500 > 0.2).mean())
        numbers["99th pct ||P_A v||, k=20 (sim)"] = float(np.quantile(D20, 0.99))
        numbers["99th pct ||P_A v||, k=500 (sim)"] = float(np.quantile(D500, 0.99))
        numbers["1/sqrt(d)"] = 1 / math.sqrt(d)
        numbers["1/sqrt(20)"] = 1 / math.sqrt(20)


if __name__ == "__main__":
    numbers = {}
    for theme, t in THEMES.items():
        style(t)
        fig1(t, theme)
        fig2(t, theme)
        fig3(t, theme, numbers)
    print("Numbers quoted in the text:")
    for key, val in numbers.items():
        print(f"  {key}: {val:.4f}")
    print("RMS step, independent-coordinate model, h = 0.1: k=1 -> %.4f, k=20 -> %.4f"
          % (0.1 / math.sqrt(3), math.sqrt(20 / 3) * 0.1))
    print("mean squared step, unit direction, R = 0.5: %.4f (RMS %.4f)" % (0.25 / 3, math.sqrt(0.25 / 3)))
