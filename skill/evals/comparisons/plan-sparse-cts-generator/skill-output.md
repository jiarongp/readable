<!-- Skill version: after adding paragraph-contract, picture-before-mechanism, and figure rules (2026-10-08) -->

### 6.1 The generator, and what $k$ means

This section defines the sparse candidate generator the plan studies and pins down what its parameter $k$ controls. The sparse construction sits between two existing generators: CTS, which the plan builds on, and RAASP, the perturbation scheme used in TuRBO. We describe those two first.

CTS generates each candidate by choosing a direction and a distance separately, then stepping away from the incumbent $c$ (the best point found so far):

$$
x = c + r v, \qquad r \sim U(0, R), \qquad \lVert v \rVert_2 = 1,
$$

Here $v$ is a dense unit direction, meaning every coordinate of $v$ can be nonzero, and $r$ is the distance moved along $v$, drawn independently of $v$ and uniformly between $0$ and a cap $R$. Two details of CTS matter later. First, CTS draws $v$ from a truncated multivariate normal, so that a dense random direction does not point into a nearby wall of the box domain. Second, it caps the permissible radius by both the wall distance and a trust-region-like $R_{\max}$. (LITERATURE CONTEXT TO VERIFY: the exact construction, Rashidi, Johnstonbaugh & Gao 2024.)

RAASP works coordinate by coordinate instead. For each of the $d$ coordinates it decides independently whether to perturb that coordinate, with probability $\min(1, 20/d)$ in the original TuRBO implementation. The perturbed coordinates take their new values from Sobol points inside the rectangular trust region; the other coordinates keep the incumbent's values. For $d \gg 20$, about 20 coordinates move per candidate.

The sparse construction combines the two ideas. It first chooses a **support** $S \subseteq \{1, \ldots, d\}$, the set of coordinates allowed to move, with $\lvert S \rvert = k$. It sets $v_i = 0$ for every $i \notin S$, then draws the direction on the coordinates in $S$ and draws the radius, both as CTS does. The candidate still moves a distance $r$ along a unit vector; only $k$ coordinates take part in that vector.

The value of $k$ covers the familiar cases:

- $k = 1$ is a coordinate-like move: one coordinate changes.
- $1 < k < d$ is a sparse move.
- $k = d$ is ordinary CTS in the interior (§2).

As a concrete instance (hypothetical numbers), take $d = 500$ and $k = 20$. The direction $v$ has 480 zero entries, its 20 nonzero entries form a unit vector, and the candidate moves distance $r$ along it.

The point to hold onto is that $k$ is an **angular support dimension**, not a distance: FACT. It sets how many coordinates the direction uses; the distance is set separately by $r$. §6.2 makes this quantitative.

### 6.2 Why RAASP's "20" cannot be inherited

A natural first guess is to set $k = 20$ because RAASP moves about 20 coordinates. This section explains why that number does not carry over. In a coordinate-wise sampler, the number of moving coordinates also sets the step length; in the unit-direction construction it does not.

Consider a simplified model of coordinate-wise perturbation. Suppose each of $k$ perturbed coordinates is displaced independently by $\delta_i \sim U(-h, h)$, a uniform draw within $\pm h$. Each coordinate then contributes $\mathbb{E}[\delta_i^2] = h^2 / 3$ to the squared step, and summing over the $k$ coordinates gives

$$
\mathbb{E}\lVert \delta \rVert_2^2 = \frac{k h^2}{3},
$$

so the typical step grows like $\sqrt{k}$. Increasing $k$ therefore changes two things at once: *how many coordinates move* and *how far the candidate moves*. For example (hypothetical numbers, same $h$ throughout), moving 4 coordinates instead of 1 quadruples the mean squared step and doubles the typical step; moving 20 coordinates makes the typical step about 4.5 times that of a single-coordinate move.

That is a FACT about this simplified model, not a claim about every RAASP implementation. However, it is one reason sparsity helps RAASP stay local: fewer moving coordinates means shorter steps. It is also why the TuRBO value 20 belongs to a sampler in which support size also sets distance. The number bundles two effects that the unit-direction construction keeps apart.

In the unit-direction construction, the displacement is $\delta = r v$ with $\lVert v \rVert = 1$, so

$$
\lVert \delta \rVert_2 = r
$$

exactly. With $r \sim U(0, R)$, the mean squared step is $R^2 / 3$ for every $k$ (FACT, in the interior, that is, where the wall cap on the radius does not bind). The two controls are then separate: $k$ is how many coordinates cooperate, and $r$ is how far the move goes.

HYPOTHESIS (the thread's first): some of the effect commonly attributed to sparse perturbations is due to the support size itself rather than to the shorter steps that coordinate-wise sparsity produces. The test is to hold the radial law (the distribution of $r$) fixed and sweep $k$. If the differences between values of $k$ disappear under radial control, the hypothesis is weakened.

### 6.3 What a random support does

This section asks what a randomly chosen support does when only a few coordinates matter to the objective. Two facts come out. The *average* directional energy that lands on the important coordinates does not depend on $k$, but its *distribution* across candidates does. Combined with best-of-pool selection, that distribution motivates the section's hypothesis.

Take, for analysis only, an axis-aligned objective that depends on an **active set** $A$ of coordinates, with $\lvert A \rvert = s$, and a support $S$ drawn uniformly among the $k$-subsets of $\{1, \ldots, d\}$. The number of active coordinates the support touches, $J = \lvert S \cap A \rvert$, is hypergeometric (the overlap when drawing $k$ coordinates without replacement from $d$, of which $s$ are active):

$$
P(J = j) = \frac{\binom{s}{j} \binom{d - s}{k - j}}{\binom{d}{k}}, \qquad \mathbb{E}[J] = \frac{k s}{d},
$$

and for $s, k \ll d$ the chance of touching at least one active coordinate is about $1 - e^{-k s / d}$ (FACT). As an instance (hypothetical numbers), $d = 500$, $s = 10$ and $k = 20$ give $\mathbb{E}[J] = 0.4$, and about $1 - e^{-0.4} \approx 0.33$: roughly one sparse candidate in three touches an active coordinate at all. Small supports miss often. This is the familiar argument against very sparse supports, and it is only half the story.

The other half concerns how much of the direction lands on the active coordinates. Let $P_A$ denote the projection onto the active coordinates, so $\lVert P_A v \rVert^2$ is the fraction of the unit direction's squared length that lies in the active subspace, its **active-space energy**. If the direction is isotropic on $S$ (uniformly random over unit vectors supported on $S$), then conditional on $J = j$ this energy has mean $j / k$, because each of the $k$ support coordinates carries $1/k$ of the energy on average. Averaging over supports gives

$$
\mathbb{E}\lVert P_A v \rVert^2 = \mathbb{E}\Big[ \frac{J}{k} \Big] = \frac{s}{d}
$$

for every $k$ (FACT under isotropy). Sparse and dense pools therefore allocate the same *average* fraction of directional energy to an unknown active subspace, so the claim "smaller $k$ puts more energy into the active coordinates" is false on average.

What changes is the *distribution* of that energy across candidates. A dense direction gives every candidate a small active component, about $1 / \sqrt{d}$ on each active coordinate. A sparse direction gives most candidates none, and the rest a component of about $1 / \sqrt{k}$ on each active coordinate it hits. At $d = 500$ and $k = 20$ that is $1/\sqrt{20} \approx 0.22$ against $1/\sqrt{500} \approx 0.045$, a factor 5 larger. Sparse pools trade hit probability, which rises with $k$, for concentration per hit, which rises as $k$ falls.

Pool size decides how this trade plays out. The optimizer generates a pool of $M$ candidates and takes the best one, so what matters is not the average candidate but the best in the pool. That makes this an extreme-value question, and the pool size $M$ is part of the answer. HYPOTHESIS: rare strong hits beat ubiquitous weak hits when the pool is large enough and the selector (whatever rule picks the best of the pool) can find them. Step 0 (§4) makes this quantitative under the linear model. The tail diagnostic of Step 3 measures it: the distribution, per $k$, of the active-space displacement $D_A = \lVert P_A (x - c) \rVert$, including its mass at zero (candidates that miss the active set entirely) and its upper quantiles (the strong hits).

Figure to generate (illustration from the model above, not measured data): for the hypothetical case $d = 500$, $s = 10$, histograms of $\lVert P_A v \rVert^2$ over candidates for $k = 20$ and for $k = d$. Each bar counts candidates whose active-space energy falls in that bin. Compare the two shapes: the sparse histogram has a spike at zero and a long right tail, the dense one is a narrow bump near $s/d = 0.02$, and both have the same mean. The comparison shows the same average energy with a different spread, which is what the best-of-$M$ argument relies on.
