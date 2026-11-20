# Exact overlaps, smaller dimension bounds, and the residual set

20 November 2026. This follow-up preserves the reference definitions in the
parent directory. It studies the original membrane at q=1/4 and a separately
defined norm-13 rotation variant. All word conventions are outermost first.

## Results

| Model | Explicit equal words | Common contraction | Certified improved upper bound |
|---|---|---|---|
| Original denominator-125 rotation | 47131103333 = 12222011470 | 2^(-13) | dim_H K < 2.271553252338126 |
| Norm-13 variant | 410033 = 211040 | 2^(-7) | dim_H K < 2.270907424784688 |

An equality in this table means equality of the entire affine maps, not
merely a shared point. Both models have 2<dim_H K, topological dimension 2,
Assouad dimension 3 and the every-scale full-ball tangent property.
Neither exact Hausdorff dimension is known. No global shortest-overlap claim
is made for the original model; the first search checked 340 core rotation
words of lengths 1–4 within the particular plane-intersection construction
below. A separate exact modular screen distinguishes all 37,449 words of
length at most 5, including the empty word, for each model. Therefore the
norm-13 relation is shortest in the precise sense of minimizing the maximum
of the two word lengths: that minimum is 6. The original minimum lies
between 6 and 11. The free-rotation argument below shows that every affine
coincidence has equal word lengths, so the norm-13 minimum combined length
is also established: 12.

The old similarity bound is 2.271553303163612… for both models. Thus exact
overlaps prove that neither model attains that value. The original improvement
is small, approximately 5.083×10^(-8); the norm-13 improvement is approximately
0.0006458784. These are mathematically strict changes, not visual distinctions.

## Notation and the first exact relation

Digits 0,1,2,3 are the square-tiling maps with respective signs
(−1,−1),(−1,+1),(+1,−1),(+1,+1). Digits 4,5,6,7 are h_0,h_1,h_2,h_3.
For a base-only word v of length m,

    F_v(x)=2^(−m)x+N_v/2^m,

where the x and y entries of N_v are odd integers strictly between −2^m
and 2^m; its z entry is zero. Every such pair occurs exactly once.

For the original model put H=h_0 h_3=(1/16)R, where R=Q_0 Q_3. Exact
matrix multiplication gives

    R = [[105, −15576, 1232],
         [−15400, 105, 2640],
         [−2640, −1232, −15351]] / 15625,
    R(−7,15,0)=(−15,7,0).

Let W=(−7,15,0), V=(−15,7,0), and c=(−1,−1,0). Define base words u,v,e by

    |u|=8,   N_u=V,
    |v|=9,   N_v=c+32W=(−225,479,0),
    |e|=1,   N_e=c.

Then

    H F_v(x)
      = 2^(−13) R x + 2^(−13) R(c+32W)
      = 2^(−13) R x + V/256 + 2^(−13) R c
      = F_u H F_e(x).

Decoding the base numerators gives the first relation in the table. This
identity has been checked independently by composing all 3×3 matrices and
translations with Fraction arithmetic.

The single rotation Q maps (5,−6,0) to (5,6,0), but this alone does not give
an exact affine-word collision with just one h. The intersection direction
has unequal 2-adic valuations in its two coordinates. When the h is moved
between different base-word positions, the outer dyadic translation difference
has equal valuations in x and y, so it cannot lie in that direction. For equal
positions, the possible h(S) translations remain inside disjoint small balls
around distinct dyadic tile centres; equal centres reduce to equal base words.
The two-rotation block above removes that parity obstruction.

## Thirty-two relations and an improved cover

Rotate the construction through the four C4 symmetries, choose W or −W,
and choose either sign independently in c=(±1,±1,0). This gives 32 exact
equalities. In each one, the left word has two core letters followed by nine
base letters, while the right word begins with a base letter. Both words have
length L=11 and contraction 2^(−p), p=13.

Replacing a left word by its right partner strictly decreases lexicographic
order without changing word length or its affine map. Therefore repeated
replacement terminates for every finite word. All length-n cylinder maps can
be represented by words avoiding the 32 left patterns. These patterns are
distinct and have no proper suffix equal to a prefix of any other pattern;
this follows from their core-core-base…base form and is also exhaustively
verified in the certificate.

For s>0 write

    A(s)=4·2^(−s)+4·2^(−2s),
    B(s)=32·2^(−ps).

Let Z_n(s) sum r_w^s over allowed length-n words. The absence of overlapping
forbidden patterns gives the exact weighted recurrence

    Z_n=A Z_(n−1)−B Z_(n−L),     n≥L,
    Z_n=A^n,                    0≤n<L.

Indeed, append any letter to an allowed prefix, then subtract exactly those
extensions completing a forbidden pattern. Such a pattern cannot overlap an
earlier forbidden occurrence, which is precisely why the subtraction term
is B Z_(n−L).

Let s_* satisfy A(s_*)−B(s_*)=1, and put y=2^(−s_*). Equivalently,

    4y+4y²−32y^13−1=0,

with y in (207/1000,21/100). The certificate brackets this root in rational
arithmetic, verifies strict monotonicity of the polynomial on the interval,
and verifies B(s_*)(L−1)<1.

Here is an elementary boundedness argument avoiding a numerical spectral-radius
claim. With D_n=Z_n−Z_(n−1), the recurrence at s_* becomes

    D_n=B(D_(n−1)+…+D_(n−L+1)).

Its initial differences are nonnegative. On successive blocks of L−1 indices,
the maximum difference decreases by at least the factor B(L−1)<1. Hence
sum D_n is finite and Z_n is bounded uniformly. Allowed cylinder sets cover K
and have diameters at most 2^(−n)diam K. For any s>s_*, their s-weight sum is
at most 2^(−n(s−s_*)) Z_n(s_*) and tends to zero. Thus dim_H K≤s_*.

The exact root and logarithm certificate yields

    2.271553252338125 < s_* < 2.271553252338126.

The logarithm bracket uses 64 terms of the rational atanh series and an
explicit geometric tail bound. The final decimal upper endpoint is therefore
certified, rather than a rounded floating-point value.

## The norm-13 variant

Keep the four base maps, q=1/4, and C4 conjugation, but replace Q by

    P = [[−3,4,12],[12,−3,4],[4,12,−3]] / 13.

This is a proper rotation with cos θ=−11/13, axis (1,1,1)/√3. The rotation
angle is an irrational multiple of π by the rational algebraic-integer
argument. Its C4 conjugate has a different axis; the same two-circle/Lie-algebra
argument gives a dense SO(3) rotation semigroup. All basic membrane proofs
therefore transfer. The reference definition has not been changed.

Now P(−3,1,0)=(1,−3,0). Taking W=(−3,1,0), V=(1,−3,0), c=(−1,−1,0),
|u|=4, N_u=V, |v|=5, N_v=c+8W=(−25,7,0), |e|=1, N_e=c gives

    h_0 F_v=F_u h_0 F_e,
    F_410033=F_211040.

The same four symmetries, two W signs and four c choices give 32 forbidden
patterns, now one core letter followed by five base letters. Their length is
L=6 and their contraction is 2^(−7). The preceding proof applies with p=7:

    4y+4y²−32y^7−1=0,
    2.270907424784687 < −log_2(y) < 2.270907424784688.

Numerical direction-coverage tests also found faster coverage for this rotation:
using all core words through depth 5, the maximum distance over 12,000 tested
unit-sphere points to the 1,365 retained unit disks was about 0.00654, versus
0.0800 for the original rotation. This is a finite-sampling diagnostic, not
a certified uniform covering rate.

Even if freeness of the rotation generators is separately established, these
affine overlaps persist. Rotation-word freeness is therefore insufficient to
apply a theorem requiring distinct full affine word maps.

## Both core rotation alphabets are free

There is an elementary proof, with only small finite modular premises to
check. For p=5 use the six integer quaternions (1,±2,0,0) and coordinate
permutations. For p=13 use the fourteen quaternions (1,±2,±2,±2) together
with (3,±2,0,0) and coordinate permutations. Each has squared norm p; the
listed quaternions occur in conjugate pairs. Normalize by √p to obtain
unit quaternions, hence rotations.

Choose a square root i_p of −1 modulo p: i_5=2 and i_13=5. The map

    a+bi+cj+dk  ->  [[a+i_p b, c+i_p d],
                    [−c+i_p d, a−i_p b]]  modulo p

is an algebra homomorphism, as follows by checking the quaternion basis
relations. Every listed generator becomes a nonzero rank-one matrix. The
finite certificate checks all 36 or 196 ordered generator pairs and finds
that their product is zero exactly for conjugate pairs, i.e. a generator
followed by its inverse rotation.

A product of rank-one matrices u_j v_j^T is nonzero whenever each adjacent
scalar v_j^T u_(j+1) is nonzero. Consequently the matrix of any nonempty
freely reduced quaternion word is nonzero modulo p. If its rotation were
identity, its integer quaternion product would be a real scalar a. Its norm
requires a²=p^m, where m is the reduced word length. Odd m is impossible;
for even m≥2 the scalar a is divisible by p, contradicting the nonzero
matrix. This proves the corresponding rotation groups are free of ranks
3 and 7.

For the original rotation, let X,Y,T denote the norm-5 rotations about
the x,y,z axes (T is unrelated to the quarter-turn C4 symmetry Z). Direct
quaternion multiplication gives

    (1−2j)(1−2k)(1+2j)=5+8i+6k,
    Q=Y^(−1) T^(−1) Y.

Its C4 orbit is

    Y^(−1)T^(−1)Y,  X T^(−1)X^(−1),
    Y T^(−1)Y^(−1), X^(−1)T^(−1)X.

These four conjugates freely generate a rank-four subgroup. In a reduced
word in these generators and their inverses, adjacent equal conjugators
merge powers of T with the same sign, while distinct conjugators leave a
nonempty connecting word in X,Y. Since that connecting word contains no T,
the resulting word in the free group on X,Y,T cannot reduce to identity.

For the norm-13 model, the four core quaternions are

    (1,2,2,2), (1,−2,2,2), (1,−2,−2,2), (1,2,−2,2),

normalized by √13. They select one generator from each of four distinct
inverse pairs of the rank-seven free group and therefore freely generate
a rank-four subgroup as well.

Thus in both membrane models equality of full affine maps forces equality
of the ordered core-letter subsequences. Equality of contraction factors
then forces equality of the number of base letters. Every exact coincidence
therefore has equal ordinary word lengths. This justifies the shortest-word
conclusion for the norm-13 model and explicitly demonstrates **free core
rotations coexisting with exact affine overlaps**.

## The residual set carries the excess dimension

Let

    D=union over all finite words w of F_w(S),     E=K\D,

including the empty word. D is a countable union of exact square sheets and
has Hausdorff dimension exactly 2. It is dense in K by the contraction argument.
Each sheet is closed in K and has empty relative interior: otherwise a relative
neighbourhood contained in its plane could not contain disks in a dense set
of orientations. Thus D is meagre, E is a dense G_delta, and E is uncountable
because K is a nontrivial connected compact metric space with no isolated points.

The strict lower bound dim_H K>2 uses an established theorem, independently
read for this follow-up. Farkas–Fraser Corollary 3.1 applies to ordinary finite
self-similar attractors through the full-shift case, without a separation
condition. Positive Hausdorff measure in the critical dimension forces Ahlfors
regularity. If dim_H K were 2, its retained square would supply positive
critical measure, forcing Assouad dimension 2 and contradicting the proved
value 3. [Primary paper, Corollary 3.1, p. 7](https://arxiv.org/pdf/1411.0867).

Countable stability gives

    dim_H K=max(dim_H D,dim_H E)=max(2,dim_H E),

so **dim_H E=dim_H K>2**. The residual set omitted as literal points from
every finite square-only rendering therefore carries the full Hausdorff
dimension. This does not prevent the finite sheets converging in Hausdorff
distance to the whole attractor.

The same regularity theorem also implies H^d(K)=0 at d=dim_H K: if it were
positive, K would be Ahlfors d-regular and have Assouad dimension d<3.
“Carries the dimension” must consequently not be replaced by a claim of
positive critical Hausdorff measure on E.

## Reproduction and limitations

Run `python certify_bounds.py` from this directory or by its full path.
It uses only the standard library and verifies all 64 full affine equalities,
the combinatorial pattern conditions, polynomial root brackets, recurrence
stability, and logarithm bounds. `find_relations.py` reproduces the restricted
search that led to the original relation.

`screen_short_words.py` gives the bounded noncollision certificate. It reduces
every rational affine map modulo 2^31−1, after checking denominators are
invertible through Python's modular-inverse operation. All 37,449 reduced
maps differ for each model, so the corresponding rational maps necessarily
differ. It does not use a modular collision as evidence of rational equality.

The certificates establish an upper bound, not the actual dimension or a
complete overlap classification. They do not prove that the displayed word
relations generate all coincidences. The residual conclusion is a cited
analytic deduction, not a finite computation or a novelty claim. External
mathematical review remains appropriate.
