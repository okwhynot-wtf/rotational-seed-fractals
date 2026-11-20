# Prescribed polygon graphs in low-dimensional self-similar continua

The reusable compiler is `graph_compiler.py`. It accepts finite rational
polygonal graphs, retains their complete segments literally, and builds a
connected finite similarity IFS with a requested strict Hausdorff upper bound.
It first proves scalar inequalities and estimates the number of maps; only
then does it allocate a map list. It uses Python's standard library and numpy.
`verify_exact.py` supplies rational upper bounds proved by integer powers.

This is a proposed explicit construction theorem and implementation, not a
claim that the general mechanism or its combination is historically new.

## Theorem

Let Gamma be any finite union of straight segments and isolated points in
R^3. Let B be a nonzero vector, and optionally let G be rotation of finite
order n about the axis R B. Given epsilon>0, there is a compact, path-connected
finite similarity attractor K with these properties:

1. K contains Gamma and its selected finite rotation orbit literally.
2. K contains a smaller exact copy of itself along every finite word; near
   every point of K lie arbitrarily small copies of Gamma.
3. K is invariant under G when the rotation orbit is requested.
4. 1 <= dim_H K < 1+epsilon, and dim_A K=3.
5. At a dense set of cylinder centres p, the sets
   ((K-p)/t) intersect B(0,1) converge in Hausdorff distance to B(0,1) for
   **all** t decreasing to0.
6. If epsilon<=1, then dim_top K=1.

When Gamma, B and the other scalar input data are rational, all defining
coefficients are algebraic. The finite-order rotation has exact angle2*pi/n;
radicals enter through normalization of rational vectors. Numeric JSON
matrices are exports of this exact construction, not its definition.

An input that is described as a knot or link must already be a valid embedded
polygonal knot/link. The compiler guarantees set inclusion; it does not
classify arbitrary input links or prove that a submitted polygon has no
self-intersections. Extra attached edges or rotated copies do not alter the
original link as a subset, but can change the topology of the whole K.

## Canonical graph and attachments

Vertices are exact rational triples. Duplicate vertices, zero-length edges,
reversed edges and repeated edges are normalized. Isolated vertices are
retained. Let S=[-B,B]. For each connected graph component that has no vertex
on S, attach its smallest-norm vertex to0 by a segment, breaking ties
lexicographically. This yields a finite segment network Gamma_star whose union
with S is connected. A component already crossing S through the interior of
an edge may receive a redundant attachment; that is harmless.

If symmetry is requested, take all G^j copies of the graph and attachments.
Because G fixes S pointwise and fixes0, their union with S remains connected.
The compiler intentionally keeps any duplicate orbit maps: this is safe for
the construction and gives a conservative dimension budget.

## Exact map recipe

Choose integer M>=2. The source interval is retained by

    a_j(x) = x/M + ((2j+1-M)/M) B,    j=0,...,M-1.

These M maps tile S. Each augmented graph edge U->V is divided into m equal
pieces, where m=2^k is chosen by the planner. For one piece with endpoints
u,v put

    r=|v-u|/(2|B|),   f(x)=r Q x+(u+v)/2.

The proper orthogonal Q sends B/|B| to (v-u)/|v-u|. A reproducible transverse
frame chooses the coordinate axis least aligned with each direction and
uses a cross product. Between the source and target frames it applies a roll
with cos=3/5, sin=4/5. Hence f(-B)=u and f(B)=v exactly. For symmetry use
G^j f G^-j. Since G fixes B, these maps retain the intended rotated edges.

Finally add a central map h0(x)=q x and central rotations h_i(x)=q Q_i x,
with 0<q<=1/2. Without requested symmetry use rotations about the global x
and y axes; thus there are3 central maps. For n>=2 let

    v=B cross e_j,   a=B+v,

where j minimizes |B_j|; v is nonzero and perpendicular to B. Take the n
rotations about the axes G^j a, together with h0. All central rotations have
cos(theta)=3/5 and sin(theta)=4/5. There are N=n+1 central maps in this case.

All central maps fix0. G permutes their list, and conjugation by G also
permutes the graph maps and fixes the interval maps. Consequently the
attractor has the requested n-fold rotational symmetry.

## Why the prescribed geometry survives

The interval subsystem has attractor S, so S is a subset of K. Every graph
piece is exactly f(S), hence every original segment, attachment and rotated
copy lies in K. The source interval plus this finite graph is connected.

The planner arranges all graph ratios to be at most1/2. Let T be a rational
upper bound on all original vertex norms and |B|. All translation norms are
at most T, and every map ratio is at most1/2, so B(0,2T) is invariant and
contains S. Applying the Hutchinson operator to a connected compact set
containing S and the retained network gives another connected set: interval
images meet along the tiled source interval, graph images meet at their
retained endpoints, and central images meet the interval at0. The nested
compact iterates therefore have connected intersection K.

Every translation f_i(0) lies on the retained network. For an arbitrary
address of x in K, join successive prefix images of0 by prefix images of
paths in that finite network. Their diameters shrink at least geometrically
as(1/2)^k. Concatenation on shrinking time intervals yields a path to x.
Thus K is path connected, not merely connected.

Every word image of the entire network is a subset of K. A sufficiently
deep cylinder containing any chosen x has arbitrarily small diameter, which
proves the all-scale prescribed-graph statement near every point.

## Exact dimension budget and allocation planning

Put D=2|B|, let ell_e be the lengths of augmented seed edges, and let
s=1+epsilon. The similarity covering sum is

    P(s)=M^(1-s)+N q^s+n sum_e (ell_e/D)^s m^(1-s).

Here n=1 if no symmetry is requested. Separation assumptions are unnecessary
for the upper bound: P(s)<1 implies dim_H K<s.

The compiler obtains rational upper bounds a>=M^(-epsilon), b>=Nq^s,
and C>=n sum_e(ell_e/D)^s by integer-root inequalities. For example, to
bound (ell_e/D)^s it uses the rational squared length ratio x and proves
u^(2*s_denominator)>=x^s_numerator. No floating acceptance decision is used.

If q is not supplied, it is successively halved from1/4 until b<(1-a)/4.
Otherwise the compiler requires a+b<1. Set delta=1-a-b>0. If
epsilon=p/r, choosing m=2^k with

    2^(k*p) > (C/delta)^r

proves C*m^(-epsilon)<delta and therefore P(s)<1. This test uses exact
integer arithmetic. A second inequality makes every graph ratio<=1/2.
Increasing k only improves both inequalities. Since C is finite, such k
always exists. The interval gives dim_H K>=1.

For numerical and verification tractability the current implementation accepts
epsilon with denominator at most1000, and caps effective epsilon at3/2 when
a weaker bound is requested. The latter still satisfies the request and
guarantees dimension below3 and zero volume.

The map count is exactly

    M+N+n E 2^k,

where E is the number of augmented seed edges. This is computed before map
generation. If it exceeds `--max-maps`, the compiler writes only a plan and
certificate. Astronomical counts are represented as exact power expressions
and approximate digit counts; no enormous vertex or matrix arrays are built.
The current count limit is an implementation constraint, not a mathematical
obstruction or a failed theorem.

## Why the magnification limit is a solid ball

The central angle is irrational relative to pi. Otherwise2cos(theta)=6/5
would be a rational algebraic integer and hence an integer. Positive powers
of each central rotation are dense in its full circle subgroup.

For n=1 the x and y axes are nonparallel. For n>=2, a=B+v and Ga=B+Gv
are nonparallel: they have equal nonzero B components, so parallelism would
force Ga=a, impossible for nonzero v perpendicular to the axis under a
nonidentity finite rotation. Full circle rotations about two nonparallel axes
generate SO(3). Thus the positive central rotation semigroup is dense in SO(3).

For every central word w, K contains the centred segment q^|w| Q_w(S).
For any eta>0, choose finitely many such words whose directions are an eta-net
of radial directions. Let rho be the minimum of their positive segment radii.
For every0<t<=rho, the clipped normalized set(K/t) intersect B(0,1) contains
the corresponding full unit radial segments, which are eta-dense in the
ball. Its Hausdorff distance from the ball therefore tends to0 for all t.

Any cylinder similarity f(x)=rRx+p gives f(K) subset K, so the same argument
works at p=f(0). These centres are dense in K. The full-ball weak tangent
implies dim_A K=3 by the standard tangent lower bound, or directly by finite
separated grids in the unit ball and the definition of Assouad dimension.
This is a Hausdorff limit of views of a zero-volume set, not a literal
positive-volume region of K at any finite magnification.

If epsilon<=1 then dim_H K<2. The standard inequality dim_top K<=dim_H K,
integer-valued topological dimension, and the retained interval prove
dim_top K=1. This contrasts with the sibling membrane continuum's proved
topological dimension2.

## Demonstrations actually generated

The input `compiler_borromean_seed.json` supplies one rectangle. Rotation
about B=(2,2,2) of order3 produces the standard Borromean rectangle triple.
Automatic bridges join the three seed components to the interval at0.

| Requested epsilon | Exact conclusion | Maps | Action |
|---:|---|---:|---|
| 1 | dim_H K<2; dim_top K=1; dim_A K=3 | 70 | Materialized and checked |
| 1/2 | dim_H K<3/2; dim_top K=1; dim_A K=3 | 970 | Materialized and checked |
| 1/100 | dim_H K<101/100; dim_top K=1; dim_A K=3 | 15*2^876+10 | Estimated only, about265 decimal digits |

The generated plans and models are in `compiler-demo-one`,
`compiler-demo-half`, and `compiler-demo-estimate`. The last directory contains
no model. `verify_compiler.py` independently reconstructs each scalar
certificate from its saved rational data, checks meaningful canonicalization
cases, and confirms that the allocation guard rejects the huge plan before
map construction. `compiler-verification.json` records the results.

```powershell
uv run --python 3.12 --with numpy python fractal_discovery_2026/survey/graph_compiler.py fractal_discovery_2026/survey/compiler_borromean_seed.json --epsilon 1/2 --symmetry 3 --output fractal_discovery_2026/survey/compiler-demo-half
uv run --python 3.12 --with numpy python fractal_discovery_2026/survey/verify_compiler.py
```

For arbitrary graphs supply rational vertices and index pairs as in the
example. `--symmetry 1` preserves the input without adding rotated copies;
`--axis x y z` sets B; `--axis-pieces M` and `--central-scale q` control
the source interval and central system. `--plan-only` suppresses materialization.

## A matched control and scope of claims

The separate `low_dimension.py` generates the existing m6/M6/q1/8 family
member and a matched unlinked-skeleton control. Both have244 maps, identical
contraction lists, dim_H<23/12<2, dim_top=1, dim_A=3, and C3 symmetry.
The control moves the seed rectangle by a90-degree rotation about its bridge
anchor. Its three spanning disks are

    [1,3]x[-2,2]x{0}, {0}x[1,3]x[-2,2], [-2,2]x{0}x[1,3].

They are pairwise disjoint, proving the retained triple is an unlink.
The original triple is collectively nontrivial by root's independent exact
Fox-colouring certificate. This compares designated embedded subsets; it
does not prove the complete attractors inequivalent, or exclude other links
elsewhere in the control attractor. The dimension certificate is in
`low-dimension-exact-certificate.json` and the point comparison is
`previews/low-dimension-sheet.jpg`.

## Literature and remaining questions

Finite contraction IFSs, endpoint-retained graph constructions, homogeneous
encodings of condensation sets, and overlap-driven Assouad dimension gaps
are established ideas. Generalized Menger constructions also show that
complicated spatial topology need not require high Hausdorff dimension.
The specific synthesis here is a compiler for prescribed embedded graphs
with a proved strict dimension budget and an explicit every-scale ball-tangent
mechanism. Historical originality of that synthesis is unresolved.

The weak-tangent framework and separation comparison are discussed in
[Fraser, Henderson, Olson and Robinson](https://arxiv.org/pdf/1404.1016).
[García, Corollary1.6](https://arxiv.org/pdf/1909.03148) gives a separate route
from dense rotations and WSP failure to Assouad dimension3. Recursive
Borromean art explicitly predates this investigation:
[Burkholder, Brunnian Weavings](https://archive.bridgesmathart.org/2010/bridges2010-263.pdf).

Exact Hausdorff dimensions, full intersection patterns, ambient equivalences,
and complete homeomorphism types remain open. The certificates and review
are computational/analytic research evidence, not external peer review or
proof-assistant formalizations.
