# Independent check of the polygonal link

The three rectangle boundaries are

    L0 = boundary([-2,2] × [-1,1] × {0}),
    L1 = G L0, L2 = G² L0, G(x,y,z)=(z,x,y).

They are disjoint. The disk D0=[-2,2]×[-1,1]×{0} is disjoint from L1: the points of L1 with z=0 have y=±2. A sufficiently small closed regular neighborhood of D0 is a ball containing L0 and disjoint from L1. Both loops are planar unknots, so this pair is the two-component unlink. Cyclic symmetry proves the same for the other two pairs.

The script `verify_link.py` constructs their projected diagram using rational arithmetic. Projection is (17x-7z,17y-11z), with depth 7x+11y+17z. It rejects projected vertex crossings and multiple crossings. There are twelve regular crossings, with nonzero exact depth separation. The resulting Fox 3-colouring system has three solutions, whereas the three-component unlink has 27. The colouring count is preserved by Reidemeister moves, so the triple is not the unlink. Each two-component subdiagram gives nine colourings, providing an independent check consistent with the disk separation argument. All three pairwise linking numbers are zero.

Because every pair is an unlink, a splitting sphere separating one component from the other two would make the entire triple an unlink. The triple is therefore nonsplittable despite every pair being unlinked: the Borromean property.

The certificate concerns the three polygonal loops. The interval-backed construction contains these loops literally, and hence contains their images under every word map. Extra points of the full attractor do not alter the embedding type of this selected subset. This does **not** classify the topology or complement of the full attractor, imply the selected loops are essential in that full set, or establish a previously unknown fractal family.

Reproduce with `python research/verify_link.py` from the expedition directory. The JSON receipt preserves exact crossing fractions and the modular linear system. The result is an independently implemented finite computation plus the stated geometric argument, not external mathematical review.

An early diagnostic projection along (1,1,1) was degenerate: it placed vertices on other projected edges. Pairwise colouring checks detected the missing crossings. The final verifier explicitly rejects that degeneracy and uses the regular direction above.
