<!-- Human-preferred rendering of the same material, excerpted from docs/readable/sparse_cts.md (lines 23-27, 37-64, 90-114). Not a one-to-one target: it covers more and omits some details. Use for calibration of paragraph shape, examples, and figures. -->

This question matters because a common candidate-generation rule already favors changing a small subset of coordinates. TuRBO is an optimizer that searches within an adjustable region around a promising point. Its random axis-aligned subspace perturbation rule, or RAASP, changes about 20 coordinates in high dimensions.

However, that coordinate count also affects the distance traveled. In the plan's simplified model, where each changed coordinate receives an independent uniform perturbation, typical distance grows like $\sqrt{k}$. Moving from 5 changed coordinates to 20 would therefore roughly double the typical distance.

The familiar choice of 20 coordinates does not tell us which count would work best if distance were controlled separately. That is what this study aims to find out. It then asks whether any benefit helps an actual optimizer, which has to choose a candidate using an imperfect model.

## How do we change coordinate count while keeping distance the same?

*[Figure 1 of the target, not kept in this repository: Two moves change one or two coordinates: equal per-coordinate changes have different lengths, whereas normalized directions reach the same distance circle. Generated in the hdbo project by studies/plot_sparse_cts_readable.py.]*

*Illustration, not experimental data. On the left, changing a second coordinate adds distance: the orange arrow leaves the dashed radius-0.5 circle. On the right, both arrows reach that circle, so their comparison isolates direction and coordinate count. Each actual pool uses many distances between 0 and $R$, with the same draws reused across support sizes.*

We generate each candidate by making two separate choices: a direction and a distance. This construction gives us a **cylindrical candidate pool**, where a *pool* is simply the set of candidates available for selection.

For each candidate, we:

1. Start at the current best point, $c$.
2. Choose exactly $k$ coordinates at random, with every set of that size equally likely.
3. Draw a random direction using only those coordinates, with no preferred orientation within them. Scale the direction to have length one.
4. Draw a distance uniformly between zero and a maximum distance $R$, then move that far in the chosen direction.

In symbols, this is

$$
x = c + r v, \qquad r \sim U(0,R), \qquad \lVert v\rVert_2 = 1.
$$

Here $x$ is the candidate, $v$ is its direction, and $r$ is its distance from $c$. The notation $U(0,R)$ means that distances anywhere between zero and $R$ are equally likely. Because $v$ has length one, the distance traveled is exactly $r$, regardless of how many coordinates $v$ uses.

For example, a move of length 0.5 could change one coordinate by 0.5. It could also change two coordinates by about 0.354 each: the combined distance is still $\sqrt{0.354^2+0.354^2}\approx0.5$. Those moves change different numbers of coordinates while traveling equally far.

Every support size uses the same distance distribution. For a paired comparison, we go further and reuse the actual distance draws across support sizes. At $k=1$, candidates move along a single coordinate axis. At $k=d$, every coordinate participates, giving ordinary cylindrical Thompson sampling, or CTS, in the absence of boundaries.

The **Step 1 generator and optimizer checks are complete**. They check that candidates change the requested number of coordinates, that directions have length one, that distances follow the intended rule, and that random supports overlap relevant coordinates as expected. These checks establish that the comparison is implemented correctly.

## What can we predict from a simple tilted plane?

Before studying curved landscapes or model errors, we ask what coordinate count should do on a tilted plane. A smooth objective looks approximately like a plane when viewed close enough to a point. This gives us a baseline prediction for the later experiments.

For this first calculation, imagine that we can evaluate every candidate using the true objective. The improvement delivered by the best candidate in the pool is its **oracle gain**. “Oracle” means we can identify the best point perfectly, without relying on the GP.

On a plane, the prediction is

$$
I_k = \max_{m\le M} r_m(-g^\top v_m), \qquad g=\nabla f(c).
$$

The pool contains $M$ candidates. The gradient $g$ describes the local slope, and $-g^\top v_m$ measures how strongly candidate $m$ points downhill. Multiplying by its distance $r_m$ gives its predicted improvement. The maximum picks the best improvement in the pool.

### Why could sparse moves help?

Suppose only 2 of 100 coordinates affect the objective. A candidate that changes one randomly chosen coordinate will usually miss both useful coordinates. But when it hits one, its entire move goes into that coordinate. A dense candidate always touches the useful coordinates, but spends much of its move on the other 98.

That tradeoff is central: sparse candidates have fewer useful hits, but a hit can be stronger. With thousands of candidates available, a few strong hits may be enough to produce a good best candidate.

*[Figure 2 of the target, not kept in this repository: Strip plots of per-candidate predicted gain for k equal to 1, 8, and 100 on a plane with two relevant coordinates: sparse pools have few non-zero candidates but the widest spread, and the best candidate is highest at k equal to 1. Generated in the hdbo project by studies/plot_sparse_cts_readable.py.]*

*Illustration computed from the plane model, one pool draw per row; not a measured Step 0 average. Each dot is one of 5,000 candidates, placed by its predicted gain; grey dots miss both relevant coordinates and sit at zero. Read each row's spread as how strong a hit can be and the annotation as how often a hit occurs. At $k=1$ only 2% of candidates hit, but those hits reach the largest gains and the best candidate (orange star) is best. At $k=100$ every candidate touches the relevant coordinates, yet the spread is narrow because most of each move goes to the 98 irrelevant ones. Setting: $d=100$, two relevant coordinates, $R=1$, unit gradient.*

This does not mean sparse directions put more movement into relevant coordinates on average. If $s$ coordinates are relevant, the expected fraction of squared direction length on them is $s/d$ for every $k$. What changes is how that movement is distributed across candidates. Since we select from a whole pool, the best available draw matters as well as the average draw.
