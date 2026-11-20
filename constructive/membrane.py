"""Exact rational definition and finite, genuine sheet subsets of the membrane IFS."""
from __future__ import annotations
import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
Z = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=int)
# Rotation through acos(-3/5) about (4/5, 0, 3/5).
N = np.array([[53, -60, 96], [60, -75, -80], [96, 80, -3]], dtype=int)


def maps(q=0.25):
    linear, translate = [], []
    for a, b in itertools.product((-1, 1), repeat=2):
        linear.append(np.eye(3) / 2)
        translate.append(np.array([a, b, 0]) / 2)
    for k in range(4):
        z = np.linalg.matrix_power(Z, k)
        linear.append(q * (z @ N @ z.T) / 125)
        translate.append(np.zeros(3))
    return np.array(linear), np.array(translate)


def upper_dimension(q=0.25):
    lo, hi = 2.0, 4.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if 4 * 0.5**mid + 4 * q**mid > 1:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def sheets(depth=3, q=0.25):
    """Each returned square is literally contained in the infinite attractor.

    Trailing planar-tile maps produce subsets of an already included square,
    so enumerate the base square and words ending in an h-map only.
    """
    a, t = maps(q)
    square = np.array([[-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0]], float)
    result = [(square, 0, -1)]
    frontier = [(np.eye(3), np.zeros(3), -1)]
    for n in range(1, depth + 1):
        nxt = []
        for m, b, first in frontier:
            for j in range(8):
                child_m, child_b = m @ a[j], m @ t[j] + b
                label = j if first < 0 else first
                if j >= 4:
                    result.append((square @ child_m.T + child_b, n, label))
                nxt.append((child_m, child_b, label))
        frontier = nxt
    return result


def verify():
    assert np.array_equal(N.T @ N, 125**2 * np.eye(3, dtype=int))
    assert round(np.linalg.det(N)) == 125**3
    axis = np.array([4, 0, 3], dtype=int)
    assert np.array_equal(N @ axis, 125 * axis)
    assert int(np.trace(N)) == -25  # cos(theta)=(tr(Q)-1)/2=-3/5
    a, t = maps()
    # Conjugation by Z permutes the actual maps, not just their samples.
    perm = []
    for mat, shift in zip(a, t):
        candidates = [j for j in range(8)
                      if np.allclose(Z @ mat @ Z.T, a[j], atol=1e-15)
                      and np.array_equal(Z @ shift, t[j])]
        assert len(candidates) == 1
        perm.append(candidates[0])
    # The Q1-image of the Q0 axis is not parallel to the Q0 axis.
    n1 = Z @ N @ Z.T
    cross = np.cross(axis, n1 @ axis)
    assert any(cross)
    report = {
        "q": "1/4", "Q0_numerator": N.tolist(), "Q0_denominator": 125,
        "axis": ["4/5", 0, "3/5"], "cos_angle": "-3/5", "sin_angle": "4/5",
        "C4_map_permutation": perm,
        "density_axis_cross_integer": cross.tolist(),
        "hausdorff_lower": 2, "hausdorff_upper": upper_dimension(),
        "similarity_upper_exact": "1 + log_2(1 + sqrt(2))",
        "topological_dimension": 2, "assouad_dimension": 3,
        "sum_cubed_ratios": 4 * 0.5**3 + 4 * 0.25**3,
        "claim_status": "Elementary argument in MEMBRANE.md; not independently peer reviewed",
    }
    (HERE / "membrane_checks.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def render(depth=4, q=0.25, output=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    from matplotlib.colors import to_rgb
    panels = sheets(depth, q)
    fig = plt.figure(figsize=(16, 9), facecolor="#08121b")
    views = [(23, -56), (58, -42)]
    palette = np.array([to_rgb(c) for c in
                        ["#68b9bc", "#76a3d3", "#c2a173", "#d58f63",
                         "#de8a5a", "#60c3bc", "#c5b1d7", "#d4b463"]])
    light = np.array([0.3, -0.5, 0.8]); light /= np.linalg.norm(light)
    for pos, (elev, azim) in enumerate(views, 1):
        ax = fig.add_subplot(1, 2, pos, projection="3d", computed_zorder=False)
        ax.set_facecolor("#08121b")
        polygons, colors = [], []
        for vertices, n, label in panels:
            normal = np.cross(vertices[1] - vertices[0], vertices[2] - vertices[0])
            normal /= np.linalg.norm(normal)
            shade = 0.5 + 0.5 * abs(normal @ light)
            color = np.array(to_rgb("#244c60")) if n == 0 else palette[label]
            polygons.append(vertices)
            colors.append(np.clip(color * shade, 0, 1))
        collection = Poly3DCollection(polygons, facecolors=colors,
                                      edgecolors=(0.03, 0.06, 0.08, 0.6), linewidths=0.12,
                                      zsort="average")
        ax.add_collection3d(collection)
        ax.set(xlim=(-1.05, 1.05), ylim=(-1.05, 1.05), zlim=(-0.65, 0.65))
        ax.set_box_aspect((2.1, 2.1, 1.3))
        ax.view_init(elev=elev, azim=azim)
        ax.set_axis_off()
    fig.text(.055, .91, "MEMBRANE CONTINUUM", color="#ecf3f4", fontsize=25, weight="bold")
    fig.text(.055, .865, f"Fourfold exact self-similarity · q={q:g} · actual contained sheets through depth {depth}",
             color="#b2c6cd", fontsize=13)
    fig.text(.055, .065, "Every local neighbourhood contains planar disks in a dense set of orientations.\n"
             "At a dense set of centres, all sufficiently deep normalized views approach a full ball — despite zero volume.",
             color="#b2c6cd", fontsize=12)
    fig.subplots_adjust(left=.01, right=.99, bottom=.13, top=.85, wspace=-.2)
    path = Path(output) if output else HERE / f"membrane-q{str(q).replace('.', '')}.png"
    fig.savefig(path, dpi=130, facecolor=fig.get_facecolor())
    plt.close(fig)
    return str(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--q", type=float, default=.25)
    parser.add_argument("--depth", type=int, default=4)
    args = parser.parse_args()
    print(json.dumps(verify(), indent=2))
    if args.render:
        print(render(args.depth, args.q))
