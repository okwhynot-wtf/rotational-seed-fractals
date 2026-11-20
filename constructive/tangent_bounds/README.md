# Explicit full-ball zoom bounds

These are finite, reproducible certificates for the **original eight-map
membrane with q=1/4**, using the denominator-125 rotation defined in
[the membrane report](../MEMBRANE.md). They give quantitative instances of
the existing full-ball tangent argument. No historical novelty or optimal
rate is claimed.

Write B for the closed unit ball and K for that membrane attractor. The
certificate proves the following bounds **for every** positive t below the
stated threshold, rather than only at a sampled sequence of scales:

| Maximum core-word depth n | Scale threshold t ≤ 4⁻ⁿ | Certified upper bound on d_H((K/t) ∩ B, B) |
|---|---|---|
| 3 | 1/64 | 0.338487238454 |
| 4 | 1/256 | 0.212585963237 |
| 5 | 1/1024 | 0.092423119034 |
| 6 | 1/4096 | 0.021264176895 |
| 7 | 1/16384 | 0.009278720270 |

Thus, for example, every normalized view centred at the origin at scales
t ≤ 1/16384 is within **one percent of the ball radius** of the full ball in
Hausdorff distance. This is a statement about a zero-volume set and does not
assert that any view contains a solid ball. The bound is not a visual
resolution or pixel measurement.

The same estimates transfer to a cylinder centre p=f_w(0). If f_w has
contraction ratio r_w, replace the scale threshold by r_w 4⁻ⁿ. The inclusion
f_w(K) ⊆ K and rotational invariance of B prove this directly.

## Why this covers every point of the ball

The retained square contains a centred unit disk. A core word v of length
k retains a centred disk of radius 4⁻ᵏ whose unit normal is Q_v e_z. Therefore,
for t ≤ 4⁻ⁿ, every core word of length k ≤ n supplies its entire unit disk
inside (K/t) ∩ B. Include the empty word as well.

For a unit normal a and a point x in B, orthogonal projection onto the plane
a⊥ remains in its unit disk. The distance to that disk is |a·x|. Consequently
it is enough to prove that every unit direction u has some retained normal
a with |a·u| ≤ ε.

Parameterize each face of the cube [-1,1]³ radially onto the unit sphere.
Subdivide a face into M×M squares and take each square's centre. On a face,
normalization v ↦ v/|v| has derivative norm at most one: |v|≥1 throughout
each segment in that face. Every point of the face is therefore within
√2/M of the normalized centre of its cell. We use the strict rational
upper bound 3/(2M) for this radius. Since |a·u| is 1-Lipschitz in u, an
upper bound δ on the selected plane distance at each mesh point implies
the complete-sphere bound δ + 3/(2M). Multiplying u by a radius at most one
then gives the same bound throughout B.

The supplied certificates use M=200: the rational covering-radius bound is
3/400 = 0.0075. Only the three positive cube faces need explicit checks,
because |a·(-u)|=|a·u|. There are **120,000 checked points**, representing
240,000 sphere-mesh points with antipodal symmetry. The analytic cell-radius
bound covers the intervening directions; a sampled maximum alone would
not certify the result.

## Exact arithmetic and witnesses

The four core rotation matrices are N_j/125, where N_j are the integer
C4 conjugates of

```
 53  -60   96
 60  -75  -80
 96   80   -3
```

For all core words of length at most n, the checker constructs their normals
using Python integers and puts them over the common denominator 125ⁿ.
It verifies that every normal numerator A has |A|²=125²ⁿ. The positive-face
mesh uses vectors X whose fixed coordinate is M and whose other coordinates
are -M+2i+1 and -M+2j+1, with 0≤i,j<M. The corresponding unit direction is
X/|X|. For a selected normal, the squared plane distance is the exact rational
number

```
(A·X)² / (125²ⁿ |X|²).
```

NumPy's floating-point matrix multiplication is used **only to propose a
normal index** at each mesh point. The saved witness list contains those
indices. Every selected dot product, squared distance, comparison and square
root upper enclosure is then checked using arbitrary-precision integers and
fractions. A poorly chosen floating-point witness could weaken a bound or
cause a requested target to fail; it cannot create a false certified bound.

The largest selected squared distance is stored exactly. If it equals A/B,
the square-root enclosure uses

```
p = floor(sqrt(floor(A D²/B))) + 1,   D=10¹²,
δ = p/D.
```

The checker verifies δ²>A/B. Adding 3/(2M) gives the table's upper bound.
Decimal upper enclosures in the JSON are formed by integer division with
rounding upwards. Elapsed-time fields are diagnostics, not mathematical
inputs.

The word counts, including the empty word, are 85, 341, 1,365, 5,461 and
21,845 at depths 3 through 7. These are counts of included words, not a claim
that their planes are all different. Plane-index ordering is defined by
`normals()` in the checker, and witness hashes are included in the certificate.

## Reproduce

From the repository root, verify the existing certificate using only the
Python standard library:

```sh
python constructive/tangent_bounds/certify.py --verify
```

To regenerate the witnesses and certificate, install NumPy and run:

```sh
python constructive/tangent_bounds/certify.py
```

The recorded run checked all five bounds in about two seconds, after a
roughly 18-second witness search on the development machine. The search
uses 256-point batches; it does not allocate the full mesh-by-plane matrix.
Exact verification does not require NumPy or the renderer. The proof above
and the finite computation remain subject to external mathematical review.
