"""Exact finite full-ball tangent bounds for the reference q=1/4 membrane.

NumPy only proposes a nearest-plane witness at each rational cube-face mesh
point. Every reported inequality is then verified with Python integers.
Use --verify to recheck saved witnesses without NumPy. All inequalities and
reported decimal upper enclosures use integer arithmetic, not floating point.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import isqrt
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
N = ((53, -60, 96), (60, -75, -80), (96, 80, -3))
Z = ((0, -1, 0), (1, 0, 0), (0, 0, 1))
I = ((1, 0, 0), (0, 1, 0), (0, 0, 1))


def transpose(a):
    return tuple(zip(*a))


def multiply(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3))
                       for j in range(3)) for i in range(3))


def mv(a, v):
    return tuple(sum(row[j] * v[j] for j in range(3)) for row in a)


def rotations():
    out = []
    z = I
    for _ in range(4):
        a = multiply(multiply(z, N), transpose(z))
        if multiply(transpose(a), a) != tuple(tuple(125**2 * I[i][j] for j in range(3)) for i in range(3)):
            raise ValueError('Nonorthogonal generator')
        out.append(a)
        z = multiply(Z, z)
    return out


def normals(depth):
    denominator = 125**depth
    frontier = [(0, 0, 1)]
    out = [(0, 0, denominator)]
    for level in range(1, depth+1):
        frontier = [mv(a, v) for a in rotations() for v in frontier]
        multiplier = 125**(depth-level)
        out.extend(tuple(multiplier*c for c in v) for v in frontier)
    if any(sum(c*c for c in v) != denominator**2 for v in out):
        raise ValueError('A normal is not exactly unit length')
    return out, denominator


def mesh_points(m):
    # The three negative faces follow by antipodal symmetry of |normal dot x|.
    for face in range(3):
        for i, j in product(range(m), repeat=2):
            v = [-m + 2*i + 1, -m + 2*j + 1]
            v.insert(face, m)
            yield tuple(v)


def fraction_data(value):
    scale = 10**12
    ceiling = (value.numerator*scale + value.denominator-1)//value.denominator
    return {'numerator': value.numerator, 'denominator': value.denominator,
            'decimal_upper': f'{ceiling//scale}.{ceiling%scale:012d}'}


def rational_sqrt_upper(value, denominator=10**12):
    # floor(sqrt(a/b)*D) is floor(sqrt(floor(a D²/b))). Add one for a strict bound.
    a, b = value.numerator, value.denominator
    p = isqrt(a * denominator**2 // b) + 1
    upper = Fraction(p, denominator)
    if upper**2 <= value:
        raise ValueError('Invalid square-root enclosure')
    return upper


def check_witnesses(depth, m, witnesses):
    ns, denominator = normals(depth)
    points = list(mesh_points(m))
    if len(witnesses) != len(points):
        raise ValueError('Incomplete sphere mesh witness list')
    maximum = Fraction(0)
    worst = None
    for point, index in zip(points, witnesses):
        if not isinstance(index, int) or not 0 <= index < len(ns):
            raise ValueError('Invalid normal index')
        dot = sum(a*b for a, b in zip(ns[index], point))
        squared = Fraction(dot**2, denominator**2 * sum(c*c for c in point))
        if squared > maximum:
            maximum, worst = squared, {'cube_point_numerator': point, 'normal_index': index}
    plane_bound = rational_sqrt_upper(maximum)
    mesh_bound = Fraction(3, 2*m)  # sqrt(2)/m < 3/(2m).
    epsilon = plane_bound + mesh_bound
    return dict(depth=depth, core_words_up_to_depth_including_empty=len(ns), cube_subdivisions=m,
                checked_points=len(points), full_sphere_mesh_points=2*len(points),
                scale_threshold=f'1/{4**depth}',
                largest_witness_distance_squared=fraction_data(maximum),
                mesh_plane_distance_upper=fraction_data(plane_bound),
                sphere_mesh_radius_upper=fraction_data(mesh_bound),
                full_ball_hausdorff_distance_upper=fraction_data(epsilon),
                worst_mesh_point=worst,
                integer_arithmetic_verification=True,
                scope='For every 0 < t <= 4^(-depth), at the origin of the original eight-map q=1/4 membrane.')


def generate(depth, m):
    import numpy as np
    started = time.time()
    ns, denominator = normals(depth)
    numeric = np.array(ns, dtype=float) / denominator
    points = list(mesh_points(m))
    witnesses = []
    for offset in range(0, len(points), 256):
        batch = np.array(points[offset:offset+256], dtype=float)
        scores = np.abs(batch @ numeric.T)
        witnesses.extend(np.argmin(scores, axis=1).tolist())
    result = check_witnesses(depth, m, witnesses)
    witness_path = HERE / f'witness-depth{depth}-mesh{m}.json'
    witness_path.write_text(json.dumps(dict(depth=depth, cube_subdivisions=m,
                                          normal_indices=witnesses), separators=(',', ':')) + '\n', newline='\n')
    result['witness_file'] = witness_path.name
    result['witness_sha256'] = hashlib.sha256(witness_path.read_bytes()).hexdigest()
    result['elapsed_seconds_diagnostic'] = round(time.time() - started, 3)
    print(json.dumps({k: result[k] for k in ['depth', 'checked_points', 'full_ball_hausdorff_distance_upper', 'elapsed_seconds_diagnostic']}), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--depths', nargs='+', type=int, default=[3, 4, 5, 6, 7])
    parser.add_argument('--mesh', type=int, default=200)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    if args.verify:
        report = json.loads((HERE/'certificate.json').read_text())
        for previous in report['bounds']:
            path = HERE / previous['witness_file']
            if hashlib.sha256(path.read_bytes()).hexdigest() != previous['witness_sha256']:
                raise ValueError('Witness hash mismatch')
            data = json.loads(path.read_text())
            actual = check_witnesses(data['depth'], data['cube_subdivisions'], data['normal_indices'])
            for key, value in actual.items():
                # Tuples become lists after JSON serialization.
                if json.loads(json.dumps(value)) != previous[key]:
                    raise ValueError(f'Certificate mismatch: {key}')
        print(f"Verified {len(report['bounds'])} complete-sphere bounds using integer arithmetic only.")
    else:
        if not 1 <= args.mesh <= 1000 or any(not 1 <= n <= 8 for n in args.depths):
            raise ValueError('Outside the deliberately bounded study range')
        report = dict(status='passed', construction='Original denominator-125 membrane, q=1/4',
                      method='Antipodal rational cube-face mesh; floating proposal, exact integer witness verification.',
                      bounds=[generate(n, args.mesh) for n in args.depths])
        (HERE/'certificate.json').write_text(json.dumps(report, indent=2)+'\n', newline='\n')


if __name__ == '__main__':
    main()
