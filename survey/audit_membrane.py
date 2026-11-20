"""Independent exact matrix audit of the sibling membrane construction."""
from fractions import Fraction as F
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
N=[[53,-60,96],[60,-75,-80],[96,80,-3]]
Z=[[0,-1,0],[1,0,0],[0,0,1]]
def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def transpose(a):return [list(x) for x in zip(*a)]
def determinant(a):return sum(a[0][i]*(a[1][(i+1)%3]*a[2][(i+2)%3]-a[1][(i+2)%3]*a[2][(i+1)%3]) for i in range(3))
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]

assert mul(transpose(N),N)==[[125**2*int(i==j) for j in range(3)] for i in range(3)]
assert determinant(N)==125**3
assert [sum(N[i][j]*[4,0,3][j] for j in range(3)) for i in range(3)]==[500,0,375]
assert sum(N[i][i] for i in range(3))==-25
assert cross([4,0,3],[0,4,3])==[-12,-12,16]
assert 4*F(1,2)**3+4*F(1,4)**3==F(9,16)<1
report={'subject':'../constructive/MEMBRANE.md and stated Q matrix',
        'independent_integer_checks':{'orthogonal_scaled_matrix':True,'proper_determinant':True,
                                      'axis_fixed':True,'trace_cosine':True,'two_axis_cross':[-12,-12,16],
                                      'volume_sum':'9/16'},
        'analytic_review':'No defect found in retained-square, connectedness, symmetry, topological dimension 2, dense-rotation, every-scale ball tangent, Assouad dimension 3, or OSC-obstruction arguments.',
        'simplification':'Use axes a=(4,0,3)/5 and Z a=(0,4,3)/5 directly for the two dense circle groups; no Q1 a computation needed.',
        'scope':'Independent within-agent-team check, not external peer review or formal proof.'}
(ROOT/'membrane_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
