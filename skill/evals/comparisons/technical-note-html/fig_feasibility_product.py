"""Illustration for technical-note.html: how the product feasibility score
falls as constraints accumulate, under the independence assumption.

Hypothetical values, not measured data. Each line fixes the same per-constraint
satisfaction probability p for every constraint and plots p**m for m = 1..8.

Render (no local matplotlib on this machine):
    uv run --offline --no-project --with matplotlib --with numpy python3 fig_feasibility_product.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

m = np.arange(1, 9)
levels = [0.95, 0.90, 0.80]
colors = ["#1F5F8B", "#3E8E9E", "#B5651D"]

fig, ax = plt.subplots(figsize=(8, 4.5), dpi=200)
for p, c in zip(levels, colors):
    score = p ** m
    ax.plot(m, score, marker="o", color=c, linewidth=2, markersize=5,
            label=f"each constraint satisfied with p = {p:.2f}")
    ax.annotate(f"{score[-1]:.2f}", (m[-1], score[-1]), textcoords="offset points",
                xytext=(8, -3), fontsize=9, color=c)

ax.axvline(3, color="#888888", linestyle=":", linewidth=1)
ax.text(3.08, 0.98, "m = 3 in this note", fontsize=9, color="#555555", va="top")

ax.set_xlabel("number of constraints m")
ax.set_ylabel("feasibility score  P(feasible | x) = p^m")
ax.set_xticks(m)
ax.set_ylim(0, 1.02)
ax.set_xlim(0.8, 8.6)
ax.grid(True, alpha=0.3)
ax.legend(frameon=False, loc="upper right", bbox_to_anchor=(1.0, 0.9))
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
fig.tight_layout()
fig.savefig("fig_feasibility_product.png")
print("wrote fig_feasibility_product.png")
