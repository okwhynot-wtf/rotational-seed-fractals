# Retained graphs and membranes in self-similar spatial continua

**Research draft — 20 November 2026.** This document presents explicit constructions and proofs assembled during an exploratory investigation. It does not claim invention of a new category of fractal. Historical priority, exact overlaps, and several geometric questions remain under investigation. The draft has received internal mathematical and computational checks, not external peer review.

## Abstract

We describe two finite similarity constructions in three-dimensional Euclidean space. Both retain a simple geometric seed as an exact subset and add contracting rotations about a common point. The first can contain any prescribed finite connected polygonal spatial graph while having Hausdorff dimension strictly between one and an arbitrarily chosen number greater than one. The second retains a square and has topological dimension two, with Hausdorff dimension strictly between two and three and tending towards two in an upper-bound sense. Both are connected, have zero volume, and admit a dense set of points at which every normalized small-scale view converges in Hausdorff distance to the full unit ball. Thus their Assouad dimension is three. A corollary of the Benoist–de Saxcé spectral-gap theorem gives a positive-power convergence rate, an Assouad spectrum equal to three sufficiently near parameter one, and quasi-Assouad dimension three; the exponent and transition threshold remain nonnumerical. A graph example retains a rectangular Borromean link, and an eight-map membrane example has exact fourfold rotational symmetry. These are concrete combinations of established IFS, tangent, spectral-gap, and dimension theory; their exact dimensions and full topological classifications are not determined.

## 1. Framework and meaning of the claims

A finite similarity iterated function system consists of maps

\[
f_i(x)=r_i O_i x+b_i,\qquad 0<r_i<1,\quad O_i\in SO(3).
\]

It has a unique nonempty compact attractor satisfying

\[
K=\bigcup_{i=1}^N f_i(K).
\]

For a word \(w=i_1\cdots i_k\), write \(f_w=f_{i_1}\circ\cdots\circ f_{i_k}\), with the rightmost map acting first. Each \(f_w(K)\) is literally a smaller similar copy of the entire set, and word diameters tend to zero along every infinite address. Existence, uniqueness, and convergence of compact-set iteration are the standard contraction framework of [Hutchinson, *Fractals and Self-Similarity*](https://maths-people.anu.edu.au/~john/Assets/Research%20Papers/fractals_self-similarity.pdf).

We distinguish Hausdorff dimension \(\dim_H\), which measures small-scale size, from Assouad dimension \(\dim_A\), which bounds the worst local covering complexity over all locations and pairs of scales. The covering equation

\[
\sum_i r_i^s=1
\]

always supplies a Hausdorff-dimension upper bound. Equality is not assumed here: the constructions have substantial overlap.

Let \(B=\overline B(0,1)\). The basic local assertion in this draft is

\[
\lim_{t\downarrow0}d_H\left(\frac{K-p}{t}\cap B,B\right)=0. \tag{1}
\]

Here \(d_H\) is Hausdorff distance between compact sets. Equation (1) concerns every sufficiently small positive scale at the fixed centre \(p\). It is stronger than finding a full-ball weak tangent along selected scales with moving centres, and stronger than a statement about limiting directions alone. It does not imply that any finite-scale piece has positive volume or contains a ball.

## 2. Two elementary construction lemmas

**Retained-seed lemma.** Suppose a subsystem has attractor \(S\). The attractor of the complete system contains \(S\), hence contains every \(f_w(S)\).

For example, two half-interval maps retain a segment, while four half-scale square maps retain a square. Subsequent maps copy the entire eventual attractor, not merely the seed; the seed is used to certify attachments and literal geometry inside those copies.

**Full-ball lemma.** Suppose \(K\) contains the centred unit segment \([-e,e]\), and similarities fixing zero give retained segments

\[
\rho_w[-O_we,O_we]\subset K,\qquad \rho_w>0,
\]

whose directions \(O_we\) are dense on the sphere. Then (1) holds at zero.

To prove this, fix \(\varepsilon>0\) and choose finitely many directions forming an \(\varepsilon\)-net of the sphere. Their retained segment radii have a positive minimum \(\delta\). For every \(0<t\leq\delta\), the normalized set contains the corresponding unit segments. A point \(ru\in B\) lies within \(r\varepsilon\leq\varepsilon\) of one of them. The reverse Hausdorff distance is zero because the normalized set is clipped to \(B\).

The conclusion transfers from zero to every cylinder centre \(p=f_w(0)\): writing \(f_w(x)=rOx+p\),

\[
\frac{K-p}{t}\cap B\supset O\left(\frac{K}{t/r}\cap B\right).
\]

These centres are dense in \(K\), since an address prefix containing any chosen point has arbitrarily small diameter. A square seed also suffices, since it contains a centred segment. A dense collection of retained centred disks gives the same argument using plane normals.

Finally, (1) implies \(\dim_A K=3\). Arbitrarily fine finite grids in the ball are approximated by separated points in a normalized piece of \(K\), precluding any uniform Assouad covering exponent smaller than three.

### 2.1 A spectral-gap corollary

For the constructions below, the common-scale central rotations have algebraic entries and generate a dense subgroup of \(SO(3)\). [Benoist–de Saxcé, Theorem 1.2](https://www.math.univ-paris13.fr/~desaxce/publications/spectral_gap.pdf) supplies a spectral gap for the probability measure supported on those rotations. Its statement applies without requiring inverse letters in the support. The resulting decay of powers on mean-zero \(L^2\) gives exponentially fine direction nets from positive words of each sufficiently large exact length.

The retained segments then yield, for some \(\alpha>0\),

\[
H_p(R):=d_H\left(((K-p)/R)\cap B,B\right)
\leq C_pR^\alpha
\]

at every cylinder centre \(p=f_w(0)\), for all sufficiently small \(R\). The exponent can be common to those centres; the constants and starting scales depend on the cylinder. Neither a numerical exponent nor a uniform estimate over all points of \(K\) is asserted.

The ordinary Assouad spectrum uses small radius \(r=R^{1/\theta}\). If \(\theta>1/(1+\alpha)\), then the absolute approximation error \(O(R^{1+\alpha})\) is \(o(r)\). Approximating a separated grid in \(B(0,R/2)\) therefore requires order \((R/r)^3\) radius-r balls. The ambient upper bound proves

\[
\dim_A^\theta K=3\quad\text{for every sufficiently large }\theta<1,
\qquad \dim_{qA}K=3.
\]

The quasi-Assouad conclusion uses the limiting relation in [Fraser–Hare–Hare–Troscheit–Yu, Corollary 2.2](https://arxiv.org/pdf/1804.09607). The [full derivation](../research/SPECTRAL_TANGENTS.md) and [separate internal review](../research/SPECTRAL_TANGENTS_REVIEW.md) check the hypotheses, positive-word argument, and all-scale quantifiers. The sufficient threshold is existential, and the actual transition in the spectrum is undetermined. This is an application of established spectral-gap theory with unresolved historical originality, not an assertion of a new category.

The spectrum is nonconstant. For any covering exponent s<3 with \(\sum_i r_i^s\leq1\), a stopping-word cover has at most \(C r^{-s}\) cylinders of diameter at most r: the stopped ratios are bounded below by a fixed multiple of r and their total s-weight is at most one. Consequently

\[
\dim_A^\theta K\leq\min\{3,s/(1-\theta)\}<3
\qquad(0<\theta<1-s/3).
\]

Together with the plateau at three near one, this proves nonconstancy without assuming equality of Hausdorff and box dimensions. The hero's exponent s=17/8 gives the explicit interval \(0<\theta<7/24\) on which the spectrum is below three. The actual transition remains undetermined.

## 3. A graph construction with Hausdorff dimension near one

**Theorem A.** For every finite connected polygonal graph \(G\subset\mathbb R^3\) and every \(\varepsilon>0\), there is a finite similarity attractor \(K\) such that:

1. \(G\subset K\), and \(K\) is path connected;
2. \(1<\dim_H K<1+\varepsilon\) and \(\dim_A K=3\);
3. \(K\) can be chosen to have topological dimension one and zero volume;
4. equation (1) holds at a dense set of cylinder centres;
5. every neighbourhood of every point of \(K\) contains a similar copy of the prescribed graph.

Any chosen finite cyclic rotational symmetry can additionally be imposed by including the corresponding finite orbits of the construction. This proves that the symmetry is present, not that it is the full symmetry group.

### 3.1 Exact recipe

Let \(e=(0,0,1)\) and \(S=[-e,e]\). Join \(G\) to \(S\) by a finite polygonal path if necessary. Denote the resulting connected finite graph by \(\Gamma\). Split crossings and overlapping edges into a finite edge decomposition, so \(\Gamma\) is the union of \(S\) and finitely many additional nondegenerate segments of lengths \(\ell_1,\ldots,\ell_E\). Put \(L=\sum_j\ell_j\).

Retain \(S\) with

\[
a_\pm(x)=\tfrac12x\pm\tfrac12e.
\]

For an integer \(m\geq1\), divide edge \(j\) into \(n_j=\lceil m\ell_j\rceil\) equal pieces. For each oriented piece \(U\to V\), choose a proper rotation \(O_{UV}\) with

\[
O_{UV}e=\frac{V-U}{|V-U|},
\]

and include

\[
f_{UV}(x)=\frac{|V-U|}{2}O_{UV}x+\frac{U+V}{2}. \tag{2}
\]

Then \(f_{UV}(-e)=U\) and \(f_{UV}(e)=V\). The choice of rotation about the target edge is a free roll parameter.

Add four central similarities

\[
h_0(x)=q_mx,\quad h_x(x)=q_mR_xx,\quad h_y(x)=q_mR_yx,\quad h_z(x)=q_mR_zx,
\qquad q_m=\frac1{4m^2}, \tag{3}
\]

where \(R_x,R_y,R_z\) are rotations about the coordinate axes with

\[
\cos\theta=\frac35,\qquad\sin\theta=\frac45.
\]

All maps are strict contractions. For rational graph vertices, a reproducible orthonormal-frame choice in (2) gives algebraic coefficients; (3) has rational coefficients. The existence statement permits arbitrary real graph coordinates.

### 3.2 Containment and connectivity

The interval subsystem gives \(S\subset K\), and (2) gives every subdivided edge of \(\Gamma\) as an exact subset of \(K\).

For a direct connectivity proof, begin compact-set iteration at \(\Gamma\). The two axial images meet at zero and cover \(S\). Every edge image contains its target segment in \(\Gamma\); every central image contains zero. The union therefore contains \(\Gamma\), and each connected image meets that connected graph. Repeating the argument gives connected iterates converging to connected \(K\).

Path connectedness follows from the same attachment data. Every map centre \(f_i(0)\) lies on \(\Gamma\), so choose a polygonal path in \(\Gamma\) from zero to each centre. For an infinite address, successive images of these finitely many paths join consecutive cylinder centres. Their lengths decrease geometrically, and the centres converge to the addressed point. Concatenation gives a continuous, indeed finite-length, path from zero to that point.

### 3.3 Dense directions and every-scale tangents

The angle \(\theta/\pi\) is irrational: otherwise \(2\cos\theta=6/5\) would be a rational algebraic integer and thus an integer. Positive powers of \(R_x\) and \(R_y\) are dense in their respective circle subgroups. Their positive semigroup is dense in \(SO(3)\), because a closed subsemigroup of a compact group is a subgroup and rotations about the two axes generate \(SO(3)\).

The central words retain segments \(q_m^{|w|}R_w(S)\) in a dense collection of directions. The full-ball lemma proves (1) at zero and all cylinder centres, and hence \(\dim_A K=3\).

### 3.4 Dimension bounds

The number of edge maps is at most \(mL+E\), and each edge contraction ratio is at most \(1/(2m)\). For \(s>1\),

\[
\sum_i r_i^s\leq 2^{1-s}+(mL+E)(2m)^{-s}+4(4m^2)^{-s}. \tag{4}
\]

For fixed \(s>1\), the right side tends to \(2^{1-s}<1\). Set \(\eta=\min\{\varepsilon,1\}\) and choose sufficiently large \(m\) so (4) is less than one at \(s=1+\eta\). The usual cylinder covers then give \(\dim_H K<1+\eta\leq1+\varepsilon\). In particular \(\dim_H K<2\), so the retained interval and \(\dim_{\rm top}K\leq\dim_HK\) give topological dimension one. Zero three-dimensional volume follows.

The strict lower bound uses a cited regularity theorem, rather than the covering calculation. Farkas–Fraser Corollary 3.1 implies that an ordinary finite self-similar set with positive measure in its Hausdorff dimension is Ahlfors regular, without a separation assumption. If \(\dim_HK=1\), the retained interval gives positive critical measure; Ahlfors 1 regularity would imply \(\dim_AK=1\), contradicting the full-ball tangent. Thus \(\dim_HK>1\). [Farkas–Fraser, primary paper](https://arxiv.org/pdf/1411.0867).

For symmetry, take the finite orbit of \(\Gamma\) around the source axis and include the conjugate orbit of every edge and central map. The axial subsystem remains unchanged; the other terms in (4) gain only a fixed factor. The same limit argument applies. A deep cylinder containing a point has small diameter and contains a copy of \(G\), proving the neighbourhood claim.

## 4. A concrete Borromean member

The implemented spatial example uses source endpoints \(A=(-1,-1,-1)\), \(B=(1,1,1)\) and the order-three rotation \(T(x,y,z)=(z,x,y)\). Let \(L_0\) be the rectangle with corners

\[
(-2,-1,0),\ (2,-1,0),\ (2,1,0),\ (-2,1,0),
\]

and set \(L_1=T(L_0)\), \(L_2=T^2(L_0)\). Three bridges join \(B\) to \((1,1,0)\) and its rotated images. Dividing all ring and bridge edges into length \(1/m\) pieces gives \(39m\) edge maps, each of ratio \(1/(2m\sqrt3)\), plus two axial maps. Four central maps give the tangent extension.

The three selected loops are disjoint planar unknots and pairwise unlinked. For instance, the spanning disk \([-2,2]\times[-1,1]\times\{0\}\) misses \(L_1\); a thin regular neighbourhood separates that pair. A rational projection yields a regular twelve-crossing diagram whose Fox 3-colouring system has three solutions, compared with 27 for the three-component unlink. Each pair has nine colourings. The geometric separation argument and the full-link count establish the nonsplittable Brunnian property of the specified rectangular arrangement.

For \(m=2\), \(q=1/4\), the original system has 84 maps and a numerical covering root about 2.56264511; exact scalar inequalities certify \(\dim_HK<13/5\). The published hero uses a different member: \(m=3\), six axial subdivisions, and \(q=1/8\), with 127 maps and certified \(\dim_HK<17/8\). Its exact recipe is linked in Section 8. Neither of these members is claimed to have topological dimension one. A finer member with \(m=6\), six axial subdivisions, and \(q=1/8\) has 244 maps and certified \(\dim_HK<23/12<2\), which does establish topological dimension one. Their exact Hausdorff dimensions remain undetermined.

Every cylinder contains a similar copy of the selected link. The full attractor is connected, and additional points may fill surfaces or connect paths around those curves. Containment of a link therefore does not determine the topology of \(K\), prove that its loops are essential in \(K\), or classify \(\mathbb R^3\setminus K\).

## 5. An eight-map fourfold membrane

Let \(S=[-1,1]^2\times\{0\}\), and define four tiling similarities

\[
f_{ab}(x)=\tfrac12x+(a/2,b/2,0),\qquad a,b\in\{-1,1\}.
\]

Let \(Z\) be the rotation through \(\pi/2\) about the z axis and put

\[
Q=\frac1{125}
\begin{pmatrix}
53&-60&96\\
60&-75&-80\\
96&80&-3
\end{pmatrix},\qquad
Q_k=Z^kQZ^{-k},\qquad h_k(x)=qQ_kx,
\quad k=0,1,2,3,
\tag{5}
\]

where \(0<q<1/2\). For rational \(q\), every coefficient is rational. Let \(K_q\) be the eight-map attractor.

**Theorem B.** The set \(K_q\) is path connected, has fourfold rotational symmetry, topological dimension two, and zero volume. Its dimensions satisfy

\[
2<\dim_HK_q\leq s_q<3,\qquad \dim_AK_q=3,
\]

where \(s_q\) solves \(4\cdot2^{-s_q}+4q^{s_q}=1\) and \(s_q\downarrow2\) as \(q\downarrow0\). Every relative neighbourhood contains actual planar square patches in a dense set of orientations. Equation (1) holds at every cylinder centre.

**Proof.** The tiling subsystem retains \(S\). All four central images contain zero. Connected-set iteration, or the path argument above, proves connectivity. Conjugation by \(Z\) permutes the eight maps, so uniqueness gives \(Z(K_q)=K_q\).

The matrix \(Q\) is a proper rotation about \((4/5,0,3/5)\), with cosine \(-3/5\) and sine \(4/5\). Its angle is again an irrational multiple of \(\pi\). The closure of the positive semigroup contains the full rotation circles generated by \(Q_0\) and \(Q_1\). Their axes \((4/5,0,3/5)\) and \((0,4/5,3/5)\) are nonparallel. Their infinitesimal rotations and Lie bracket span \(\mathfrak{so}(3)\), so the closed group is \(SO(3)\).

Consequently the normals of the centred squares \(h_w(S)\) are dense. The full-ball lemma applies. Every cylinder also contains the rotated square subsystem, so the density of orientations persists inside every relative neighbourhood. The countable union of all retained square copies is dense in \(K_q\). Section 5.1 describes its residual complement; that complement's topology remains undetermined.

The covering sum equals \(1/2+4q^3<1\) at exponent three, hence \(s_q<3\). The square gives \(\dim_HK_q\geq2\). Equality to two would, by the same verified Farkas–Fraser regularity argument used above, imply Assouad dimension two, a contradiction. The topological-dimension inequality and the retained square then force \(\dim_{\rm top}K_q=2\).

At \(q=1/4\), the explicit upper bound is

\[
2<\dim_HK_{1/4}\leq1+\log_2(1+\sqrt2)
=2.271553303163612\ldots.
\]

The upper bound is not asserted to be the dimension. For any \(\varepsilon>0\), sufficiently small positive \(q\) gives \(2<\dim_HK_q<2+\varepsilon\).

### 5.1 Exact overlaps and the residual set

At \(q=1/4\), exact rational composition verifies the affine-map equality

```text
47131103333 = 12222011470.
```

Here digits 0–3 are the square maps in sign order \((-,-),(-,+),(+,-),(+,+)\), digits 4–7 are \(h_0,\ldots,h_3\), and words are outermost first. Both sides contract by \(2^{-13}\). Thirty-two symmetry and sign variants yield a lexicographically decreasing rewriting rule. Their forbidden left patterns have no proper prefix–suffix overlaps. The resulting weighted cover recurrence proves

\[
2<\dim_HK_{1/4}<2.271553252338126.
\]

The last decimal is a certified upper endpoint, obtained with rational polynomial and logarithm bounds. It is not an exact dimension. The [overlap report](../constructive/overlaps/OVERLAPS.md) gives the recurrence proof and exact certificates, as well as a separately defined norm-13 rotation variant with a shorter relation. These equalities coexist with free core rotation generators: inserting tiling maps changes the translations without changing the ordered core rotation subsequence.

For any \(q\) in Theorem B, put \(D=\bigcup_w f_w(S)\), including the empty word, and \(E=K_q\setminus D\). The set \(D\) is dense and has Hausdorff dimension two. Each square is closed with empty relative interior, since every relative neighbourhood contains patches with dense orientations. Thus \(D\) is meagre and \(E\) is a dense Gδ set. Countable stability of Hausdorff dimension and \(\dim_HK_q>2\) imply \(\dim_HE=\dim_HK_q\). Finite square-only renders omit the residual points literally, while still converging in Hausdorff distance to the whole attractor. Moreover, if \(d=\dim_HK_q\), then \(\mathcal H^d(K_q)=0\): positive critical measure would force Ahlfors regularity and contradict \(\dim_AK_q=3>d\).

### 5.2 Explicit finite bounds at the origin

An independent finite certificate gives numerical instances of the full-ball convergence for the **original eight-map denominator-125 membrane at \(q=1/4\)**. At the origin, the following bounds hold at every positive scale below the threshold:

| Maximum central-word depth n | Scale threshold | Strict upper bound on \(d_H((K_{1/4}/t)\cap B,B)\) |
|---|---|---|
| 5 | t ≤ 1/1024 | 0.092423119034 |
| 6 | t ≤ 1/4096 | 0.021264176895 |
| 7 | t ≤ 1/16384 | 0.009278720270 |

Each central word of length at most n retains a centred disk with radius at least \(4^{-n}\). The certificate checks exact plane-distance witnesses at 120,000 antipodally paired cube-face directions and adds a rigorous rational mesh-radius enclosure to cover the intervening directions. Integer arithmetic verifies the selected normals, squared distances, and upper enclosures. The [finite-bound proof and checker instructions](../constructive/tangent_bounds/README.md) and [complete certificate](../constructive/tangent_bounds/certificate.json) give the details.

These inequalities concern the infinite reference attractor and every stated scale; they are not sampled-image errors or estimates for the anchored visual variant. At a cylinder centre with contraction \(r_w\), the same error bound holds below scale \(r_w4^{-n}\). The finite certificate does not determine the asymptotic exponent in Section 2.1 or the actual Assouad-spectrum transition.

## 6. Separation, presentation, and intrinsic properties

The graph system visibly fails the weak separation property (WSP): relative word maps \(h_0^{-n}h_x^n=R_x^n\) have nonidentity subsequences converging to the identity. The membrane's presented IFS fails the open set condition (OSC) directly. If a feasible open set contained a ball of radius \(r\), its \(4^n\) central-word images would be disjoint balls of radius \(q^nr\), all contained in a ball whose radius is a fixed multiple of \(q^n\). Volume comparison is impossible as \(n\) grows. Coincident word maps would already violate the required disjointness.

More strongly, neither attractor admits any alternative finite similarity presentation satisfying WSP, and hence none satisfying OSC. The precise applicable result is Fraser–Henderson–Olson–Robinson Theorem 1.4: a self-similar set not contained in a codimension-one affine hyperplane has \(\dim_A=\dim_H\) whenever its defining IFS satisfies WSP. Both sets have full affine span and a strict intrinsic dimension gap. This implication does not require that the alternative presentation use the displayed rotations. [FHOR, primary paper](https://arxiv.org/pdf/1404.1016).

This distinction matters throughout. The number of maps, individual roll angles, exact word coincidences, and a first-level intersection graph describe a presentation. Hausdorff, Assouad, and topological dimensions, the existence of a contained embedded graph, and equation (1) describe the set. Different presentations can define the same set. A map-level change or a different rendered silhouette alone does not establish a new intrinsic family.

## 7. Relation to earlier work and remaining questions

Retaining a segment or square with its own subsystem is a homogeneous way to implement a persistent seed. It is closely related in spirit to condensation-set constructions; it is not a new framework for self-similarity. Recursive knots and Borromean arrangements also have direct predecessors, including [Fathauer's iterative fractal knots](https://archive.bridgesmathart.org/2007/bridges2007-335.pdf) and [Burkholder's Brunnian weavings](https://archive.bridgesmathart.org/2010/bridges2010-263.pdf). Even arbitrary knot containment is not a new discriminator by itself: [Broden and collaborators](https://arxiv.org/abs/2409.03639) establish it for the Menger sponge.

The full-ball phenomenon should likewise be placed within tangent theory. Guido–Isola's fixed-point result, Theorem 2.6 in the linked preprint, describes metric tangents through the completion of the union of inverse similarity iterates. With the graph system's central homothety and dense retained directions, that completion is \(\mathbb R^3\). The elementary proof here establishes the precise embedded, closed-window, every-scale statement used in the construction. [Guido–Isola](https://arxiv.org/pdf/math/0305091).

Käenmäki–Rutar prove abundant points with tangents attaining Assouad dimension for broad invariant-set classes. Their general result concerns existence of large tangents, rather than the unique full-ball convergence asserted here. [*Tangents of invariant sets*, Theorem C](https://arxiv.org/pdf/2309.11971).

The contribution currently proposed is therefore an explicit, reproducible combination: chosen retained spatial geometry, symmetry when desired, controllably small excess Hausdorff dimension, and a dense set of unique full-ball tangent points. An exact earlier statement combining these features was not located in the present search. That does not establish priority or publishable novelty.

Further investigation should address the actual Hausdorff dimensions, parameter-dependent exact overlaps and equivalent presentations, the geometry of the residual set beyond the retained seeds, and complement invariants that survive all descendants. Section 2.1 supplies a positive-power rate for (1), but an effective numerical exponent and the actual transition in the Assouad spectrum remain open. Rendering should document which geometry is shown, at what depth, and with what line or surface thickness.

## 8. Reproducibility and current artifacts

The implementation and evidence are recorded in the following repository files.

| Artifact | Purpose |
|---|---|
| [Survey definition and report](../survey/REPORT.md) | Threefold Borromean recipes, bounds, and scope |
| [Survey model](../survey/model.py) | Recipe construction, decimal matrix exports, and point sampling |
| [Rendered 127-map exact recipe](../survey/Borromean-C3-m3-axis6-q1_8-Exact.aifs) and [variant definitions](../survey/VARIANTS.md) | Exact hero geometry and axial subdivision parameters |
| [Exact scalar verifier](../survey/verify_exact.py) | Rational enclosure and dimension inequalities |
| [Link certificate explanation](../research/LINK_CHECK.md) and [verifier](../research/verify_link.py) | Exact projected crossings and Fox-colouring system |
| [Membrane definition](../constructive/MEMBRANE.md) and [implementation](../constructive/membrane.py) | Rational matrices, proofs, and finite genuine sheet subsets |
| [Exact overlaps and residual-set report](../constructive/overlaps/OVERLAPS.md) | Word equalities, sharper bounds, free rotations, and limits of sheet renders |
| [Spectral-gap corollary](../research/SPECTRAL_TANGENTS.md) and [internal review](../research/SPECTRAL_TANGENTS_REVIEW.md) | Existential power-law tangent rate, final Assouad-spectrum plateau, and quasi-Assouad dimension |
| [Explicit tangent bounds](../constructive/tangent_bounds/README.md) and [certificate](../constructive/tangent_bounds/certificate.json) | Exact finite numerical bounds for the original eight-map q=1/4 membrane |
| [Prior-art audit](../research/PRIOR_ART.md) | Broader precedents and unresolved novelty comparison |
| [Independent internal review](../research/INDEPENDENT_REVIEW.md) and [publication audit](../research/PUBLICATION_AUDIT.md) | Checked hypotheses, limitations, and independent finite computations |

Floating-point matrix tests establish implementation consistency, not symbolic topology. The scalar and link certificates use exact arithmetic for their stated finite questions. Rendered tubes or finite point clouds are visualizations of the construction; membrane square panels are genuine retained subsets computed to finite depth. None of these artifacts alone is a proof-assistant formalization, an external review, or evidence of historical originality.
