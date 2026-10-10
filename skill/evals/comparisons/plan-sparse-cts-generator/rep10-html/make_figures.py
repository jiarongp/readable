"""Figures for the Sparse CTS Generator page.

Both figures are illustrations with hypothetical parameter values, not
measured data. Each is rendered twice, for a light and a dark page theme.

  fig_step_vs_k_{light,dark}.png    Section 6.2: typical step length against k
                                    for the coordinate-wise model and the
                                    unit-direction construction.
  fig_active_support_{light,dark}.png
                                    Section 6.3: probability that a random
                                    k-support touches the active set, and the
                                    distribution of the active-space component
                                    of a unit direction for sparse vs dense k.

Run from this directory:
  uv run --offline --no-project --with matplotlib --with numpy python3 make_figures.py
"""

import math

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Palette: dataviz reference instance (categorical slots 1 and 2, chrome and ink).
THEMES = {
    "light": dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781",
                  grid="#e1e0d9", axis="#c3c2b7", s1="#2a78d6", s2="#eb6834"),
    "dark": dict(surface="#1a1a19", ink="#f0efec", ink2="#c3c2b7", muted="#898781",
                 grid="#2c2c2a", axis="#383835", s1="#3987e5", s2="#d95926"),
}

# Hypothetical parameters, shared by both figures where they apply.
D = 500          # ambient dimension
S = 10           # size of the active set A (analysis-only toy objective)
K_SPARSE = 20    # the TuRBO/RAASP count, used here as the sparse support size
H = 1.0          # half-width of the per-coordinate uniform displacement, U(-h, h)
R = 1.0          # radius cap of the unit-direction construction, r ~ U(0, R)
DPI = 200
RNG = np.random.default_rng(20261008)


def style(ax, t):
    ax.set_facecolor(t["surface"])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(t["axis"])
    ax.tick_params(colors=t["muted"], labelsize=9, length=3)
    ax.xaxis.label.set_color(t["ink2"])
    ax.yaxis.label.set_color(t["ink2"])
    ax.grid(True, color=t["grid"], linewidth=0.8)
    ax.set_axisbelow(True)


def hit_probability_exact(k, d=D, s=S):
    """P(J >= 1) for hypergeometric J = |S ∩ A| with |S| = k, |A| = s."""
    return 1.0 - math.comb(d - s, k) / math.comb(d, k)


def hit_probability_approx(k, d=D, s=S):
    return 1.0 - math.exp(-k * s / d)


def active_component_samples(k, n, d=D, s=S):
    """||P_A v|| for v isotropic on a uniformly random k-subset S.

    The active set A is taken as the first s coordinates (the objective is
    axis-aligned, so which coordinates are active does not matter).
    """
    out = np.empty(n)
    for i in range(n):
        support = RNG.choice(d, size=k, replace=False)
        g = RNG.standard_normal(k)
        v = g / np.linalg.norm(g)
        active = support < s
        out[i] = np.sqrt(np.sum(v[active] ** 2))
    return out


def figure_step_vs_k(t, path):
    k = np.arange(1, D + 1)
    rms_coord = np.sqrt(k * H**2 / 3)          # coordinate-wise model, E||δ||² = k h²/3
    rms_unit = np.full_like(k, np.sqrt(R**2 / 3), dtype=float)   # unit direction, R²/3

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=DPI)
    fig.patch.set_facecolor(t["surface"])
    style(ax, t)

    ax.plot(k, rms_coord, color=t["s2"], linewidth=2)
    ax.plot(k, rms_unit, color=t["s1"], linewidth=2)
    ax.plot([K_SPARSE], [math.sqrt(K_SPARSE * H**2 / 3)], "o", color=t["s2"],
            markersize=7, markeredgecolor=t["surface"], markeredgewidth=1.5)

    ax.set_xscale("log")
    ax.set_xlim(1, D)
    ax.set_xticks([1, 2, 5, 10, 20, 50, 100, 200, 500])
    ax.set_xticklabels(["1", "2", "5", "10", "20", "50", "100", "200", "500"])
    ax.set_ylim(0, 14)
    ax.set_xlabel("k, number of perturbed coordinates (log scale)")
    ax.set_ylabel("typical step length, (E‖δ‖²)^½")

    ax.text(D, rms_coord[-1], "  coordinate-wise\n  δᵢ ~ U(−h, h), h = 1",
            color=t["ink"], fontsize=9.5, va="center", ha="left")
    ax.text(D, rms_unit[-1], "  unit direction\n  r ~ U(0, R), R = 1",
            color=t["ink"], fontsize=9.5, va="center", ha="left")
    ax.annotate(f"k = 20: step ≈ {math.sqrt(K_SPARSE / 3):.2f} h",
                xy=(K_SPARSE, math.sqrt(K_SPARSE / 3)), xytext=(6, 5.2),
                color=t["ink2"], fontsize=9.5,
                arrowprops=dict(arrowstyle="-", color=t["muted"], linewidth=0.8))
    fig.subplots_adjust(left=0.09, right=0.78, top=0.95, bottom=0.14)
    fig.savefig(path, dpi=DPI, facecolor=t["surface"])
    plt.close(fig)


def figure_active_support(t, path, samples):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.2), dpi=DPI)
    fig.patch.set_facecolor(t["surface"])
    for ax in (ax1, ax2):
        style(ax, t)

    # Left: probability that the support touches at least one active coordinate.
    k = np.arange(1, D + 1)
    p_exact = np.array([hit_probability_exact(int(kk)) for kk in k])
    p_approx = np.array([hit_probability_approx(int(kk)) for kk in k])
    ax1.plot(k, p_approx, color=t["s1"], linewidth=1.4, linestyle=(0, (4, 3)))
    ax1.plot(k, p_exact, color=t["s1"], linewidth=2)
    p20 = hit_probability_exact(K_SPARSE)
    ax1.plot([K_SPARSE], [p20], "o", color=t["s1"], markersize=7,
             markeredgecolor=t["surface"], markeredgewidth=1.5)
    ax1.annotate(f"k = 20: P ≈ {p20:.2f}", xy=(K_SPARSE, p20), xytext=(28, 0.17),
                 color=t["ink2"], fontsize=9.5,
                 arrowprops=dict(arrowstyle="-", color=t["muted"], linewidth=0.8))
    ax1.text(1.15, 0.42, "solid: exact hypergeometric\ndashed: 1 − e^(−ks/d)",
             color=t["ink2"], fontsize=9, va="top")
    ax1.set_xscale("log")
    ax1.set_xlim(1, D)
    ax1.set_xticks([1, 5, 20, 100, 500])
    ax1.set_xticklabels(["1", "5", "20", "100", "500"])
    ax1.set_ylim(0, 1.02)
    ax1.set_xlabel("k, support size (log scale)")
    ax1.set_ylabel("P(J ≥ 1): support touches A")
    ax1.set_title(f"Hit probability, d = {D}, s = {S}", color=t["ink"], fontsize=10.5, loc="left")

    # Right: distribution of the active-space component ||P_A v||.
    bins = np.arange(0, 0.52, 0.02)
    for key, color, label in ((K_SPARSE, t["s2"], f"sparse, k = {K_SPARSE}"),
                              (D, t["s1"], f"dense, k = d = {D}")):
        x = samples[key]
        ax2.hist(x, bins=bins, weights=np.full_like(x, 1 / len(x)),
                 histtype="stepfilled", color=color, alpha=0.28, edgecolor="none")
        ax2.hist(x, bins=bins, weights=np.full_like(x, 1 / len(x)),
                 histtype="step", color=color, linewidth=2)
    zero_mass = np.mean(samples[K_SPARSE] == 0)
    ax2.text(0.03, zero_mass * 0.98, f" {zero_mass:.0%} of sparse\n candidates: none",
             color=t["ink"], fontsize=9, va="top")
    ax2.text(0.20, 0.30, "dense\n(all near √(s/d) ≈ 0.14)", color=t["ink"], fontsize=9,
             ha="left", va="center")
    ax2.annotate("sparse hits, spread\naround 1/√k ≈ 0.22", xy=(0.25, 0.022), xytext=(0.28, 0.12),
                 color=t["ink"], fontsize=9, ha="left", va="center",
                 arrowprops=dict(arrowstyle="-", color=t["muted"], linewidth=0.8))
    ax2.set_xlim(0, 0.5)
    ax2.set_ylim(0, 0.75)
    ax2.set_xlabel("‖P_A v‖, active-space component")
    ax2.set_ylabel("fraction of candidates")
    ax2.set_title("Where the direction's energy lands", color=t["ink"], fontsize=10.5, loc="left")
    fig.subplots_adjust(left=0.08, right=0.985, top=0.9, bottom=0.15, wspace=0.3)
    fig.savefig(path, dpi=DPI, facecolor=t["surface"])
    plt.close(fig)


if __name__ == "__main__":
    n = 20000
    samples = {K_SPARSE: active_component_samples(K_SPARSE, n),
               D: active_component_samples(D, n)}
    for name, t in THEMES.items():
        figure_step_vs_k(t, f"fig_step_vs_k_{name}.png")
        figure_active_support(t, f"fig_active_support_{name}.png", samples)

    # Numbers quoted in the page captions and worked examples.
    print(f"d={D}, s={S}, k={K_SPARSE}")
    print(f"E[J] = ks/d = {K_SPARSE * S / D:.3f}")
    print(f"P(J>=1) exact = {hit_probability_exact(K_SPARSE):.4f}, approx = {hit_probability_approx(K_SPARSE):.4f}")
    print(f"P(J=0) exact = {1 - hit_probability_exact(K_SPARSE):.4f}")
    for key in (K_SPARSE, D):
        x = samples[key]
        print(f"k={key}: mean ||P_A v||^2 = {np.mean(x**2):.4f} (theory s/d = {S / D:.4f}), "
              f"mass at zero = {np.mean(x == 0):.4f}, "
              f"mean ||P_A v|| given hit = {np.mean(x[x > 0]):.4f}, "
              f"90th percentile = {np.quantile(x, 0.9):.4f}")
    print(f"sqrt(d/k) = {math.sqrt(D / K_SPARSE):.2f}")
    print(f"coordinate-wise RMS step at k=4, h=1: {math.sqrt(4 / 3):.3f}; at k=16: {math.sqrt(16 / 3):.3f}")
