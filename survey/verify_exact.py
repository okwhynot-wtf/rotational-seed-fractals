"""Exact scalar certificate for interval-backed rectangle IFS recipes.

Only rational arithmetic and integer root inequalities. Matrices have their
own floating implementation check in model.py; theorem arguments are in REPORT.
"""
from fractions import Fraction as F
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent

def power_upper(x,p,q,den=10**16):
    """Rational upper bound for x**(p/q), proved by integer inequalities."""
    target=x**p
    low,high=0,den
    while F(high,den)**q<target:high*=2
    while high-low>1:
        mid=(low+high)//2
        if F(mid,den)**q<target:low=mid
        else:high=mid
    bound=F(high,den)
    assert bound**q>=target
    assert low==0 or F(low,den)**q<target
    return bound

def certify(m,overlap,q=F(1,4),axis_subdivisions=2,dimension_bound=None):
    r2=F(1,12*m*m)
    rupper=F(289,1000*m)
    assert rupper*rupper>r2
    R=F(3) if m==1 else F(5,2)
    # Largest edge midpoint is on the short side nearest a corner.
    M2=4+(1-F(1,2*m))**2
    assert R-R*rupper>0 and (R-R*rupper)**2>M2
    # Axis translations have maximal norm sqrt(3)*(M-1)/M.
    M=axis_subdivisions
    assert (R-R/M)**2>3*F(M-1,M)**2
    # Bridge midpoints have squared norm <=3; the same bound encloses them.
    assert M2>=3
    volume_upper=F(1,M*M)+39*m*rupper**3+(4*q**3 if overlap else 0)
    assert volume_upper<1
    exponent=dimension_bound or {2:F(13,5) if overlap else F(5,2),3:F(12,5),4:F(23,10)}[m]
    p,n=exponent.numerator,exponent.denominator
    cover_upper=M*power_upper(F(1,M),p,n)+39*m*power_upper(r2,p,2*n)
    if overlap:cover_upper+=4*power_upper(q,p,n)
    assert cover_upper<1
    return {'subdivisions':m,'axis_subdivisions':M,'central_overlap':overlap,'central_scale':str(q),
            'invariant_radius':str(R),
            'edge_scale_squared':str(r2),'edge_scale_rational_upper':str(rupper),
            'largest_edge_midpoint_squared':str(M2),
            'volume_cover_rational_upper':str(volume_upper),
            'hausdorff_dimension_strict_upper':str(exponent),
            'dimension_cover_rational_upper':str(cover_upper),
            'all_scalar_inequalities':'passed using fractions.Fraction and integer root bounds'}

if __name__=='__main__':
    data=[certify(2,False),certify(2,True),certify(3,True),certify(4,True)]
    (ROOT/'exact_certificate.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
