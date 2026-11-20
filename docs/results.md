# Results and their scope

The mathematical arguments concern the infinite attractors. Exact arithmetic checks support specific finite claims; images illustrate finite approximations. Independent external mathematical review is pending.

## A full ball in the zoom limit

At a dense set of cylinder centres \(p=f_w(0)\), both central-rotation constructions satisfy

\[
\lim_{t\downarrow0}d_H\left(((K-p)/t)\cap\overline B(0,1),\overline B(0,1)\right)=0.
\]

The limit holds through every sufficiently small scale at these fixed centres. It does not assert that every point has this behaviour, or that a finite-scale piece contains a ball.

The proof is short. Retained centred segments or disks occur in dense orientations. Choose finitely many directions giving any desired accuracy. Their positive radii have a positive minimum. Below that radius, every normalized view contains the entire chosen directional net. The result transfers to all cylinder centres, which are dense in K.

These full-ball tangents force Assouad dimension three, even though the original sets have zero volume.

## Quantitative zoom bounds and the Assouad spectrum

The stated graph and membrane constructions admit a stronger conclusion. Their central rotations have algebraic entries and generate a dense subgroup of SO(3). An analytic corollary of [Benoist–de Saxcé's spectral-gap theorem, Theorem 1.2](https://www.math.univ-paris13.fr/~desaxce/publications/spectral_gap.pdf) gives, at each cylinder centre p,

\[
d_H\left(((K-p)/R)\cap\overline B,\overline B\right)\leq C_p R^\alpha
\]

for all sufficiently small R, with some common exponent \(\alpha>0\). The constant and starting scale may depend on the centre. The exponent is existential: no numerical value of α or spectral-gap constant has been computed.

Consequently the ordinary Assouad spectrum is three for every θ sufficiently close to one, and the quasi-Assouad dimension is three. The sufficient condition is \(\theta>1/(1+\alpha)\); neither a numerical threshold nor the actual transition point is known. The [derivation](../research/SPECTRAL_TANGENTS.md) and [independent internal review](../research/SPECTRAL_TANGENTS_REVIEW.md) state the hypotheses and distinguish this analytic corollary from a claim of historical originality.

The spectrum is also **nonconstant**. A global cylinder cover gives \(\dim_A^\theta K\leq\min\{3,s/(1-\theta)\}\) for a certified covering exponent s<3. For example, the hero's spectrum is strictly below three when \(0<\theta<7/24\), and is three sufficiently near one. This separates two regimes without locating their exact transition.

Separately, exact finite computations give explicit bounds for the **original eight-map membrane with q=1/4**. Write K for that reference attractor and B for the closed unit ball. At the origin, the following inequalities hold for **every** positive t below the corresponding threshold:

| Maximum core-word depth | Scale threshold | Strict upper bound on \(d_H((K/t)\cap B,B)\) |
|---|---|---|
| 5 | t ≤ 1/1024 | 0.092423119034 |
| 6 | t ≤ 1/4096 | 0.021264176895 |
| 7 | t ≤ 1/16384 | 0.009278720270 |

The final row is less than one percent of the ball radius. These are bounds on the infinite set, not pixel measurements or assertions that it contains a solid ball. They do not apply unchanged to the 12-map anchored visual variant. Integer arithmetic checks 120,000 directional witnesses per depth, while a proved mesh-radius bound covers the directions between them. See the [proof and reproduction instructions](../constructive/tangent_bounds/README.md) and [full certificate](../constructive/tangent_bounds/certificate.json). This finite certificate does not supply the unknown asymptotic exponent α.

## Graph family

Any finite connected polygonal spatial graph can be retained inside a connected finite similarity attractor. With sufficiently fine edge subdivisions and sufficiently small central contractions, for every \(\varepsilon>0\) one obtains

\[
1<\dim_H K<1+\varepsilon,\qquad\dim_AK=3.
\]

The construction can be chosen with topological dimension one. Every neighbourhood contains a similar copy of the prescribed graph. The specific visually rendered members need not be the small-dimension members used in this existence statement.

For the original m=2, q=1/4 Borromean extension, exact scalar checks certify \(\dim_HK<13/5\). Its exact Hausdorff dimension and full topological classification are unknown.

The hero uses the 127-map m=3 member with six axial subdivisions and q=1/8, for which \(\dim_HK<17/8\). The finer 244-map m=6 member with the same axial and central parameters has \(\dim_HK<23/12<2\), certifying topological dimension one. These are separate recipes; the latter bound is not assigned to the hero. See the [variant definitions](../survey/VARIANTS.md) and [thin-member certificate](../survey/low-dimension-exact-certificate.json).

## Membrane family

For every \(0<q<1/2\), the membrane has topological dimension two, Assouad dimension three, and zero ordinary volume. Its Hausdorff dimension satisfies

\[
2<\dim_HK_q\leq s_q<3,\qquad4\cdot2^{-s_q}+4q^{s_q}=1.
\]

At q=1/4 the elementary upper bound is \(1+\log_2(1+\sqrt2)\approx2.271553303\). The exact-overlap calculation below improves it strictly. Neither bound is an exact dimension. As q tends to zero, the elementary bound tends to two. Every relative neighbourhood contains genuine planar patches in a dense set of orientations.

The strict lower bounds use [Farkas–Fraser, Corollary 3.1](https://arxiv.org/pdf/1411.0867): positive critical Hausdorff measure of a finite self-similar set implies Ahlfors regularity without a separation assumption. A retained interval or square rules out equality to one or two, respectively, because regularity would contradict the Assouad dimension gap.

## Exact overlaps and a sharper bound

The original q=1/4 membrane has an exactly verified affine-word coincidence:

```text
47131103333 = 12222011470
```

Digits 0–3 denote the four tiling maps and 4–7 the central rotations; words are outermost first. This is equality of complete affine maps, not merely an intersection between copies. The common contraction ratio is \(2^{-13}\).

A family of 32 such relations permits a smaller cylinder cover. Exact rational root and logarithm bounds give

\[
2<\dim_HK_{1/4}<2.271553252338126.
\]

The improvement is small but strict, proving that the elementary similarity bound is not attained. A separately defined norm-13 rotation variant has a six-letter relation and upper bound 2.270907424784688. It is not the reference rotation. See the [full derivation and certificates](../constructive/overlaps/OVERLAPS.md). These are internally checked results, pending external review.

## What the visible sheets leave out

Let D be the union of all finite-word square images, and E the remainder \(K\setminus D\). Then D is dense, meagre, and has Hausdorff dimension exactly two. E is a dense Gδ set carrying the full Hausdorff dimension of K, which is strictly greater than two. Finite sheet renders omit those residual points even though the sheets approximate the entire attractor in Hausdorff distance.

At the actual dimension \(d=\dim_HK\), the critical measure \(\mathcal H^d(K)\) is zero. Otherwise the same Farkas–Fraser theorem would force Ahlfors regularity and erase the dimension gap. “Carries the dimension” therefore does not mean positive critical Hausdorff measure. The [residual-set proof](../constructive/overlaps/OVERLAPS.md) records this distinction.

## Separation and alternative descriptions

The gap \(\dim_HK<\dim_AK=3\) excludes every alternative finite similarity presentation satisfying the weak separation property, and therefore excludes an open-set-condition presentation. The applicable [Fraser–Henderson–Olson–Robinson Theorem 1.4](https://arxiv.org/pdf/1404.1016) requires full affine span, which both constructions have.

This is a property of the set. A list of maps may also have its own exact overlaps or redundant words; those presentation-level questions are distinct and remain under investigation.

## What has been checked

- [Rational scalar bounds](../survey/verify_exact.py) verify the reported enclosures and selected dimension inequalities.
- [The link certificate](../research/LINK_CHECK.md) uses exact crossings and Fox 3-colourings, together with a geometric pairwise separation argument.
- [Independent internal review](../research/INDEPENDENT_REVIEW.md) audits the arguments and independently enumerates the colouring assignments.
- [The manuscript](paper.md) gives the general constructions and proof dependencies.

Containing an embedded link does not classify the topology of the whole attractor or its complement. Historical originality and exact Hausdorff dimensions are not established.
