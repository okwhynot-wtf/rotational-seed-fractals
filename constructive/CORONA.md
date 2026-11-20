# Anchored-wing extension

This is a separate extension of the basic membrane continuum in MEMBRANE.md.
Retain its four half-scale square maps and four common-centre maps h_k with
q=1/10. Add four maps

    g_k(x)=p_k+r A_k(x−p_k),
    p_k=Z^k p_0,     A_k=Z^k A_0 Z^(−k).

The corner recipes use p_0=(1,1,0); the edge recipe uses p_0=(1,0,0).
The slant rotation A_0 is Q from MEMBRANE.md. Radial uses the 90° rotation
about (1,1,0)/√2; tangent the 90° rotation about (−1,1,0)/√2; sweep uses
cos θ=−3/5, sin θ=4/5 about (3/5,4/5,0). These formulas, not rounded
matrices, are the exact definitions. The selected r values are 7/20,9/20,49/100.

Every added map fixes a point p_k of the retained square S. Its image of S
therefore meets S. The same connectedness argument as for the basic model
works. A sufficiently large invariant ball exists by contraction and can
be chosen to contain S, so nested connected iterates establish connectedness.
Conjugation by Z permutes all twelve maps, proving C4 symmetry.

The original square and common-centre rotation subsystem remain present.
Thus all dense-sheet and full-ball-tangent arguments from MEMBRANE.md apply
unchanged. Hausdorff dimension is at least 2 and at most the root s of

    4·2^(−s)+4·q^s+4·r^s=1.

All surveyed members satisfy 1/2+4q³+4r³<1, so s<3, zero volume and
topological dimension exactly 2 follow. Assouad dimension is 3.
No claim of exact Hausdorff dimension or historical originality is made.

corona.py renders finite collections of the exact squares f_w(S), suppressing
words ending in a base square-tiling map since those create only subsets of
already present squares. Its depth-limited rendering uses no added thickness.
The individual maps are exact smaller copies of the full set, even though
the finite pictures only display known sheet subsets and omit the residual set.
