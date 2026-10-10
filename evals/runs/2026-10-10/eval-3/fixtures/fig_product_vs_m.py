"""Figure for technical-note.html: how the feasibility score P(feasible | x)
shrinks as the number of constraints m grows, when every constraint has the
same per-constraint satisfaction probability p.

Illustration with hypothetical values, not measured data. The curves are
p ** m for p in {0.95, 0.80, 0.60}. The vertical hairline marks m = 3, the
case in the note.

Render (no local matplotlib on this machine):
    uv run --offline --no-project --with matplotlib --with numpy \
        python3 fig_product_vs_m.py
Writes fig_product_vs_m.png (1600 x 900 px, transparent background) beside
this script.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Neutral ink that reads on both the light and the dark page surface.
INK = "#7A8480"
GRID = "#A7B0AC"
# Categorical slots 1-3 of the reference palette, in fixed order, stepped so the
# same PNG passes the palette validator on both the light and the dark surface.
SERIES = [(0.95, "#2a78d6"), (0.80, "#d95926"), (0.60, "#199e70")]
FONT = ["Avenir Next", "Helvetica Neue", "DejaVu Sans", "sans-serif"]

m = np.arange(1, 9)

fig, ax = plt.subplots(figsize=(8, 4.5), dpi=200)
fig.patch.set_alpha(0.0)
ax.set_facecolor("none")

for p, color in SERIES:
    y = p ** m
    ax.plot(m, y, color=color, linewidth=2, solid_capstyle="round",
            solid_joinstyle="round", zorder=3)
    ax.scatter(m, y, s=48, color=color, zorder=4, linewidths=0)
    ax.annotate(f"p = {p:.2f}", xy=(m[-1], y[-1]), xytext=(10, 0),
                textcoords="offset points", va="center", ha="left",
                color=INK, fontsize=10.5, fontfamily=FONT)

# Reference line at the note's case, m = 3.
ax.axvline(3, color=GRID, linewidth=1, zorder=1)
ax.text(3.08, 1.0, "this note: m = 3", color=INK, fontsize=10, va="top",
        fontfamily=FONT)

ax.set_xlim(0.6, 9.4)
ax.set_ylim(0, 1.04)
ax.set_xticks(m)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(["0", "0.25", "0.50", "0.75", "1.00"])
ax.set_xlabel("Number of constraints  m", color=INK, fontsize=11, fontfamily=FONT)
ax.set_ylabel("Score  P(feasible | x) = p^m", color=INK, fontsize=11, fontfamily=FONT)
ax.tick_params(colors=INK, labelsize=10, length=0)
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontfamily(FONT)
ax.grid(axis="y", color=GRID, linewidth=1, alpha=0.5, zorder=0)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.spines["bottom"].set_linewidth(1)

fig.tight_layout()
out = Path(__file__).with_suffix(".png")
fig.savefig(out, dpi=200, transparent=True)
print(out)
