"""Figure for technical-note.html: what the independence product can miss.

Two constraints, each satisfied with probability p (hypothetical values).
Without knowing how the two events depend on each other, the probability that
both are satisfied can lie anywhere between the Frechet bounds
    max(0, 2p - 1)  <=  P(both)  <=  p.
The independence assumption picks one value inside that band: p**2.

Renders one PNG per theme so the page can show the matching one:
    uv run --offline --no-project --with matplotlib --with numpy python3 fig_independence_bounds.py
Outputs fig_independence_bounds_light.png and fig_independence_bounds_dark.png
(1600 x 900 px) beside this script.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

THEMES = {
    "light": dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781",
                  grid="#e1e0d9", axis="#c3c2b7", series="#2a78d6", band="#b7d3f6"),
    "dark": dict(surface="#1a1a19", ink="#f0efec", ink2="#c3c2b7", muted="#898781",
                 grid="#2c2c2a", axis="#383835", series="#3987e5", band="#184f95"),
}

p = np.linspace(0, 1, 401)
upper = p                      # min(p, p)
product = p ** 2               # independence
lower = np.maximum(0, 2 * p - 1)
P0 = 0.8                       # worked point used in the note

for name, c in THEMES.items():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 11, "axes.labelsize": 11, "xtick.labelsize": 10, "ytick.labelsize": 10,
        "text.color": c["ink2"], "axes.labelcolor": c["ink2"],
        "xtick.color": c["muted"], "ytick.color": c["muted"],
    })
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=200)
    fig.patch.set_facecolor(c["surface"])
    ax.set_facecolor(c["surface"])

    ax.fill_between(p, lower, upper, color=c["band"], alpha=0.5, linewidth=0,
                    label="all values consistent with the two marginals")
    ax.plot(p, upper, color=c["muted"], lw=1.2, label="upper bound  min(p₁, p₂) = p")
    ax.plot(p, lower, color=c["muted"], lw=1.2, label="lower bound  max(0, 2p − 1)")
    ax.plot(p, product, color=c["series"], lw=1.8, label="independence product  p²")

    # The worked point from the note: p = 0.8.
    ax.vlines(P0, 0, P0, color=c["axis"], lw=0.8)
    ax.plot([P0], [P0 ** 2], "o", ms=5, color=c["series"], mec=c["surface"], mew=1.2)
    ax.plot([P0, P0], [2 * P0 - 1, P0], "o", ms=4, color=c["muted"], mec=c["surface"], mew=1.2)
    ax.annotate("p = 0.8\ntrue value: 0.60 to 0.80\nindependence: 0.64",
                xy=(P0, P0 ** 2), xytext=(0.985, 0.30), ha="right", va="center",
                fontsize=9.5, color=c["ink"],
                arrowprops=dict(arrowstyle="-", color=c["axis"], lw=0.8, shrinkB=4))

    # Selective direct labels, placed where the curves are well separated.
    ax.text(0.33, 0.33 + 0.045, "upper bound", color=c["muted"], fontsize=9.5,
            ha="center", va="bottom", rotation=0)
    ax.text(0.60, 0.36 - 0.05, "independence product", color=c["series"], fontsize=9.5,
            ha="center", va="top")
    ax.text(0.68, 0.0 + 0.02, "lower bound", color=c["muted"], fontsize=9.5,
            ha="right", va="bottom")

    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ticks = [0, 0.25, 0.5, 0.75, 1]
    ax.set_xticks(ticks); ax.set_yticks(ticks)
    ax.set_xlabel("p: probability that each of the two constraints is satisfied")
    ax.set_ylabel("P(both satisfied | x)")
    ax.grid(True, color=c["grid"], lw=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(c["axis"]); ax.spines[s].set_linewidth(0.8)
    ax.tick_params(length=3, width=0.8, color=c["axis"])
    leg = ax.legend(loc="upper left", frameon=False, fontsize=9, labelcolor=c["ink2"],
                    handlelength=1.8)
    fig.tight_layout()
    fig.savefig(f"fig_independence_bounds_{name}.png", dpi=200, facecolor=c["surface"])
    plt.close(fig)
print("done")
