# Interval-backed Borromean continua

20 November 2026, Australia/Sydney.

This survey found an explicit connected, exactly self-similar spatial family
with pure threefold rotation symmetry and literal polygonal Borromean links
inside every similarity copy. A four-map extension has an explicit solid-ball
magnification limit at a dense set of points, despite zero volume and Hausdorff
dimension strictly below three. This is a proposed research construction, not
an established new historical category. Recursive Borromean art predates it.

The models are in `model.py`; six exact-recipe JSON exports are accompanied by
numerical checks in `summary.json`. `verify_exact.py` independently checks the
scalar enclosure and dimension inequalities with rational arithmetic and
integer-root bounds. `previews/contact-sheet.jpg` compares six finite point
samples. Their colour and apparent thickness are display choices.

## Construction

Let A=(-1,-1,-1), B=(1,1,1), u=B/sqrt(3), and G(x,y,z)=(z,x,y).
The source segment S=[A,B] has length 2sqrt(3) and lies on the C3 rotation axis.
Choose arbitrary axial angles alpha_minus, alpha_plus, and define

    a_minus(x) = (1/2) R_u(alpha_minus) x + A/2,
    a_plus(x)  = (1/2) R_u(alpha_plus) x + B/2.

On S these maps are simply the two half-interval maps. Their subsystem
attractor is exactly S, independently of the rotations. The exported examples
use alpha_minus=-alpha_plus and tan(alpha_plus/2)=0, 1/3, or 1/2.

Let L0 be the rectangle with cyclic corners

    (-2,-1,0), (2,-1,0), (2,1,0), (-2,1,0).

Set L1=G(L0), L2=G^2(L0). Add the bridge [B,(1,1,0)] and its two rotations.
For an integer m>=2 subdivide every ring and bridge edge into pieces of
length 1/m. There are 36m ring pieces and 3m bridge pieces.

For each piece U->V take a proper rotation Q carrying (B-A)/|B-A| to
(V-U)/|V-U|, with a freely chosen roll angle beta, and define

    f_UV(x) = r Q x + (U+V)/2,    r=1/(2m sqrt(3)).

Thus f_UV(A)=U and f_UV(B)=V exactly. To ensure C3 symmetry, define all maps
on the first rectangle and bridge, then take their two conjugates G f G^-1
and G^2 f G^-2. The source endpoints are fixed by G. The model's frame()
function chooses a reproducible right-handed reference frame; rational
half-angle tangents define its displayed rolls through
cos(beta)=(1-q^2)/(1+q^2), sin(beta)=2q/(1+q^2).

The base family has 39m+2 similarities, including 80 when m=2. Let K be its
unique nonempty compact attractor. These maps are fixed at all generations;
every f_w(K) is an exact smaller copy of K.

## Literal structure, connectedness and spatiality

The interval subsystem implies S is a subset of K. Consequently f_UV(S) is
the whole straight segment [U,V], so K contains the three rectangle loops,
the bridges, and the source axis **literally**. This avoids the gap between a
path homotopy to a knot and an actually embedded knot.

Let Gamma be the finite graph made of these segments. It is connected.
Begin the Hutchinson iteration with an invariant ball containing Gamma. The
two axial copies meet at 0 and retain A,B. The edge images of each connected
iterate join at the graph vertices; the bridges connect all three rings to B.
Every image union is therefore connected. The decreasing compact iterates
converge to connected K.

There is also a direct path-connectedness proof. Every map translation f_i(0)
lies on Gamma. For a point x with address i1 i2..., join each pair
f_(i1...in)(0), f_(i1...in+i)(0) by an image of a polygonal path in Gamma.
These paths have diameters tending to zero geometrically. Concatenating them
on shrinking time intervals yields a continuous path from 0 to x.

The retained vertices (-2,-1,0),(2,-1,0),(2,1,0),(0,-2,-1) have nonzero affine
determinant (-8), so K spans R^3. Conjugation by G permutes the complete map
list. Uniqueness of the attractor gives G(K)=K: genuine 120-degree rotational
symmetry about (1,1,1).

## Why the three loops are collectively linked

All three are disjoint planar rectangles. D0=[-2,2]x[-1,1]x{0} spans L0.
The rotated loop L1 lies in x=0 and has either y=+/-2 or z=+/-1. Its points
with z=0 therefore have y=+/-2, so L1 misses D0. A sufficiently small regular
neighbourhood of D0 is a ball disjoint from L1, separating L0 from L1.
Both are unknots, hence this pair is the two-component unlink. Applying G
proves the same for the other two pairs.

Root's independent `../research/verify_link.py` uses an exact rational,
nondegenerate projection and Fox 3-colouring equations. Its reported count
is 3 for the full triple versus 27 for the three-component unlink, while each
pair has 9. The triple therefore is not the unlink. Together with the
pairwise unlink result this rules out splitting the triple into sublinks.
The coordinate rectangles are the standard rectangular Borromean arrangement.
No Milnor-invariant computation or numerical knot recognition is required for
the above conclusions. This report relies on root's separate diagram check
for the collective nontriviality, not on the appearance of a rendering.

Every finite word f_w carries this embedded triple into K, retaining its
ambient link type. Given any x in K and epsilon>0, a sufficiently deep prefix
of an address of x has diameter below epsilon; its embedded triple lies
inside B(x,epsilon). Thus arbitrarily small copies of the link occur near
every point of K. This does **not** claim that K itself has three connected
components, or that K is homeomorphic to the Borromean link. K is connected.

## Explicit solid-ball magnifications

Optionally add four maps, with 0<q<1:

    h0(x)=q x,
    hx(x)=q Rx(theta)x,
    hy(x)=q Ry(theta)x,
    hz(x)=q Rz(theta)x,

where cos(theta)=3/5 and sin(theta)=4/5. The default q=1/4. They all fix 0,
already in K, so connectedness is preserved; G cyclically permutes hx,hy,hz.
The same skeleton remains a subset. This extension has 39m+6 maps.

The angle theta is an irrational multiple of pi. Indeed, if it were rational,
2cos(theta) would be a rational algebraic integer, hence an integer, whereas
2cos(theta)=6/5. The positive powers of Rx(theta) are therefore dense in the
circle of x-axis rotations, and similarly for y-axis rotations. Their positive
semigroup is dense in SO(3), since x and y rotations generate SO(3).

For every n, q^-n K contains R_word(S) for every rotation word of length at
most n: pad shorter words with identity h0 before rescaling. The rotations of
the centred diameter S fill the entire closed ball B(0,sqrt(3)). Density and
compactness show that the increasing sets of rotated segments approximate
that ball in Hausdorff distance. Since h0(K)=qK is a subset of K, the clipped
sets

    (q^-n K) intersect B(0,sqrt(3))

are nested compact sets and converge in Hausdorff metric to the full ball.
In fact the convergence holds for **every** sufficiently small normalization
scale, not just q^n. For any epsilon>0 choose a finite epsilon-net of
directions among positive rotation words w_1,...,w_N. Their centred segments
q^|w_j| R_wj(S) all lie in K. Below the smallest of these segment radii,
every clipped normalized view contains the corresponding full unit radial
segments, so its Hausdorff distance to the unit ball is at most epsilon.
Thus ((K/t) intersect B(0,1)) tends to B(0,1) as t decreases to zero.

This proves an explicit every-scale ball tangent at 0, rather than only
invoking an abstract existence theorem. The usual weak-tangent dimension
bound implies dim_A K=3. Applying a finite similarity f_w proves the same
local ball magnification limit at f_w(0); those points form a dense subset
of K. The four central maps do not need to include h0 for the finite-net
proof, although h0 provides a particularly simple explicit WSP obstruction.

The original K has no interior and zero volume when the covering inequalities
below hold. A solid magnification limit is compatible with this. It is not a
claim that K becomes a literal solid after a finite zoom, that views centred
at arbitrary points have this limit, or that every point has this tangent.

There is also an explicit WSP obstruction: h0^-n hx^n=Rx(n theta) has
nonidentity subsequences approaching identity. Common-fixed-point words
likewise obstruct OSC. As an independent literature route, García's
Corollary 1.6(1) applies to full-span self-similar sets failing WSP whose
positive rotation products are dense in SO(3), and yields the same dim_A=3.

Because dim_H K<3, Fraser–Henderson–Olson–Robinson Theorem 1.4 excludes
**every alternative finite similarity IFS satisfying WSP** for the same K.
In particular no such OSC presentation exists. This is an intrinsic
dimension-gap statement, not merely a feature of a redundant list of maps.

## Enclosures and dimensions

For m>=2 the ball radius 5/2 is invariant. The axial translation has norm
sqrt(3)/2. An edge translation has squared norm at most
4+(1-1/(2m))^2; the edge ratio is 1/(2m sqrt(3)). The rational verifier uses
r<289/(1000m) and squares only positive quantities. Central maps clearly
preserve the ball. These bounds are independent of all allowed rolls.

The scalar covering sum is

    P_m(s)=2(1/2)^s + 39m (1/(2m sqrt(3)))^s

for the base family, with +4q^s for the overlap extension. The unique root is
only a **Hausdorff upper bound** without separation assumptions.

| Recipe | Maps | Numerical covering root | Certified strict dim_H upper |
|---|---:|---:|---:|
| m=2 base | 80 | 2.48014991 | 5/2 |
| m=2 overlap, q=1/4 | 84 | 2.56264511 | 13/5 |
| m=3 overlap, q=1/4 | 123 | 2.36494823 | 12/5 |
| m=4 overlap, q=1/4 | 162 | 2.26129760 | 23/10 |

Every displayed bound is proved by an exact rational upper enclosure of
P_m(s) below 1; `exact_certificate.json` records it. The same verifier gives
P_m(3)<1 and hence zero ordinary volume. The interval gives dim_H K>=1.
The exact Hausdorff dimension, full intersection structure, and complete
homeomorphism type are not established.

## A generalization worth investigating

The graph construction is not limited to Borromean rectangles. Any finite
connected polygonal graph, augmented to contain a reference interval, can
be retained literally by two half-interval maps and one endpoint similarity
per sufficiently subdivided graph edge. Add the four central rotation maps
at a point on that interval. These connected self-similar continua contain
an exact copy of the prescribed embedded graph inside every similarity copy.

If subdivision gives O(m) edges of length O(1/m), choose central q_m->0.
For every epsilon>0 the covering sum at 1+epsilon tends to
2^(-epsilon)<1. Therefore sufficiently large m yields

    1 <= dim_H K < 1+epsilon,    dim_A K=3,

while retaining any prescribed finite link collection and the dense set of
every-scale solid-ball tangents. For the C3 Borromean family q_m=1/(4m^2) suffices. This
is an elementary candidate general theorem; its historical status has not
been determined. The required m can be enormous for very small epsilon,
so it is a theoretical result rather than a practical rendering prescription.

## Prior art and scope

Recursive Borromean geometry is old. Douglas Burkholder's 2010 *Brunnian
Weavings* explicitly iterates smaller Borromean designs into larger ones.
Richard Southwell's 2014 demonstration describes Borromean rings made from
Borromean rings. Robert Fathauer published iterative fractal knots in 2007.
Our exact finite similarity definition, literal retained graph, arbitrary
small-scale copies, and independently engineered dimension gap are the
specific items to compare, rather than claiming invention of recursive links.

Endpoint IFS constructions and overlap-driven dimension gaps are also
established frameworks. A potentially useful contribution is their explicit
combination with embedded higher-order links and a direct ball-tangent proof.
No exhaustive novelty search or independent external review has been done.

Sources checked in this investigation:

- [Burkholder, Brunnian Weavings (2010)](https://archive.bridgesmathart.org/2010/bridges2010-263.pdf).
- [Southwell, Borromean rings fractal (2014)](https://www.youtube.com/watch?v=dh9s1vyzy7s).
- [Fathauer, Fractal Knots Created by Iterative Substitution (2007)](https://archive.bridgesmathart.org/2007/bridges2007-335.pdf).
- [García, Assouad dimension and local structure of self-similar sets with overlaps in R^d, Corollary 1.6 and Theorem 1.9](https://arxiv.org/pdf/1909.03148).
- [Fraser, Henderson, Olson and Robinson, On the Assouad dimension of self-similar sets with overlaps, Theorem 1.4 and weak-tangent discussion](https://arxiv.org/pdf/1404.1016).
- [Cantarella et al., Criticality for the Gehring link problem, planar perpendicular Borromean symmetry discussion](https://jasoncantarella.com/downloads/papers/ropcrit/gehring_criticality.pdf.bak.pdf).

## Reproduction

From the workspace root:

```powershell
uv run --python 3.12 --with numpy python fractal_discovery_2026/survey/model.py
uv run --python 3.12 python fractal_discovery_2026/survey/verify_exact.py
uv run --python 3.12 --with numpy --with moderngl --with pillow python fractal_discovery_2026/survey/render.py
```

The mathematical definition is rational data plus explicitly specified square
roots and rotations. JSON decimal matrices and the random point previews
are numerical implementations. Root's link certificate is a separate exact
topological check. Passing scripts do not independently verify every analytic
deduction in this report and are not proof-assistant formalizations.
