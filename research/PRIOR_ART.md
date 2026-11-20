# Prior-art map and research targets

Search date: 20 November 2026 (Australia/Sydney). This is a working research record, not a priority certificate. No absence from the searches below establishes historical novelty.

## Finding that should govern the project

The strongest opportunity is a precisely defined new construction with a verifiable combination of properties, rather than a claim to have invented 3D self-similarity, recursive knotting, rotated sponges, or fractal solids. All of those broad ideas have substantial precedents. The user's clarification permits connected, zero-volume spatial attractors, so nonempty interior need not constrain the search.

There is nevertheless a timely published invitation to investigate this territory. Bandt's 2025 *Elementary Fractal Geometry 7* explicitly proposes three-dimensional constructions using an integer dilation and the cube symmetry group, as well as graph-directed 3D constructions. Its Section 7 describes the scarcity of worked spatial examples and emphasizes that rendering and classification are the difficulty. This supports the value of a careful experimental atlas; it does not confer novelty on any particular member. The paper also gives an unlimited magnification method using control points and neighboring copies. [Primary paper](https://www.mdpi.com/2504-3110/9/12/762).

## IFStile, not “IFStyle”

The intended program appears to be **IFStile** by Dmitry Mekhontsev. Its current official site advertises arbitrary-dimensional affine graph IFSs, 2D/3D cross-sections, automated search, dimension calculations, mesh export, and batch animation. The current repository is GPL and includes the declarative AIFS language, with JavaScript extension support. The source distribution itself is a useful prior-art corpus: compare proposed maps against its examples, not only against named textbook fractals. [Official site](https://ifstile.com/) · [development repository](https://github.com/mekhontsev/ifstile) · [AIFS manual](https://github.com/mekhontsev/ifstile/blob/master/manual.md).

Caution: the 2025 Bandt paper describes an older, then non-open-source IFStile release. That statement should not be copied into a current software description.

## Close precedents and what they rule out

### Rotated cubical sponges and contact spectra

Ruan and Xiao study exactly the class

\[
f_i(x)=\frac{O_i(x)+i}{N},\qquad i\in I\subset\{0,\ldots,N-1\}^d,
\]

where every \(O_i\) is a symmetry of the unit cube. They give effective finite methods for piece-intersection emptiness and connectedness in every dimension, including branch-dependent rotations and reflections. Thus a search over those orientations is a search *within an established class*. Their paper notes that equality of attractors from different IFS recipes already has a group-theoretic treatment by Falconer and O'Connor. [Ruan–Xiao preprint, 2022, revised 2025](https://arxiv.org/abs/2204.09219) · [published paper, 2025](https://doi.org/10.1017/S0305004125000015).

Bandt and Mekhontsev's 2018 search already uses boundary/intersection dimensions to distinguish examples with the same overall Hausdorff dimension. Its examples show that similar first impressions can hide very different contact structures under magnification. Therefore “constant dimension, variable contacts” is not itself a new mechanism. A rigorously classified spatial family could still be new. [Primary preprint](https://arxiv.org/abs/1801.08325) · [journal version](https://doi.org/10.1063/1.5023890).

Tetenov and Drozdov give graph-directed descriptions of intersections of fractal cubes and opposite faces, with dimension, cardinality, and measure consequences. This is directly relevant to claims about an exact contact spectrum, even where its unrotated hypotheses differ from a new construction. [Primary preprint, 2024](https://arxiv.org/abs/2410.03388).

**Important invariant warning:** dimensions of first-level piece intersections describe a chosen IFS presentation. Without an intrinsic characterization of those pieces, different spectra do not alone prove that the limit sets are noncongruent, nonhomeomorphic, or not bi-Lipschitz equivalent.

### Symmetry and distinctness

Falconer and O'Connor give a group-theoretic method to enumerate distinct attractors arising from families of similarity systems. This is an appropriate reference before treating the number of recipes as the number of different fractals. [*Symmetry and enumeration of self-similar fractals*, 2007](https://doi.org/10.1112/blms/bdl031).

A failure of literal map conjugacy is useful but limited: two different IFSs can have the same attractor. Conversely, global rotational symmetry of the set is not the same as density of the rotations occurring in its small copies. A bounded set cannot generally have all of SO(3) as its global symmetry while retaining an asymmetric sculpture-like shape; the dense-rotation property concerns the IFS orientation group.

### Knots, links, and repeated knotting

Fathauer described iterative fractal knot substitution in 2007, including symmetric arrangements, and a 2010 paper treats genuinely spatial self-similar knots using nested surfaces and connecting strands. These constructions should be compared at the level of exact rules: an iterative substitution with persistent connector strands is not automatically a finite homogeneous similarity IFS. They nonetheless preclude a broad novelty claim for knots containing smaller copies of themselves. [2007 paper](https://archive.bridgesmathart.org/2007/bridges2007-335.pdf) · [2010 paper](https://archive.bridgesmathart.org/2010/bridges2010-103.pdf).

Burkholder's 2010 *Brunnian Weavings* explicitly uses iterative self-similar patterns of three linked rings, alongside other weaving procedures. A Borromean-looking recursive rendering is therefore insufficient evidence for a new family. The useful comparison is whether the new object has exact Euclidean similarity maps, connectedness of the whole limit, and a proved invariant of the embedding that the older construction lacks. [Primary paper](https://archive.bridgesmathart.org/2010/bridges2010-263.pdf).

Antoine's necklace is an old geometric counterexample with exact self-similar realizations. Schwartz's 2022 notes give one explicit construction and explain why its limit is a Cantor set despite the linked torus approximations. It is a warning against inferring connectedness or persistent loops from finite thickened pictures. [Author's notes](https://www.math.brown.edu/reschwar/MathNotes/antoine.pdf).

Broden, Espinosa, Nazareth and Voth prove that every knot embeds in the Menger sponge, and that all pretzel knots embed in the Sierpinski tetrahedron. Consequently, merely finding a knot inside a spatial fractal is not a new category. An invariant of the full complement, or a metric constraint absent from those constructions, would be more informative. [2024 preprint](https://arxiv.org/abs/2409.03639) · [2026 published paper](https://doi.org/10.1080/10586458.2026.2615948).

### Genuine solid interiors

Blair, Marley and Richards classify the homeomorphism types of 3D rep-tile manifolds as exteriors of finite connected graphs in \(S^3\). Handles, knot exteriors, and related topology are thus already present in the solid self-similar world. This theorem does not classify exact geometric similarity types or every fractal boundary. [*Three-dimensional Rep-tiles*, 2021](https://arxiv.org/abs/2107.10216).

Conner and Thuswaldner construct self-affine tile manifolds of arbitrary handlebody genus and an example with a wild sphere boundary. The distinction between self-affine and Euclidean self-similar is essential when comparing these examples. [*Self-affine Manifolds*, 2015](https://arxiv.org/abs/1402.3000).

### Necklaces and cut points

Wen defines connected necklaces by a cycle of first-level pieces, with singleton adjacent intersections and no nonadjacent intersections. The paper proves several no-cut-point criteria; stable self-similar necklaces satisfying OSC have no cut points. Porous Lantern's existing proof of additional non-singleton adjacent contacts means it is not automatically in this exact class. [*Fractal necklaces with no cut points*, 2021](https://arxiv.org/abs/2105.00407).

### Dense rotations and dimension gaps

Bandt and Mekhontsev already construct planar connected examples with irrational rotations under OSC. Transferring a related mechanism into three dimensions with genuinely noncommuting rotations is a possible research direction, not an established novelty result. [*Carpets Involving Irrational Rotations*, 2022](https://doi.org/10.3390/fractalfract6010039).

García's Corollary 1.6(1) applies to a self-similar set not contained in any hyperplane: if a generating IFS fails WSP and its word rotations are dense in O(d) or SO(d), the Assouad dimension is d. The same corollary makes every k-dimensional orthogonal projection have Assouad dimension k. Corollary 1.7 excludes the combination of Hausdorff dimension one, positive one-dimensional Hausdorff measure, and WSP failure. These are theorems to apply with explicit hypotheses, not new results of this project. [Primary paper](https://arxiv.org/pdf/1909.03148).

The underlying distinction between Hausdorff and Assouad dimension for overlapping similarities is already central to Fraser, Henderson, Olson and Robinson. WSP gives equality; its failure can increase local covering complexity. [Primary paper](https://doi.org/10.1016/j.aim.2014.12.026).

## Four concrete research directions

These are proposed targets, not established results.

### 1. A graph-to-attractor construction with nearly one-dimensional Hausdorff size

The team is investigating a constructive statement: for any finite connected polygonal spatial graph G and any epsilon > 0, construct a connected finite similarity attractor K containing an embedded copy of G, with

\[
1<\dim_H K<1+\varepsilon,\qquad \dim_A K=3.
\]

A prototype uses two axial half-scale maps to retain an interval S, many sufficiently small maps taking S onto subdivided edges of G, and a common-fixed-point block qI, qR_x, qR_y. Rotations about perpendicular axes with cosine 3/5 and sine 4/5 are an exact rational choice. Their angles are irrational multiples of pi, and their closed rotation group is SO(3). Comparing equal-length words from qI and qR_x produces nonidentity relative rotations converging to the identity, which is the intended WSP obstruction. Subdividing edges and reducing q make the similarity-dimension upper bound approach one.

**What could make this useful:** a reproducible compiler from a graph to a finite IFS, an elementary connectivity proof, exact source maps, and a sharp qualitative dimension gap. Knots/links then become chosen test inputs rather than guessed structures in a render.

**What remains to prove:** the seed and all attachment conditions, an explicit contraction/weight bound, the rotation-group argument, and every hypothesis of the dimension theorem. The strict lower bound above is intended to follow from a contained interval and the cited dimension-one rigidity result; it must be integrated into a complete proof.

**Novelty status:** no exact version of this combined graph-containing statement was located in the searches performed. It resembles a concise constructive application of established IFS and Assouad theory. It must not be called a new category on that basis. “Contains G” does not prescribe K's topology or the topology of its complement; extra descendants can change both.

### 2. A membrane attractor with actual planar patches in dense orientations

Use a square-tiling subsystem to retain a literal 2D square, then attach small rotated copies with a common fixed point. A cyclic orbit of tilted axes can impose fourfold symmetry. This gives a practical route to connected sheet-like geometry, with zero volume controlled by the sum of cubes of contraction ratios, and a potential dense set of plane orientations among exact subsets.

**Concrete target:** certify a topologically two-dimensional connected attractor with dense orientations of flat patches and a Hausdorff/Assouad gap, and investigate whether the patches have an intrinsic characterization.

**Precedent obstacle:** a persistent seed set plus copies is the standard idea of an inhomogeneous IFS with a condensation set. Encoding the seed by its own tiling maps can make the final definition homogeneous, but this alone is not a new paradigm. [Fraser's notes, Section 3.4](https://personal.maths.manchester.ac.uk/jm/wiki/uploads/LMS/Fraser-notes.pdf) · [Burrell–Fraser, 2020](https://doi.org/10.5186/aasfm.2020.4516).

### 3. Same-dimension spatial relatives with a new intrinsic distinction

Keep a fixed cube-pattern size and number of maps. Search orientations, compute an exact neighbor automaton, and retain pairs with equal Hausdorff dimension and the same first-level Hata graph but different deeper structures.

**Concrete target:** prove a difference in local cut-point valences, an intrinsic separating-set dimension, or complement topology. An exact rational neighbor certificate is a useful intermediate result. Contact spectra alone should be presented as presentation data.

**Precedent obstacle:** the rotated-sponge class and its connectivity algorithm are known, as are planar same-dimension examples with different interface dimensions. This direction needs a genuinely new specimen, complete spatial classification, or additional invariant, not renamed familiar machinery.

### 4. Prescribed linking that survives every descendant

Use a connected cyclic or graph-directed construction whose first-level arrangement has selected linked channels. Test the whole infinite attractor, not only finitely many rendered tubes. A proof could use complete prefix covers to keep a witness curve clear of K, then compute its linking with an explicitly retained loop in K.

**Concrete target:** a stable parameter family with a certified link or complement invariant, preferably with n-fold symmetry and a controlled infinite zoom. This is more discriminating than arbitrary knot containment.

**Precedent obstacle:** Antoine necklaces, Fathauer's knots, and Burkholder's Brunnian weavings all anticipate recursive linking. A claim should identify the exact extra property and compare exact maps or intrinsically defined topology.

## Follow-up: unique full-ball blowups at dense points

The team's revised construction suggests a stronger directly provable local statement than the Assouad conclusion. Suppose K contains a nondegenerate centered segment through 0, and a subsystem of similarities fixing 0 has word rotations whose action on that segment's directions is dense on the sphere. Then

\[
\lim_{t\downarrow0}d_H\bigl(t^{-1}K\cap\overline B(0,1),\overline B(0,1)\bigr)=0.
\]

Here d_H is Hausdorff distance between compact sets, not Hausdorff dimension. This asserts convergence at **all sufficiently small scales at one fixed center**. It is stronger than a full contingent cone, which only records attainable limiting directions, and stronger than the existence of a full-ball weak tangent along selected scales and moving centers.

An elementary proof is available. For any positive angular tolerance, choose finitely many retained segment copies whose directions form a corresponding net of the sphere. Each copy has positive radius about 0; take the minimum of these finitely many radii. Every smaller centered ball contains radial segments in the entire chosen directional net. After normalization their union approximates the closed unit ball with the prescribed tolerance. A square seed works too because it contains a centered segment. Applying any defining word transfers the property to its image of 0. These word images are dense in K, since cylinder diameters tend to zero.

### Direct mathematical precedent

Guido and Isola compute the metric tangent family at a generating similarity's fixed point: it is the dilation family of the completion of the increasing union of inverse iterates of the attractor. This is Theorem 2.6 in the arXiv version of *Tangential dimensions I. Metric spaces* (published 2005). No separation condition appears in this theorem. With a generating map qI and the retained dense directions above, the completion is Euclidean three-space, so the unique Euclidean tangent follows as a specialization. Their metric topology differs in presentation from the closed-window formula above; the elementary segment proof verifies exactly the desired embedded Hausdorff statement. [Primary preprint](https://arxiv.org/pdf/math/0305091).

Käenmäki and Rutar's *Tangents of invariant sets* establishes that finite bi-Lipschitz IFS attractors have a dense set of points possessing a tangent attaining the global Assouad dimension. For finite self-conformal systems, the set of such points has full Hausdorff dimension. Their Theorem C asserts existence of large tangents; it does not assert a unique full-ball tangent or convergence at every scale. [Primary preprint, Theorem C](https://arxiv.org/pdf/2309.11971).

**Assessment:** the all-scale assertion is mathematically meaningful and visually counterintuitive for a zero-volume attractor whose Hausdorff dimension approaches one. It is not a new tangent phenomenon established by this search: it is an elementary consequence of a retained radial seed and standard fixed-point tangent theory. The potentially distinctive contribution is a fully explicit, reproducible family combining it with arbitrary polygonal graph containment, exact cyclic symmetry, and a tunable Hausdorff-dimension upper bound. An exact prior theorem combining all these features was not located. This absence is not evidence of priority, and the combination may be a short corollary rather than a publishable new category.

A meaningful next investigation would be a quantitative result: how fast the normalized largest holes shrink, how this rate depends on q and the rotation word length, and whether it yields a sharp pointwise dimension spectrum. This is a proposed question, not an established invariant or novelty claim.

## Suggested evidential standard for publication

1. Record exact maps, parameter domains, word conventions, and a machine-readable recipe.
2. Prove connectedness of the infinite attractor, not just connectedness of a voxel model.
3. Separate symmetry of K, symmetry of a defining IFS, and the group of orientations of small copies.
4. Label similarity dimension as an upper bound until a separation theorem or another exact-dimension argument applies.
5. Distinguish literal map inequivalence from inequivalence of limit sets.
6. Give rendering thickness and geometric truncation explicitly. Tube or sheet rendering can be beautiful without being the mathematical object itself.
7. State originality as unresolved until comparisons cover the exact proposed claim. The honest initial label is an investigated construction or candidate family.

## Search scope

Primary-source searches covered self-similar and self-affine 3D tiles, handlebodies, graph exteriors, wild boundaries, Antoine necklaces, fractal knots and Brunnian links, rotated/reflected Sierpinski sponges, intersection spectra, symmetry enumeration, dense rotations, Assouad dimension gaps, condensation IFSs, and graph-directed constructions. Publication and preprint dates were checked where material to the comparison. Informal artworks with unavailable exact recipes, non-English literature, unpublished IFStile examples, and equivalent attractors with unrelated IFS presentations remain substantial gaps.

No message was sent to any author, and no repository or site was published during this literature subtask.
