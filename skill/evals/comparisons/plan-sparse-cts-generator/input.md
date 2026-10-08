<!-- Source: docs/plan/sparse_cts_plan.md, sections 6.1-6.3 (lines 1098-1192), as of 2026-10-08 -->

### 6.1 The generator, and what $k$ means

CTS generates candidates as

$$
x = c + r v, \qquad r \sim U(0, R), \qquad \lVert v \rVert_2 = 1,
$$

with $c$ the incumbent, $v$ a dense direction and $r$ an independent
distance. CTS draws $v$ from a truncated multivariate normal so that a
dense random direction does not point into a nearby wall, and caps the
permissible radius by both the wall distance and a trust-region-like
$R_{\max}$ (LITERATURE CONTEXT TO VERIFY: the exact construction, Rashidi,
Johnstonbaugh & Gao 2024). RAASP instead decides per coordinate whether to
perturb it, with probability $\min(1, 20/d)$ in the original TuRBO
implementation, and fills the perturbed coordinates from Sobol points
inside the rectangular trust region; for $d \gg 20$ about 20 coordinates
move.

The sparse construction sits between them: choose a support
$S \subseteq \{1, \ldots, d\}$ with $\lvert S \rvert = k$, set $v_i = 0$ for
$i \notin S$, draw the direction on $S$ and the radius as CTS does. Then
$k = 1$ is a coordinate-like move, $1 < k < d$ a sparse move and $k = d$
ordinary CTS in the interior (§2). $k$ is an **angular support dimension**,
not a distance: FACT.

### 6.2 Why RAASP's "20" cannot be inherited

Suppose each of $k$ perturbed coordinates is displaced independently by
$\delta_i \sim U(-h, h)$. Then $\mathbb{E}[\delta_i^2] = h^2 / 3$ and

$$
\mathbb{E}\lVert \delta \rVert_2^2 = \frac{k h^2}{3},
$$

so the typical step grows like $\sqrt{k}$: increasing $k$ changes *how many
coordinates move* and *how far the candidate moves* at once. That is a FACT
about this simplified model, not a claim about every RAASP implementation,
but it is one reason sparsity helps RAASP stay local, and it is why the
TuRBO value 20 belongs to a sampler in which support size also sets
distance. For the unit-direction construction, $\delta = r v$ with
$\lVert v \rVert = 1$ gives

$$
\lVert \delta \rVert_2 = r
$$

exactly, so with $r \sim U(0, R)$ the mean squared step is $R^2 / 3$ for
every $k$ (FACT, in the interior). The two controls are then separate:
$k$ is how many coordinates cooperate, $r$ is how far the move goes.
HYPOTHESIS (the thread's first): some of the effect commonly attributed to
sparse perturbations is due to the support size itself rather than to the
shorter steps that coordinate-wise sparsity produces. The test is to hold
the radial law fixed and sweep $k$; if the differences disappear under
radial control, the hypothesis is weakened.

### 6.3 What a random support does

Take, for analysis only, an axis-aligned objective depending on an active
set $A$ with $\lvert A \rvert = s$, and a support $S$ drawn uniformly among
the $k$-subsets. The overlap $J = \lvert S \cap A \rvert$ is hypergeometric,

$$
P(J = j) = \frac{\binom{s}{j} \binom{d - s}{k - j}}{\binom{d}{k}}, \qquad \mathbb{E}[J] = \frac{k s}{d},
$$

and for $s, k \ll d$ the chance of touching at least one active coordinate
is about $1 - e^{-k s / d}$ (FACT). This is the familiar argument against
very sparse supports, and it is only half the story.

If the direction is isotropic on $S$, then conditional on $J = j$ the
squared active-space energy $\lVert P_A v \rVert^2$ has mean $j / k$, and
averaging over supports gives

$$
\mathbb{E}\lVert P_A v \rVert^2 = \mathbb{E}\Big[ \frac{J}{k} \Big] = \frac{s}{d}
$$

for every $k$ (FACT under isotropy). Sparse and dense pools allocate the
same *average* fraction of directional energy to an unknown active
subspace, so "smaller $k$ puts more energy into the active coordinates" is
false on average. What changes is the *distribution*: a dense direction
gives every candidate a small active component of size about
$1 / \sqrt{d}$; a sparse one gives most candidates none and the rest a
component of size about $1 / \sqrt{k}$ (at $d = 500$, $k = 20$ a factor
5 larger). Sparse pools trade hit probability, which rises with $k$, for
concentration per hit, which rises as $k$ falls. Because the optimizer then
takes the best candidate of a pool of $M$, this is an extreme-value
question, and the pool size $M$ is part of the answer. HYPOTHESIS: rare
strong hits beat ubiquitous weak hits when the pool is large enough and
the selector can find them. Step 0 (§4) makes this quantitative under the
linear model, and the tail diagnostic of Step 3 — the distribution of the
active-space displacement $D_A = \lVert P_A (x - c) \rVert$ per $k$, with
its mass at zero and upper quantiles — measures it.

