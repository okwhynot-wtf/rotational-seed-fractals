# Independent mathematical and implementation review

20 November 2026. Internal review by a separate research agent; not external peer review or a proof-assistant verification. Files were changing during the review. Only this review file was edited.

## Result

No fatal gap was found in the connectedness, literal graph containment, membrane construction, full-ball tangent argument, dimension upper bounds, or polygonal link certificate. The strongest conclusions concern the exact infinite attractors; the scripts provide finite arithmetic checks and numerical implementations, with appropriately limited scope.

Reviewed: `survey/REPORT.md`, `survey/model.py`, `survey/verify_exact.py`, `constructive/MEMBRANE.md`, `constructive/membrane.py`, `research/verify_link.py`, and `research/LINK_CHECK.md`.

## Issues and recommendations

1. **Symmetry wording needs a small correction.** The survey's opening “pure threefold rotation symmetry” can imply that the full symmetry group is exactly C3, or that reflections have been excluded. The proof only establishes that C3 acts on K. Say “threefold rotational symmetry.” The membrane report already distinguishes proven symmetry from possible additional symmetries.

2. **The survey's every-scale proof was corrected during review.** Its initial version established the q-adic subsequence and explicitly declined an every-scale claim. The revised finite directional-net argument now proves
   `d_H(((K-p)/t) ∩ closed_unit_ball, closed_unit_ball) → 0`
   for every cylinder centre p as t tends to zero through all positive scales. This proof is valid. The membrane's finite disk-net/minimum-radius proof is also valid. Neither proof needs an identity central map; that map is useful for the separate WSP obstruction.

3. **Keep numerical recipes distinct from exact certificates.** `model.py` uses floating-point norms and matrices. Its endpoint, orthogonality, symmetry, and enclosure tests are implementation checks. The exact construction is determined by rational vertices, rational half-angle parameters, and prescribed positive square roots. The report makes this distinction. The scalar certificate does not independently verify rotation matrices or topological assertions.

4. **The link verifier's parallel-edge branch is safe for these coordinates, but not a general-purpose degeneracy test.** It skips projected parallel pairs without checking collinearity. I independently checked every such cross-component pair in the chosen projection: all supporting lines are distinct. The individual projected rectangles are nondegenerate parallelograms, so omitting within-component crossing tests is also justified here. If the routine is generalized, add explicit rejection of collinear overlap, collapsed projected edges, and self-crossings. The current special-case certificate is unaffected.

5. **The all-m enclosure is true but the executable certificate covers the tabulated m values.** For x=1/m in (0,1/2], the rational bound used in the report reduces to positivity of
   `(5/2 - (289/400)x)^2 - (5 - x + x^2/4)`.
   It is decreasing on this interval and positive at x=1/2. This supplies a short uniform proof for every m≥2, supplementing the four executed certificates.

6. **Graph containment is not a topology classification of K.** The files correctly avoid equating the embedded polygonal link with the topology or complement of the entire attractor. Extra points cannot change the ambient link type of the selected three curves as a subset, but may fill disks, add paths, or otherwise change which features are essential in K. Keep this qualification in the public presentation.

## Lower bounds: what can safely be stated

Without an additional measure or regularity theorem, the supplied elementary arguments establish

    1 ≤ dim_H K < 1+epsilon,    dim_A K=3

for the graph construction, and `2 ≤ dim_H K_q < 2+epsilon` for suitably small membrane q. A contained interval or square proves the respective non-strict lower bound. A full-ball tangent by itself is an Assouad lower bound; it is not an elementary Hausdorff-dimension lower bound of three or a proof of strictness above one/two.

There is, however, a verified clean route to strictness that does **not** use an alleged equivalence between positive critical measure and OSC. Farkas–Fraser, *On the equality of Hausdorff measure and Hausdorff content*, Corollary 3.1, proves that a finite self-similar set with positive Hausdorff measure in its Hausdorff dimension is Ahlfors regular. No separation condition is assumed; ordinary IFS attractors are the full-shift special case. [Primary paper](https://arxiv.org/pdf/1411.0867).

Consequently, if the graph attractor had Hausdorff dimension one, its contained interval would give positive critical measure, hence Ahlfors 1 regularity and Assouad dimension one, contradicting the full-ball tangent. Thus **1 < dim_H K**. The identical reasoning with the retained square gives **2 < dim_H K_q**. This is a valid cited measure-theoretic strengthening, not an elementary consequence of the constructions alone. If avoiding all such theorems is a publication requirement, retain the non-strict lower bounds. No independent elementary strictness proof was established in this review.

In particular, do not substitute “positive critical Hausdorff measure implies OSC”: that statement is false. The actual similarity dimension of a given presentation and the Hausdorff dimension of its attractor must remain distinct.

## Alternative presentations

The exclusion of **every** alternative OSC presentation is justified by the intrinsic gap `dim_H K < dim_A K=3`: a finite similarity IFS satisfying OSC produces equality of these dimensions. The stronger survey claim excluding every alternative WSP presentation is also justified. Fraser–Henderson–Olson–Robinson Theorem 1.4 states WSP implies equality for a self-similar set of full affine span; the retained spatial skeleton establishes that hypothesis. [Primary paper](https://arxiv.org/pdf/1404.1016).

The elementary common-fixed-point packing argument proves OSC failure for the presented map list even if finite words coincide. Its stronger conclusion about alternative presentations requires the intrinsic dimension gap, as the reports correctly indicate.

## Checks independently executed

- Imported all six survey recipes and ran endpoint, axis-interval, orthogonality, C3-conjugacy, and enclosure checks. All passed. Maximum reported numerical endpoint error was approximately 2.3×10^-16.
- Re-ran the four rational scalar certificates by calling `certify`, without writing their output files. All passed.
- Independently exhaustively enumerated all assignments over F3 for each Fox-colouring matrix, rather than relying on the script's modular row reduction. The full 12-crossing diagram has 3 colourings; each 4-crossing pair has 9. These agree with the certificate.
- Checked every skipped parallel projected edge pair with exact fractions; no collinear pair occurs.
- Checked the membrane rotation's integer orthogonality and its determinant with an independent integer determinant formula: `N^T N=125^2 I`, `det N=125^3`.

The pairwise unlink argument is sound: a thin regular neighbourhood of the stated spanning rectangle is a separating ball disjoint from the other loop. The Fox count distinguishes the triple from the three-component unlink. Together with the planar unknotted components and pairwise unlinking, this proves the stated nonsplittable Brunnian property. It does not by itself classify all possible Brunnian link types; the explicit coordinates identify the particular rectangular arrangement.

## Historical framing

The every-scale full-ball result is stronger than an unspecified weak tangent, but is still an elementary fixed-point specialization of established tangent theory; see the prior-art report and [Guido–Isola, Theorem 2.6](https://arxiv.org/pdf/math/0305091). The combined explicit construction may be worth documenting and exploring. Neither these checks nor the literature search establishes a new historical family or category.
