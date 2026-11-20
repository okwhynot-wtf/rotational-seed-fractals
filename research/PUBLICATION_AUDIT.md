# Publication mathematical audit

20 November 2026. A further internal agent review of the manuscript, public documentation, and overlap report. This is not external peer review or a proof-assistant verification.

## Outcome

No fatal mathematical gap was found in the stated construction theorems or the new overlap bounds. The supported result is a collection of explicit candidate constructions and proofs within established self-similar-set theory. Historical originality and a new category of fractal are not established.

## Analytic checks

- **Every-scale ball limit.** The finite-direction-net argument is valid. Choosing finitely many retained centred segments and then the minimum of their positive radii works simultaneously for every smaller scale. Clipping to the closed unit ball does not remove those normalized unit segments. The inclusion transfers the conclusion to every cylinder centre. These centres are dense because zero belongs to the attractor and cylinder diameters tend to zero. This is stronger than a statement about limiting directions alone.
- **Connectivity and paths.** The graph seed lies in the attractor. Every map image of the graph meets that retained connected graph, so compact-set iteration stays connected. Paths between successive cylinder centres have summable lengths, bounded by a geometric series with the maximum contraction ratio. The manuscript therefore establishes path connectedness, not merely connectedness. The square construction has the same attachment property.
- **Strict lower bounds.** I directly read [Farkas–Fraser, Corollary 3.1](https://arxiv.org/pdf/1411.0867), including its explicit statement that no separation condition is assumed. An ordinary finite IFS is its irreducible full-shift case. A retained interval or square gives positive critical measure if the dimension equals one or two; the resulting Ahlfors regularity contradicts Assouad dimension three. The strict lower bounds and the deduction of zero critical Hausdorff measure are justified. No implication from positive critical measure to OSC is used.
- **Alternative presentations.** I directly read [Fraser–Henderson–Olson–Robinson, Theorem 1.4](https://arxiv.org/pdf/1404.1016). Full affine span and the intrinsic Hausdorff–Assouad gap exclude every finite similarity presentation with WSP. The full-ball result supplies full affine span. The claim is not restricted to the displayed map lists.
- **Dimension and symmetry scope.** The covering sums are upper bounds, not dimension equalities. The presence of C3 or C4 symmetry does not prove that these are the full symmetry groups. Topological dimension one follows for the sufficiently thin graph members, and topological dimension two for the membrane; it is not established for the rendered 127-map graph member.
- **Residual membrane set.** Each retained square is closed with empty relative interior because every relative neighbourhood contains patches with dense orientations. The union of the squares is dense, meagre, and has Hausdorff dimension two. Countable stability and strict dimension greater than two give the residual complement the full Hausdorff dimension. Its topology is not classified.

## Exact-overlap and free-rotation checks

The forbidden-pattern proof is sound. Lexicographic replacement terminates at a fixed word length while preserving the complete affine map. The core–core–base pattern for the original model, and core–base pattern for the norm-13 model, prevent proper prefix–suffix overlaps. The weighted recurrence counts a genuine covering family. At its stated root, the first-difference recurrence has a block contraction factor below one, giving bounded covering weight and the claimed upper bound.

The modular rank-one quaternion argument also proves freeness: an adjacent noninverse pair has nonzero matrix product, so any reduced word has nonzero reduction. A real scalar quaternion of norm p to an even positive power would reduce to zero; an odd power cannot be an integer square. The original four conjugates form a free subgroup because distinct conjugators leave nonempty words in X and Y between T powers. Thus equality of full affine words forces the same ordered core-letter subsequence and the same number of base letters. The shortest-word claim for the norm-13 model follows when combined with the finite noncollision screen; it is not a claim that all overlaps have been classified.

I independently composed both displayed affine equalities using 4×4 homogeneous matrices and `fractions.Fraction`, without calling the construction's composition routine. Both passed. I independently multiplied the quaternions for all four original C4 generator words, checked both reference rotation matrices for exact orthogonality, and confirmed that the recorded rational cover sums for the hero and thin member are below one. The separate reproducibility suite reruns the full certificates.

## Link scope

The exact Fox-colouring count distinguishes the three-rectangle subset from the unlink. The stated spanning-disk separation proves every pair is an unlink; pairwise linking numbers or colouring counts alone would not suffice. Together these imply the nonsplittable Brunnian property. They do not determine the full attractor's topology, show that its selected loops are essential in it, or classify its complement. The existing independent review also checked the parallel projected edge cases omitted by the specialized diagram routine.

## Publication corrections made

- Distinguished the older 84-map example from the rendered 127-map member and the 244-map member with proved topological dimension one.
- Removed the stale statement declining all residual-set dimension assertions, and added a concise account of the proved overlap and residual results.
- Made the two nonparallel membrane rotation axes explicit.
- Replaced workstation-specific manuscript links with repository-relative links.
- Identified the exact hero recipe and its own dimension bound on the media and results pages.

No construction, parameter, or rendering definition was changed by this audit. Exact dimensions, a complete overlap classification, complement topology, and historical priority remain open.
