"""Illustrative figures for sections 6.2 and 6.3 of the sparse CTS plan.

Both figures are computed from the simplified models stated in the text,
not from measured optimizer runs.

Run from inside this folder:
    uv run --offline --no-project --with matplotlib --with numpy python3 make_figures.py
"""
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(0)

# ---------------------------------------------------------------------------
# Figure 1 (section 6.2): typical step length versus support size k.
# Coordinate-wise model: each of k coordinates moves by U(-h, h), so the
# root mean squared step is sqrt(k h^2 / 3).  Unit-direction model: the
# step is r ~ U(0, R) regardless of k, so the RMS step is sqrt(R^2 / 3).
# We set h = R = 1 so both curves are in the same arbitrary units.
# ---------------------------------------------------------------------------
k = np.arange(1, 51)
rms_coord = np.sqrt(k / 3.0)
rms_unit = np.full_like(k, np.sqrt(1.0 / 3.0), dtype=float)

fig, ax = plt.subplots(figsize=(6.0, 3.6))
ax.plot(k, rms_coord, color="#c0392b", lw=2,
        label=r"coordinate-wise: $\delta_i \sim U(-h,h)$, RMS $=\sqrt{k h^2/3}$")
ax.plot(k, rms_unit, color="#2c3e50", lw=2,
        label=r"unit direction: $\delta = r v$, RMS $=\sqrt{R^2/3}$")
ax.axvline(20, color="gray", ls=":", lw=1)
ax.text(20.6, 1.3, "k = 20\n(TuRBO default)", fontsize=8, color="gray", va="top")
ax.set_xlabel("support size $k$ (number of coordinates that move)")
ax.set_ylabel("root mean squared step length\n(units of $h$ or $R$; here $h = R = 1$)")
ax.set_xlim(1, 50)
ax.set_ylim(0, 4.2)
ax.legend(loc="upper left", fontsize=8, frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("step_vs_k.png", dpi=160)
plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 2 (section 6.3): survival curve (fraction of candidates above a
# threshold) of the active-space energy ||P_A v||^2 for a sparse support
# (k = 20) and a dense one (k = d),
# at d = 500 with an active set of size s = 10.  The support S is a
# uniform k-subset; the direction is isotropic on S (standard normal
# on S, then normalised).  Both distributions have mean s/d = 0.02.
# ---------------------------------------------------------------------------
d, s, n_draws = 500, 10, 40000
active = np.arange(s)  # which coordinates are active does not matter


def active_energy(k_support):
    out = np.empty(n_draws)
    for t in range(n_draws):
        support = rng.choice(d, size=k_support, replace=False)
        g = rng.standard_normal(k_support)
        g /= np.linalg.norm(g)
        v = np.zeros(d)
        v[support] = g
        out[t] = np.sum(v[active] ** 2)
    return out


e_sparse = active_energy(20)
e_dense = active_energy(d)
mean_target = s / d

ts = np.linspace(0, 0.3, 601)
surv_sparse = np.array([np.mean(e_sparse > t) for t in ts])
surv_dense = np.array([np.mean(e_dense > t) for t in ts])

fig, ax = plt.subplots(figsize=(6.0, 3.8))
ax.plot(ts, surv_dense, color="#2c3e50", lw=2, label="$k = 500$ (dense)")
ax.plot(ts, surv_sparse, color="#c0392b", lw=2, label="$k = 20$ (sparse)")
ax.axvline(mean_target, color="black", ls="--", lw=1)
ax.text(mean_target + 0.004, 0.62, "common mean\n$s/d = 0.02$", fontsize=8, va="center")
ax.annotate(f"{np.mean(e_sparse == 0):.0%} of sparse candidates\nhave exactly zero",
            xy=(0.0, surv_sparse[0]), xytext=(0.06, 0.45), fontsize=8,
            arrowprops=dict(arrowstyle="->", color="gray", lw=0.8))
q95_s, q95_d = np.percentile(e_sparse, 95), np.percentile(e_dense, 95)
ax.annotate(f"95th percentile\ndense {q95_d:.3f}, sparse {q95_s:.3f}",
            xy=(q95_s, 0.05), xytext=(0.14, 0.22), fontsize=8,
            arrowprops=dict(arrowstyle="->", color="gray", lw=0.8))
ax.set_xlabel(r"threshold $t$ on active-space energy $\|P_A v\|^2$  ($d = 500$, $s = 10$)")
ax.set_ylabel("fraction of candidates\nwith energy above $t$")
ax.set_xlim(0, 0.3)
ax.set_ylim(0, 1.02)
ax.legend(loc="upper right", fontsize=8, frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("active_energy.png", dpi=160)
plt.close(fig)

print("P(J=0) empirical, sparse:", np.mean(e_sparse == 0.0))
print("means:", e_dense.mean(), e_sparse.mean())
print("sparse nonzero mean:", e_sparse[e_sparse > 0].mean())
print("sparse 95th pct:", np.percentile(e_sparse, 95), "dense 95th pct:", np.percentile(e_dense, 95))
