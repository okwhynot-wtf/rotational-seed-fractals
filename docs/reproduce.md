# Reproduce the construction

The repository contains the definitions, parameter generators, exact finite checks, research notes, and rendering sources. Python examples below run from the repository root. The optional `uv` runner supplies isolated dependencies.

## Graph recipes and exact bounds

```sh
uv run --python 3.12 --with numpy python survey/model.py
uv run --python 3.12 python survey/verify_exact.py
uv run --python 3.12 python research/verify_link.py
```

The model exports decimal matrices and numerical consistency checks. The scalar and link verifiers use rational arithmetic for their stated questions. Successful execution does not prove historical novelty or every analytic assertion in the reports.

## Membrane

```sh
uv run --python 3.12 --with numpy python constructive/membrane.py
uv run --python 3.12 --with numpy --with matplotlib python constructive/membrane.py --render --q 0.25 --depth 4
```

The finite square panels are retained subsets. Depth controls the displayed word list; it does not change the mathematical attractor.

## Build this website

```sh
uv run --python 3.12 --with markdown python scripts/build_site.py
```

The build reads `docs/` and the research manuscript and writes static files to `site/`. It preserves `site/assets/` media. The output supports GitHub Pages under a repository subpath, without a server runtime.

To use another repository identity, pass `--repo owner/name`. Pass `--url` for the public site URL. Mathematics uses MathJax from a CDN; all geometry images and films are local assets.

## Evidence and limitations

Start with [definitions](definition.md), [results](results.md), and the [paper draft](paper.md). The [internal review](../research/INDEPENDENT_REVIEW.md) distinguishes proofs from finite implementation checks. See [media](media.md) for what the images depict and [provenance](provenance.md) for authorship and reuse.
