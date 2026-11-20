# Independent review: spectral gap, tangent rate, and Assouad spectrum

20 November 2026. Internal mathematical review of the proposed strengthening in `SPECTRAL_TANGENTS.md`. No existing definitions or manuscript claims were changed during this review. External review remains pending.

**Verdict:** the argument is sound with the qualifications and precise quantifiers below. For the displayed graph and membrane constructions, it proves a positive-power rate of full-ball convergence, an ordinary Assouad spectrum equal to three on some interval ending at one, and quasi-Assouad dimension three. It supplies no numerical spectral-gap constant, rate exponent, or transition parameter.

## 1. The cited theorem and its hypotheses

I checked Theorem 1.2 and Definition 2.1 of Benoist–de Saxcé, *A spectral gap theorem in simple Lie groups*, in the [author's final manuscript](https://www.math.univ-paris13.fr/~desaxce/publications/spectral_gap.pdf); the [published article](https://doi.org/10.1007/s00222-015-0636-2) appeared in 2016. The theorem assumes an adapted probability measure on a connected compact group with simple Lie algebra, and algebraic adjoint matrices for its support. It does **not** require the probability measure to be symmetric. The symmetry hypothesis in the final version's separate Theorem 1.1 must not be imported into, or omitted from, a statement of that different theorem.

Use G=SO(3). Identify its Lie algebra with vectors through the cross-product matrix v↦[v]×. Then Ad(O)[v]×=[Ov]×, so the adjoint matrix is exactly O in this basis. The graph core rotations and both membrane core rotations have rational entries. Their generated subgroups are dense, as established from irrational angles and two nonparallel rotation axes. The uniform probability measure on each finite core alphabet is therefore adapted and satisfies Theorem 1.2. No inverse rotations need to be added to the IFS.

Here spectral gap means spectral radius less than one on the mean-zero subspace of L²(G). Let σ be that radius. For any σ<ρ<1, the spectral-radius formula gives a finite C such that

\[
\|T_\mu^n\|_{L^2_0\to L^2_0}\le C\rho^n
\quad(n\ge0).
\]

It would be unjustified to replace this with a one-step operator-norm bound without a further argument. The bound on powers is all that is needed.

## 2. Exponential nets made of positive words of exact length

Choose a bi-invariant Riemannian metric on G and normalize Haar measure m(G)=1. Small radius-δ balls have measure vδ bounded above and below by positive constants times δ³. The constants are independent of the ball centre.

For an arbitrary target g∈G, let A=B(e,δ), B=B(g,δ). With Tμf(x)=∫f(xh)dμ(h), write both indicators as their means plus mean-zero functions. The correlation satisfies

\[
\langle\mathbf1_A,T_\mu^n\mathbf1_B\rangle
\ge v_\delta^2-C\rho^n v_\delta.
\]

Indeed, each centred indicator has L² norm at most √vδ. Fix c>0 with 3c<−logρ and put δ=e^(−cn). Then vδ≥c₀e^(−3cn), so the displayed correlation is strictly positive for every sufficiently large n, uniformly over g.

The measure μ to the convolution power n has finite support consisting of products of exactly n core generators, each with positive weight. Positive correlation therefore gives some x∈A and such a positive word w with xw∈B. Bi-invariance gives d(w,g)<2δ. Consequently **all sufficiently large exact word lengths** give a 2e^(−cn)-net of SO(3). This is not merely a net from signed words, words of bounded length, or a subsequence of lengths. Word coincidences do not affect the argument.

The action on a fixed unit vector is Lipschitz, so the corresponding segment directions form a C₁e^(−cn)-net of the sphere.

## 3. From the net to every small spatial scale

Suppose K contains the centred segment [−ae,ae], with a>0 and |e|=1, and is invariant under the common-scale central maps hᵢ(x)=qOᵢx, 0<q<1. For every positive word w of length n it contains

\[
aq^n[-O_we,O_we].
\]

For every sufficiently small R>0, choose the unique integer n such that

\[
aq^{n+1}<R\le aq^n.
\]

Those retained segments reach radius R. Their normalized portions inside the closed unit ball give an angular net with error at most C₁e^(−cn). With

\[
\alpha=\frac{c}{\log(1/q)}>0,
\]

we have e^(−cn)=(qⁿ)^α≤(R/(aq))^α. Hence

\[
d_H\left((K/R)\cap\overline B(0,1),\overline B(0,1)\right)
\le C_2 R^\alpha
\]

for every sufficiently small R, not just R=aqⁿ. A square seed contains a centred segment, so this proof covers both membranes without needing a separate estimate for plane normals.

For p=fᵥ(0), with contraction rᵥ, inclusion of fᵥ(K) gives the same exponent at p and a constant at most C₂rᵥ^(−α), valid below a correspondingly smaller scale. Thus the exponent can be common to the dense cylinder-centre set, while the multiplicative constant and starting scale may depend on the centre. A uniform estimate over all points or all centres is not established.

Additional attached maps do not invalidate this lower-approximation argument: the existing central copies remain inside K. It therefore also applies to the anchored membrane variant. Neither rationality of q nor freeness of the core rotation group is needed; the algebraic condition is on the rotation matrices.

## 4. Ordinary Assouad spectrum and quasi-Assouad dimension

For 0<θ<1, use the ordinary Assouad spectrum defined by the least s permitting a uniform bound

\[
N_{R^{1/\theta}}(K\cap B(x,R))
\le C(R/R^{1/\theta})^s
\]

over x∈K and sufficiently small R. Radius or diameter conventions for the covering sets change only constants. The upper spectrum, in which the small radius may range below R^(1/θ), is a different definition; the following proof already establishes the ordinary one.

Fix θ>1/(1+α) and put r=R^(1/θ). The absolute approximation error is at most C₂R^(1+α), and

\[
\frac{C_2R^{1+\alpha}}r
=C_2R^{1+\alpha-1/\theta}\longrightarrow0.
\]

Place a grid of points separated by 6r in B(0,R/2). For every sufficiently small R there are at least c₃(R/r)³ such points. Approximate them by points of K with error below r/4. These points remain in the open ball B(0,R), and distinct points are more than 2r apart. Every radius-r covering ball contains at most one of them. Therefore

\[
N_r(K\cap B(0,R))\ge c_3(R/r)^3.
\]

Since R/r tends to infinity, no uniform covering exponent below three is possible. The ambient upper bound gives

\[
\dim_A^\theta K=3
\quad\text{for every }\theta\in(1/(1+\alpha),1).
\]

In particular dim_qA K=3. This follows directly from the ordinary/upper-spectrum inequalities, or from [Fraser–Hare–Hare–Troscheit–Yu, Corollary 2.2](https://arxiv.org/pdf/1804.09607), which identifies the ordinary spectrum's limit at one with quasi-Assouad dimension. That primary source's definitions and corollary were checked.

## 5. Interpretation and limits

- This is a qualitative analytic theorem application, not a numerical estimate or a finite certificate. The project has no certified numerical value for σ, ρ, α, or the spectrum's actual transition point.
- The sufficient threshold 1/(1+α) is not asserted to be optimal. The rest of the spectrum has not been determined.
- Hausdorff dimension below three, zero volume, and maximal quasi-Assouad dimension are compatible: the spectrum records local covering complexity across related pairs of scales.
- The positive-word issue is essential because inverse similarities need not preserve K. The nonsymmetric theorem and the correlation argument resolve it for the existing map lists.
- The 2025 article [*Interpolating with generalized Assouad dimensions*](https://doi.org/10.1007/s12220-025-02099-w) discusses a broad-sounding question in its introduction, but its self-similar analysis in Section 4 is explicitly on the real line. This three-dimensional construction does not resolve that line-specific problem. No claim to settle an established open problem should be made from this comparison.
- Spectral-gap theory, quantitative rotation nets, and Assouad-spectrum theory are existing tools. Their application here strengthens the documented construction; it does not by itself establish historical novelty, a new fractal category, or priority for the combined result.

## 6. Separate finite certificate for the original membrane

I also reviewed `constructive/tangent_bounds/certify.py`, its saved witness data, and `certificate.json`. The analytic extension from that finite mesh to the full sphere is valid:

1. Every sphere direction radially lifts to a face of the cube [−1,1]³. On each face, the normalization map x↦x/|x| has derivative norm at most one, because |x|≥1 along every same-face segment. The square-cell centres therefore give a spherical mesh radius at most √2/m, strictly below 3/(2m).
2. The three positive cube faces suffice: antipodal replacement does not change absolute normal dot products. Face boundaries and coordinate ties cause no missing directions.
3. At each normalized mesh point u the selected exact unit normal n gives plane distance |n·u|. For a nearby direction v, the same normal gives |n·v|≤|n·u|+|v−u|. A floating-point nearest-plane proposal need not be globally optimal: verifying any valid witness with the stated bound is enough.
4. The orthogonal projection of a point in the unit ball onto a centred plane lies in its unit disk. Thus the plane-distance bound is an actual distance-to-retained-disk bound, not merely a bound to an infinite plane outside the retained patch.
5. The original square contains a unit disk. A core word of length ℓ≤n retains a disk of radius 4^(−ℓ)≥4^(−n). For every 0<t≤4^(−n), normalizing by t therefore includes each corresponding unit disk. Radial extension from the sphere covers the full unit ball.

The integer code verifies all normal lengths, selected rational dot-product squares, complete witness counts, hashes, and strict square-root upper enclosures. I reran

```text
python constructive/tangent_bounds/certify.py --verify
```

successfully for all five supplied certificates. At depth seven and m=200 the certified result is

\[
d_H\left((K_{1/4}/t)\cap\overline B,\overline B\right)
<0.009278720270
\qquad(0<t\le1/16384).
\]

This numerical bound concerns the origin of the **original eight-map denominator-125 membrane at q=1/4**. It is not a certified number for the norm-13 variant, the anchored image, the graph hero, or all centres uniformly. It proves one finite accuracy level, with several shallower levels also certified; it does not determine a spectral-gap constant or a power-law exponent. The spectral argument above and this finite certificate are complementary and logically separate.

## 7. A directly certified nonconstant spectrum

The spectrum is genuinely nonconstant, not merely known to be maximal near one. This follows from the finite similarity covering sum without assuming equality of Hausdorff and box dimensions.

Let D=diam K>0, let r_min be the smallest first-level contraction ratio, and suppose s>0 satisfies ∑ᵢrᵢˢ≤1. For 0<r<D, stop every address at its first word w with r_wD≤r. This is a finite complete prefix-free family. Repeatedly replacing a word by its children does not increase the sum of the s-powers of contraction ratios, so ∑_w r_wˢ≤1. Every stopped word satisfies r_w>r_min r/D. Its cylinder has diameter at most r, giving

\[
N_r(K)\le \#\{w\}
\le \left(\frac{D}{r_{\min}r}\right)^s.
\]

Consequently, with r=R^(1/θ), the same global cover bounds every local piece and yields

\[
\dim_A^\theta K\le
\min\left\{3,\frac{s}{1-\theta}\right\}.
\]

This is strictly below three whenever θ<1−s/3. The certified covering sums therefore imply:

| Member | Admissible s | Interval where the spectrum is strictly below three |
|---|---:|---:|
| 127-map hero | 17/8 | 0<θ<7/24 |
| 244-map thin graph | 23/12 | 0<θ<13/36 |
| Original eight-map membrane | 2.271554 | 0<θ<0.242815333… |

For the membrane the stated s is slightly above its elementary similarity root, so its original eight-map covering sum is below one; no overlap-cover argument is needed here. These upper bounds combine with Section 4's interval of spectrum value three to prove nonconstancy for each member. They do not locate the actual transition, determine the intermediate values, or establish a historically new spectral phenomenon.
