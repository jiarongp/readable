"""Figures for the group note on Doumont et al. (2025), arXiv:2512.00170.

Run from this directory:
    uv run --offline --no-project --with matplotlib --with numpy python3 make_figures.py

Writes three PNGs (1600 px wide, transparent background) that the note embeds
as data URIs:
    fig1_boundary.png    boundary-seeking of a plain linear model (hypothetical
                         1-D fit) next to the paper's exact Appendix A.2 counterexample
    fig2_projection.png  inverse stereographic projection for D = 1
    fig3_thin_shell.png  Monte Carlo of the scaled-input norm (thin-shell effect)

Colors are chosen to read on both a light and a dark page, so each figure is
one image for both themes. Ink (#898781) is the mode-invariant muted ink from
the dataviz palette; series colors are its validated categorical/ordinal steps.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

INK = "#898781"        # axis labels, ticks, annotations (reads on both themes)
GRID = "#898781"       # hairline grid, drawn at low alpha
BLUE, ORANGE, AQUA = "#3987e5", "#d95926", "#199e70"   # categorical slots 1-3
ORDINAL = ["#6da7ec", "#3987e5", "#256abf", "#184f95"]  # one hue, light -> dark

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "text.color": INK,
    "axes.labelcolor": INK,
    "axes.edgecolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "figure.facecolor": "none",
    "axes.facecolor": "none",
    "savefig.facecolor": "none",
    "savefig.transparent": True,
    "legend.frameon": False,
})

DPI = 200
W = 1600 / DPI  # 8 in wide -> 1600 px


def grid(ax):
    ax.grid(True, color=GRID, alpha=0.25, linewidth=0.6)
    ax.set_axisbelow(True)


# --------------------------------------------------------------------------
# Figure 1: boundary seeking
# --------------------------------------------------------------------------
def fig1():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(W, W * 0.5), dpi=DPI)
    x = np.linspace(-1, 1, 401)

    # Left: a hypothetical 1-D Bayesian linear model, following the form used in
    # the paper's proof of Theorem 1: mu(x) = beta x, sigma(x) = sqrt(s_eps^2 + S x^2).
    beta, S, s_eps2, kappa = 0.6, 0.3, 0.05, 2.0
    mu = beta * x
    sigma = np.sqrt(s_eps2 + S * x**2)
    ucb = mu + kappa * sigma

    ax1.fill_between(x, mu - sigma, mu + sigma, color=BLUE, alpha=0.18, linewidth=0)
    ax1.plot(x, mu, color=BLUE, linewidth=2, label="posterior mean  $\\mu(x)$")
    ax1.plot(x, ucb, color=ORANGE, linewidth=2, label="UCB  $\\mu + 2\\sigma$")
    i = np.argmax(ucb)
    ax1.plot(x[i], ucb[i], "o", color=ORANGE, markersize=8)
    ax1.annotate("maximum sits on the\nboundary, x = 1", xy=(x[i], ucb[i]),
                 xytext=(-0.35, 1.95), fontsize=10, va="center",
                 arrowprops=dict(arrowstyle="-", color=INK, linewidth=0.8,
                                 connectionstyle="arc3,rad=-0.2"))
    ax1.axvline(-1, color=INK, linewidth=0.8, alpha=0.6)
    ax1.axvline(1, color=INK, linewidth=0.8, alpha=0.6)
    ax1.set_xlim(-1.05, 1.05)
    ax1.set_ylim(-1.4, 2.3)
    ax1.set_xlabel("x  (search space [-1, 1])")
    ax1.set_title("(a) Plain linear kernel (hypothetical fit)", loc="left", fontsize=11)
    ax1.legend(loc="lower right", fontsize=9)
    grid(ax1)

    # Right: the paper's counterexample (Appendix A.2), exact.
    # alpha(x) = (1/2) * 2x/(x^2+1) - (x^2-1)/(x^2+1), with beta_hat = (1/2, -1).
    alpha = 0.5 * (2 * x) / (x**2 + 1) - (x**2 - 1) / (x**2 + 1)
    ax2.plot(x, alpha, color=AQUA, linewidth=2)
    for xv, lab, dx, dy, ha in [(-1, "α(−1) = −½", 0.08, -0.02, "left"),
                                (0.5, "α(½) = 1", 0.0, 0.14, "center"),
                                (1, "α(1) = ½", -0.06, -0.2, "right")]:
        yv = 0.5 * (2 * xv) / (xv**2 + 1) - (xv**2 - 1) / (xv**2 + 1)
        ax2.plot(xv, yv, "o", color=AQUA, markersize=8)
        ax2.annotate(lab, xy=(xv, yv), xytext=(xv + dx, yv + dy), ha=ha, fontsize=10)
    ax2.axvline(-1, color=INK, linewidth=0.8, alpha=0.6)
    ax2.axvline(1, color=INK, linewidth=0.8, alpha=0.6)
    ax2.set_xlim(-1.05, 1.05)
    ax2.set_ylim(-0.75, 1.3)
    ax2.set_xlabel("x  (search space [-1, 1])")
    ax2.set_title("(b) With spherical map (paper, App. A.2)", loc="left", fontsize=11)
    grid(ax2)

    fig.tight_layout()
    fig.savefig("fig1_boundary.png", dpi=DPI)
    plt.close(fig)


# --------------------------------------------------------------------------
# Figure 2: inverse stereographic projection, D = 1
# --------------------------------------------------------------------------
def P(z):
    z = np.asarray(z, dtype=float)
    return 2 * z / (z**2 + 1), (z**2 - 1) / (z**2 + 1)


def fig2():
    fig, ax = plt.subplots(figsize=(W, W * 0.58), dpi=DPI)
    ax.set_aspect("equal")
    ax.add_patch(Circle((0, 0), 1, fill=False, edgecolor=INK, linewidth=1.2))
    ax.axhline(0, color=INK, linewidth=1.0)              # the real line (z axis)
    ax.text(2.9, 0.06, "real line  z", fontsize=10, ha="right")
    ax.plot(0, 1, "o", color=INK, markersize=7)
    ax.text(0.08, 1.06, "north pole  (z → ±∞)", fontsize=10)

    zs = [-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0]
    for z in zs:
        px, py = P(z)
        on_unit = abs(abs(z) - 1) < 1e-9
        col = ORANGE if on_unit else BLUE
        # ray from the north pole through (z, 0) to its image on the circle
        ax.plot([0, z], [1, 0], color=col, linewidth=0.9, alpha=0.6)
        if not on_unit:
            ax.plot([z, px], [0, py], color=col, linewidth=0.9, alpha=0.6, linestyle=(0, (3, 2)))
        ax.plot(z, 0, "s", color=col, markersize=6)
        ax.plot(px, py, "o", color=col, markersize=7, markeredgecolor="white", markeredgewidth=1.2)

    ax.annotate("z = ±1 stay where they are:\nP(z) = [z, 0]", xy=(1, 0), xytext=(1.45, -0.55),
                fontsize=10, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, linewidth=0.8))
    ax.annotate("|z| < 1 → lower half", xy=P(0.5), xytext=(0.55, -1.25), fontsize=10, color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, linewidth=0.8))
    ax.annotate("|z| > 1 → upper half", xy=P(-2.0), xytext=(-2.9, 0.85), fontsize=10, color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, linewidth=0.8))
    ax.text(0, -1.12, "z = 0 → south pole", fontsize=10, ha="center", color=BLUE)

    ax.set_xlim(-3, 3)
    ax.set_ylim(-1.45, 1.35)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig("fig2_projection.png", dpi=DPI)
    plt.close(fig)


# --------------------------------------------------------------------------
# Figure 3: thin shell, Monte Carlo
# --------------------------------------------------------------------------
def fig3():
    rng = np.random.default_rng(0)
    fig, ax = plt.subplots(figsize=(W, W * 0.5), dpi=DPI)
    Ds = [2, 10, 100, 1000]
    n = 20000
    bins = np.linspace(0, 2.0, 161)
    label_pos = {2: (1.35, 1.6), 10: (1.22, 3.0), 100: (1.12, 8.5), 1000: (1.06, 22.0)}
    for D, col in zip(Ds, ORDINAL):
        x = rng.uniform(-1, 1, size=(n, D))
        z = x * np.sqrt(3.0 / D)
        norms = np.linalg.norm(z, axis=1)
        hist, edges = np.histogram(norms, bins=bins, density=True)
        centers = 0.5 * (edges[1:] + edges[:-1])
        ax.plot(centers, hist, color=col, linewidth=2)
        ax.text(*label_pos[D], f"D = {D}", fontsize=10, va="center")
    ax.axvline(1.0, color=INK, linewidth=0.8, alpha=0.6)
    ax.text(0.98, 15, "‖z‖ = 1: where P is the identity", fontsize=10, va="center", ha="right")
    ax.set_xlabel("‖z‖  for x uniform on [−1, 1]^D, scaled by √(3/D)")
    ax.set_ylabel("density")
    ax.set_xlim(0, 2.0)
    grid(ax)
    fig.tight_layout()
    fig.savefig("fig3_thin_shell.png", dpi=DPI)
    plt.close(fig)


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    print("wrote fig1_boundary.png fig2_projection.png fig3_thin_shell.png")
