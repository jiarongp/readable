### 6.1 The generator, and what $k$ means

Background the reader needs: CTS (the candidate sampler this study builds on) and RAASP (the perturbation sampler from TuRBO) are two ways of proposing candidate points around the current best point. The sparse construction studied here sits between them, so this subsection describes all three.

CTS generates candidates as

$$
x = c + r v, \qquad r \sim U(0, R), \qquad \lVert v \rVert_2 = 1,
$$

where $c$ is the incumbent (current best point), $v$ is a dense direction (every coordinate may be nonzero) and $r$ is a distance drawn independently of $v$. Two details of CTS matter later. First, it draws $v$ from a truncated multivariate normal, so that a random direction does not point into a nearby wall of the domain. Second, it caps the permissible radius by both the wall distance and a trust-region-like $R_{\max}$. (LITERATURE CONTEXT TO VERIFY: the exact construction, Rashidi, Johnstonbaugh & Gao 2024.)

RAASP works differently. It decides coordinate by coordinate whether to perturb that coordinate, with probability $\min(1, 20/d)$ in the original TuRBO implementation, and fills the perturbed coordinates with values from Sobol points inside the rectangular trust region. For $d \gg 20$, about 20 coordinates move in each candidate.

The sparse construction sits between them. Choose a support $S \subseteq \{1, \ldots, d\}$ with $\lvert S \rvert = k$, set $v_i = 0$ for $i \notin S$, then draw the direction on $S$ and the radius exactly as CTS does. The parameter $k$ interpolates between the two samplers: $k = 1$ is a coordinate-like move, $1 < k < d$ a sparse move, and $k = d$ is ordinary CTS in the interior (§2). One point to hold onto for the rest of this section: $k$ is an **angular support dimension**, meaning how many coordinates the direction $v$ may use. It is not a distance. FACT.

### 6.2 Why RAASP's "20" cannot be inherited

A natural first instinct is to reuse TuRBO's value of 20 for $k$. This subsection explains why that number does not transfer.

The reason is that in RAASP-style samplers, the number of perturbed coordinates also sets the step length. Suppose each of $k$ perturbed coordinates is displaced independently by $\delta_i \sim U(-h, h)$. Then $\mathbb{E}[\delta_i^2] = h^2 / 3$ and

$$
\mathbb{E}\lVert \delta \rVert_2^2 = \frac{k h^2}{3},
$$

so the typical step length grows like $\sqrt{k}$. Increasing $k$ changes two things at once: *how many coordinates move* and *how far the candidate moves*. That is a FACT about this simplified model, not a claim about every RAASP implementation. But it is one reason sparsity helps RAASP stay local, and it is why TuRBO's value 20 belongs to a sampler in which support size also sets distance.

The unit-direction construction of §6.1 behaves differently. There, $\delta = r v$ with $\lVert v \rVert = 1$, so

$$
\lVert \delta \rVert_2 = r
$$

exactly. With $r \sim U(0, R)$, the mean squared step is $R^2 / 3$ for every $k$ (FACT, in the interior). The two controls are therefore separate: $k$ is how many coordinates cooperate in a move, and $r$ is how far the move goes.

This separation is what makes the study's first hypothesis testable. HYPOTHESIS (the thread's first): some of the effect commonly attributed to sparse perturbations is due to the support size itself, rather than to the shorter steps that coordinate-wise sparsity produces as a side effect. The test is to hold the radial law fixed and sweep $k$. If the differences between sparse and dense sampling disappear once step length is controlled, the hypothesis is weakened.

### 6.3 What a random support does

This subsection asks what choosing a random support $S$ actually does when the objective depends on only a few coordinates. The setup is for analysis only, not a claim about real objectives.

Take an axis-aligned objective that depends on an active set $A$ of coordinates with $\lvert A \rvert = s$, and a support $S$ drawn uniformly among the $k$-subsets of $\{1, \ldots, d\}$. The overlap $J = \lvert S \cap A \rvert$, the number of active coordinates the move touches, is hypergeometric:

$$
P(J = j) = \frac{\binom{s}{j} \binom{d - s}{k - j}}{\binom{d}{k}}, \qquad \mathbb{E}[J] = \frac{k s}{d},
$$

and for $s, k \ll d$ the chance of touching at least one active coordinate is about $1 - e^{-k s / d}$ (FACT). This is the familiar argument against very sparse supports: a small $k$ often misses the active coordinates entirely. It is only half the story.

The other half concerns how much of the direction's energy lands in the active subspace when the move does hit it. Write $P_A$ for the projection onto the active coordinates. If the direction is isotropic on $S$, then conditional on $J = j$ the squared active-space energy $\lVert P_A v \rVert^2$ has mean $j / k$, and averaging over supports gives

$$
\mathbb{E}\lVert P_A v \rVert^2 = \mathbb{E}\Big[ \frac{J}{k} \Big] = \frac{s}{d}
$$

for every $k$ (FACT under isotropy). In other words, sparse and dense pools allocate the same *average* fraction of directional energy to an unknown active subspace. The intuition that "smaller $k$ puts more energy into the active coordinates" is false on average.

What changes is the *distribution* of that energy across candidates. A dense direction gives every candidate a small active component of size about $1 / \sqrt{d}$. A sparse direction gives most candidates no active component at all, and the rest a component of size about $1 / \sqrt{k}$. At $d = 500$ and $k = 20$, that is a factor 5 larger per hit. Sparse pools therefore trade hit probability, which rises with $k$, for concentration per hit, which rises as $k$ falls.

This trade matters because the optimizer does not use an average candidate: it takes the best candidate of a pool of $M$. That makes it an extreme-value question, and the pool size $M$ is part of the answer. HYPOTHESIS: rare strong hits beat ubiquitous weak hits when the pool is large enough and the selector can find them. Step 0 (§4) makes this quantitative under the linear model. The tail diagnostic of Step 3 measures it directly: the distribution of the active-space displacement $D_A = \lVert P_A (x - c) \rVert$ per $k$, with its mass at zero and its upper quantiles.
