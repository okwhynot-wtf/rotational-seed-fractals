# Exact definitions

Both families are attractors of a finite list of contracting similarities. The same maps act at every generation:

\[
K=\bigcup_i f_i(K),\qquad f_i(x)=r_iO_ix+b_i,\quad 0<r_i<1.
\]

Every finite composition maps the entire attractor onto a smaller copy contained in it. This is exact self-similarity; the rendered surface is a finite visualization.

## The retained seed

The construction first preserves a simple set exactly. Two half-scale maps retain a line segment. Four half-scale maps retain a square. Further similarities then place entire copies of the eventual fractal around that seed.

For a source segment with endpoints \(A,B\), an edge map is chosen so that \(f(A)=U\) and \(f(B)=V\). It therefore retains the whole target segment \([U,V]\), allowing a finite connected polygonal graph to be built literally inside the attractor.

## Linked continuum · threefold symmetry

The reference graph uses three rectangular loops. The first has corners

\[
(-2,-1,0),\ (2,-1,0),\ (2,1,0),\ (-2,1,0).
\]

The other two are its images under \(G(x,y,z)=(z,x,y)\). Bridges attach them to the source interval on the diagonal axis. Their selected three-loop subset has the Borromean property: all three are collectively linked, while each pair is an unlink.

Edge maps are included in complete conjugate orbits under \(G\), establishing threefold rotational symmetry. Axial subdivisions and roll angles can vary. This does not establish that the full symmetry group is exactly C3.

The central extension adds \(qx,qR_xx,qR_yx,qR_zx\), where the rotations have cosine \(3/5\) and sine \(4/5\). Its role is the [full-ball tangent result](results.md), independently of the retained link.

Read the [complete graph recipe and proof](../survey/REPORT.md) and inspect the [parameter generator](../survey/model.py).

## Membrane continuum · fourfold symmetry

Let \(S=[-1,1]^2\times\{0\}\). Four maps tile the square:

\[
f_{ab}(x)=\tfrac12x+(a/2,b/2,0),\qquad a,b\in\{-1,1\}.
\]

Let \(Z\) rotate about the z axis through \(\pi/2\), and define

\[
Q=\frac1{125}\begin{pmatrix}53&-60&96\\60&-75&-80\\96&80&-3\end{pmatrix},
\qquad h_k(x)=qZ^kQZ^{-k}x,\quad k=0,1,2,3.
\]

Together these eight maps define \(K_q\), for \(0<q<1/2\). Rational q gives rational map coefficients. The reference member uses \(q=1/4\). Conjugation by Z permutes the maps, establishing fourfold rotational symmetry.

The square is retained exactly. Every displayed square panel is a finite word image of that square, so these panels are genuine subsets of the infinite attractor.

Read the [complete membrane definition](../constructive/MEMBRANE.md) and [source implementation](../constructive/membrane.py).
