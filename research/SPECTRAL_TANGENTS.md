# Spectral gaps, quantitative ball tangents, and the Assouad spectrum

**Research note — 20 November 2026.** This is an analytic corollary developed during the publication review. It uses a deep published spectral-gap theorem and the retained-segment construction. Its constants are existential; no numerical spectral gap or transition threshold is certified here. A [separate internal review](SPECTRAL_TANGENTS_REVIEW.md) checked the argument; external mathematical review remains pending. It is not a claim of historical priority, a new category, or a resolution of a question about self-similar sets on the line.

## Statement

Let K be a compact subset of Euclidean three-space which contains the unit segment S=[−e,e], where |e|=1. Suppose that, for some 0<q<1, it is invariant in the inclusion sense under finitely many origin-fixing similarities

\[
h_j(x)=qQ_jx,\qquad h_j(K)\subset K,
\]

where the matrices Q_j belong to SO(3), have algebraic entries, and generate a dense subgroup of SO(3). Then there exist constants C>0, α>0 and R_0>0 such that

\[
H_0(R):=d_H\left((R^{-1}K)\cap\overline B(0,1),\overline B(0,1)\right)
\leq C R^\alpha\qquad (0<R<R_0). \tag{1}
\]

Consequently there is an existential θ_0<1 such that

\[
\dim_A^\theta K=3\quad\text{for every }\theta_0<\theta<1,
\qquad \dim_{qA}K=3. \tag{2}
\]

Here dim_A^θ is the ordinary Assouad spectrum, with small scale r=R^(1/θ), and dim_qA is the quasi-Assouad dimension. One may take θ_0=1/(1+α) for any exponent α obtained below. This is a sufficient threshold, not the actual transition point.

If K is a similarity attractor satisfying these hypotheses, (1) also holds at every cylinder centre p=f_w(0), with the same exponent α and with constants and starting scales depending on w. The centres are dense. There is no assertion of one uniform constant over all points of K, or of this tangent behaviour at every point.

## 1. The published input and its hypotheses

Benoist and de Saxcé's Theorem 1.2 gives a spectral gap for an adapted probability measure on a connected compact simple Lie group when every adjoint matrix of a support element is algebraic in a fixed Lie-algebra basis. Adapted means that the support generates a dense subgroup. Their spectral gap is defined by spectral radius strictly below one on the mean-zero subspace of L² of Haar measure. [Final author manuscript, Theorem 1.2 and Definition 2.1](https://www.math.univ-paris13.fr/~desaxce/publications/spectral_gap.pdf) · [Published article, Inventiones Mathematicae 205 (2016), 337–361](https://doi.org/10.1007/s00222-015-0636-2).

SO(3) is connected, compact and has simple Lie algebra. Under the standard identification of a vector v with its cross-product matrix [v]_×, the identity

\[
Q[v]_\times Q^{-1}=[Qv]_\times
\]

identifies Ad Q with Q itself. Thus the algebraicity requirement is satisfied by the stated rotation matrices.

Give each Q_j a strictly positive probability, for example the uniform distribution, and call the resulting measure μ. Its support generates SO(3) densely, so the theorem applies. Importantly, **Theorem 1.2 does not impose symmetry of μ**. The separate equivalence theorem numbered 1.1 in the final author manuscript does assume symmetry; that equivalence theorem is not the assertion invoked here. We must use the positive words that occur in the IFS, rather than assume that inverse rotations are also defining maps.

Let m be normalized Haar measure and define

\[
Tf(x)=\int f(xg)\,d\mu(g).
\]

By the spectral-radius formula, the theorem implies the existence of 0<ρ<1 and C_0<∞ such that

\[
\|T^n\|_{L^2_0\to L^2_0}\leq C_0\rho^n
\quad\text{for every integer }n\geq0. \tag{3}
\]

No claim that the one-step operator norm is less than one is needed. Choose ρ strictly above the spectral radius, then enlarge C_0 to handle the finitely many initial powers.

## 2. A positive-word net of exponential accuracy

Equip SO(3) with a bi-invariant Riemannian distance d_G. Its dimension is three, so there are positive constants a,b,δ_0 for which

\[
a\delta^3\leq v_\delta:=m(B_G(1,\delta))\leq b\delta^3
\qquad (0<\delta<\delta_0).
\]

For an arbitrary target g, let A=B_G(1,δ), B=B_G(g,δ), and put u=1_A−v_δ and v=1_B−v_δ. Haar invariance gives both balls the same measure and their centred indicators L² norms at most v_δ^(1/2). Consequently (3) gives

\[
\left|\langle T^n1_A,1_B\rangle-v_\delta^2\right|
\leq C_0\rho^n v_\delta. \tag{4}
\]

Choose any c>0 with 3c<−log ρ, and set δ_n=exp(−cn). For all sufficiently large n,

\[
C_0\rho^n<v_{\delta_n},
\]

so (4) is strictly positive, uniformly over g. The measure μ^{*n} has finite support consisting of products Q_{i_1}⋯Q_{i_n} of **exactly n positive letters**, each occurring with positive mass. Positivity of the correlation implies that, for some such word W and some x∈B_G(g,δ_n), one has xW∈B_G(1,δ_n). By bi-invariance and the triangle inequality,

\[
d_G(W,g^{-1})<2\delta_n.
\]

Since g is arbitrary, the exact-length positive words form a 2exp(−cn)-net of SO(3). Inversion of the target does not introduce inverse letters: g^{-1} still ranges over every possible target while W remains a positive word.

The action of SO(3) on the unit sphere is uniformly Lipschitz. Hence there is a constant C_1 such that the directions W e from those same length-n words form a C_1 exp(−cn)-net of the sphere. This is a covering statement; no distribution of point samples is substituted for the group estimate.

## 3. Retained segments give a power-law rate at every scale

Every positive central word of length n retains the centred segment

\[
q^n[-We,We]\subset K.
\]

For any 0<R≤q^n, the normalized set R^{-1}K therefore contains the complete unit segments in the length-n word directions. For a point ru in the unit ball, select a direction We within C_1 exp(−cn) of u. The corresponding point rWe is at most that distance away and remains in the unit ball. Thus

\[
H_0(R)\leq C_1e^{-cn}\qquad(0<R\leq q^n).
\]

For an arbitrary sufficiently small R, put

\[
n=\left\lfloor\frac{\log R}{\log q}\right\rfloor.
\]

Because log q<0, this gives q^{n+1}<R≤q^n. With

\[
\alpha=\frac{c}{\log(1/q)}>0,
\]

we have

\[
e^{-cn}=(q^n)^\alpha\leq q^{-\alpha}R^\alpha.
\]

This proves (1), with C=C_1q^{-α}. It establishes the rate through **all** sufficiently small R, not only R=q^n.

If f_w(x)=r_wO_wx+p, then f_w(K)⊂K gives

\[
\frac{K-p}{R}\cap\overline B
\supset O_w\left(\frac{K}{R/r_w}\cap\overline B\right).
\]

Consequently H_p(R)≤C r_w^(−α)R^α for 0<R<r_wR_0. The exponent transfers unchanged, but the factor r_w^(−α) and the valid scale interval depend on the cylinder. This is the stated nonuniform dense-centre result.

## 4. Consequence for the Assouad spectrum

For 0<θ<1, the ordinary Assouad spectrum uses the covering relation

\[
N_{R^{1/\theta}}(K\cap B(x,R))
\leq C_\theta\left(R/R^{1/\theta}\right)^s
\]

uniformly over x∈K and all sufficiently small R; its value is the infimum of admissible s. Every subset of a ball in Euclidean three-space obeys the corresponding ambient upper exponent three.

Fix θ with β:=1/θ−1<α, and put r=R^(1/θ). From (1), every point of B(0,R) is within C R^(1+α) of K∩B(0,R). Since

\[
\frac{C R^{1+\alpha}}r=C R^{\alpha-\beta}\longrightarrow0,
\]

for sufficiently small R this error is less than r/4. Take a 4r-separated cubic grid inside B(0,R/2). It has at least c_2(R/r)^3 points. Approximate each grid point by a point of K. These approximating points are inside the open ball B(0,R) once R is small, so closed versus open clipping does not affect this step. The resulting points are more than 2r apart, so a radius-r ball covers at most one. Therefore

\[
N_r(K\cap B(0,R))\geq c_2(R/r)^3.
\]

Because R/r→∞ as R→0, no exponent s<3 satisfies the uniform spectral covering inequality. The ambient upper bound supplies the reverse inequality. Thus dim_A^θ K=3 whenever θ>1/(1+α).

Fraser, Hare, Hare, Troscheit and Yu prove that the ordinary Assouad spectrum tends to the quasi-Assouad dimension as θ increases to one. Together with the just-proved final interval on which the spectrum is three, this gives dim_qA K=3. [Primary paper, Corollary 2.2](https://arxiv.org/pdf/1804.09607).

### The spectrum is nonconstant

For a finite similarity IFS, any exponent s with \(\sum_i r_i^s\leq1\) gives the global bound \(N_r(K)\leq C r^{-s}\). Stop each address at its first cylinder of diameter at most r. These words have ratios bounded below by a fixed multiple of r, and their total s-weight is at most one, so their number is at most \(C r^{-s}\). This argument does not assume separation or equality of Hausdorff and box dimensions.

Substituting \(r=R^{1/\theta}\) gives

\[
\dim_A^\theta K\leq\min\left\{3,\frac{s}{1-\theta}\right\}.
\]

Since the constructions have a certified s<3, their spectrum is strictly below three for \(0<\theta<1-s/3\), whereas the spectral-gap argument gives three sufficiently near one. It is therefore **nonconstant**. For the hero, s=17/8 gives the explicit nonmaximal interval \(0<\theta<7/24\); for the thin linked member, s=23/12 gives \(0<\theta<13/36\). These intervals are sufficient bounds, not the exact transition. The separate review checks the stopping argument and constants.

## 5. Applicability to the defined constructions

- **Graph family and selected Borromean members.** The source segment contains a unit centred segment. The central block I,R_x,R_y,R_z is rational and generates SO(3) densely: the irrational-angle rotation circles about two perpendicular axes already suffice. All four maps have the same ratio q. The statement applies to the selected q=1/8 members and to the general graph construction's q=1/(4m²). Extra edge and axial maps do not invalidate the inclusion hypotheses.
- **Eight-map membrane.** The retained square contains a unit centred segment. Its four rational central matrices Q_k generate SO(3) densely, using the two nonparallel axes proved in the manuscript. Their common ratio q satisfies 0<q<1/2. Hence the conclusion applies for every such q, whether or not q itself is algebraic: the spectral-gap hypothesis concerns the rotation matrices.
- **Norm-13 and anchored variants.** The norm-13 central rotation has rational entries, irrational rotation angle, and nonparallel C4-conjugate axes. The anchored variants retain the reference central block and square. The same argument applies whenever those maps and the seed remain present. Their separate dimension upper bounds must still be used.

Accordingly these examples combine dim_qA=3 with Hausdorff dimension strictly below three. Their sufficiently thin graph members have topological dimension one and their membrane members topological dimension two. In the graph family the Hausdorff upper bound can approach one; in the membrane family it can approach two. As q decreases, the sufficient rate exponent c/log(1/q) decreases and the supplied sufficient spectrum threshold approaches one. No sharp parameter formula follows from this observation.

## 6. Context and limits of originality

Full Assouad dimension with arbitrarily small Hausdorff dimension already occurs for explicit finite self-similar systems in Fraser–Henderson–Olson–Robinson, Section 4.2. Retaining curves or sheets and proving quantitative pointwise convergence is the additional structure studied here, rather than a new discovery of a Hausdorff–Assouad gap. [Primary paper](https://arxiv.org/pdf/1404.1016).

The spectral-gap mechanism is also established theory. Lindenstrauss and Varjú already apply rotation spectral gaps to Euclidean isometry walks and self-similar measures. Their work provides an important precedent for combining these subjects; the present short implication concerns retained radial subsets and local covering numbers, not the invention of spectral-gap applications to fractals. [Primary paper](https://arxiv.org/abs/1405.4426).

Orgoványi and Rutar's *Two-scale branching functions and inhomogeneous attractors* gives spectrum formulas for inhomogeneous constructions subject to its minimally-distorting and asymptotically-bounded hypotheses. Its standard conformal examples satisfy the open set condition; another listed case concerns exponentially separated similarities on the line. Those results cannot be applied here merely because a segment or square acts as a retained seed. The common-centre overlap block requires its own hypothesis check. [Primary author manuscript, Theorems D–E and Section 4.1](https://rutar.org/papers/inhomogeneous_assouad_spectra.pdf).

The 2025 article *Interpolating with generalized Assouad dimensions* discusses the possibility that self-similar spectra equal box dimension. Its surrounding deterministic discussion and Section 4 concern similarities of the line. No claim is made that the spatial examples here answer that one-dimensional question. A precise comparison would require the intended ambient-space scope and the actual statement, not an isolated sentence. [Primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC12255623/).

A focused additional search did not locate this exact retained-segment corollary stated as an Assouad-spectrum example. That is not evidence of priority: the result may be a known or immediate application of the cited spectral-gap machinery. Treat it as an explicit analytic corollary with unresolved historical originality.

The substantial remaining quantitative questions are the actual Assouad spectrum, its first transition to three, effective numerical bounds for the positive-word angular net, and comparison with sets arising from other presentations. Nothing here establishes an exact Hausdorff dimension, classifies the whole topology, supplies a numerical value of α or θ_0, or asserts uniform full-ball behaviour at every point of K.
