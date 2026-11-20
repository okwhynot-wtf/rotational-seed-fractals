"""Exact duplicate words and rational brackets for improved covering bounds."""
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
from itertools import product
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from export_exact import I,Z,Q,mul,transpose,scale,recipe
from find_relations import primitive_pair,base_word,compose

HERE=Path(__file__).resolve().parent
Q13=tuple(tuple(F(x,13) for x in row) for row in ((-3,4,12),(12,-3,4),(4,12,-3)))

def maps_for(rotation):
    maps=recipe(F(1,4))[:4];z=I
    for k in range(4):
        r=mul(mul(z,rotation),transpose(z));z=mul(Z,z)
        maps.append((scale(r,F(1,4)),(F(0),)*3,F(1,4),'core',(F(0),)*3))
    return maps

def relation_family(rotation,core_pattern):
    maps=maps_for(rotation);n=len(core_pattern);relations=[]
    for orbit in range(4):
        h=[4+(j+orbit)%4 for j in core_pattern]
        rot=I
        for j in h:rot=mul(rot,scale(maps[j][0],F(4)))
        pair=primitive_pair(rot)
        assert pair is not None
        w,v=pair
        for sign in (-1,1):
            ww=tuple(sign*x for x in w);vv=tuple(sign*x for x in v)
            for tiny in product((-1,1),repeat=2):
                large=tuple(tiny[j]+2**(1+2*n)*ww[j] for j in range(2))
                d=1
                while max(abs(x) for x in vv[:2])>=2**d or max(abs(x) for x in large)>=2**(d+1):d+=1
                left=h+base_word(large,d+1)
                right=base_word(vv[:2],d)+h+base_word(tiny,1)
                assert left>right  # lexicographically decreasing rewriting
                assert compose(left,maps)==compose(right,maps)
                relations.append(dict(left=left,right=right,W=ww,V=vv,outer_length=d,
                                      long_inner_numerators=large,short_inner_numerators=tiny))
    forbidden=[tuple(r['left']) for r in relations]
    assert len(set(forbidden))==32
    lengths={len(x) for x in forbidden};assert len(lengths)==1
    length=lengths.pop()
    powers={sum(1 if j<4 else 2 for j in x) for x in forbidden};assert len(powers)==1
    power=powers.pop()
    assert not set(forbidden)&{tuple(r['right']) for r in relations}
    # No forbidden word overlaps any other at a proper prefix/suffix.
    for a in forbidden:
        for b in forbidden:
            for j in range(1,length):assert a[-j:]!=b[:j]
    return relations,length,power

def polynomial(y,p):return 4*y+4*y*y-32*y**p-1

def log_bounds(x,terms=64):
    """Rational bounds for log(x), x>=1, using its atanh series."""
    assert x>=1
    z=(x-1)/(x+1);value=F(0);power=z
    for k in range(terms):
        value+=2*power/F(2*k+1);power*=z*z
    return value,value+2*power/(F(2*terms+1)*(1-z*z))

def root_bracket(p,length):
    lo,hi=F(207,1000),F(21,100)
    assert polynomial(lo,p)<0<polynomial(hi,p)
    # Derivative is positive throughout this bracket; all checks are rational.
    assert 4+8*lo-32*p*hi**(p-1)>0
    for _ in range(220):
        mid=(lo+hi)/2
        if polynomial(mid,p)<0:lo=mid
        else:hi=mid
    assert (length-1)*32*hi**p<1
    lower_log2,upper_log2=log_bounds(F(2))
    lower_dimension=log_bounds(1/hi)[0]/upper_log2
    upper_dimension=log_bounds(1/lo)[1]/lower_log2
    precision=10**15
    lower_digits=(lower_dimension*precision).numerator//(lower_dimension*precision).denominator
    v=upper_dimension*precision
    upper_digits=-((-v.numerator)//v.denominator)
    assert F(lower_digits,precision)<lower_dimension<upper_dimension<F(upper_digits,precision)
    with localcontext() as ctx:
        ctx.prec=65
        y=(D(lo.numerator)/D(lo.denominator)+D(hi.numerator)/D(hi.denominator))/2
        s=-y.ln()/D(2).ln()
        old=1+(1+D(2).sqrt()).ln()/D(2).ln()
        decimal_upper=(s*D(10)**12).to_integral_value(rounding='ROUND_CEILING')/D(10)**12
        # Decimal diagnostics are distinguished from the exact defining bracket.
        return dict(y_rational_lower=str(lo),y_rational_upper=str(hi),
                    polynomial=f'4*y+4*y^2-32*y^{p}-1',
                    unique_root_interval=['207/1000','21/100'],
                    dimension_expression='-log_2(y), where y is the bracketed root',
                    dimension_diagnostic=str(s),rounded_up_12_places=str(decimal_upper),
                    certified_dimension_lower_15_places=str(D(lower_digits)/D(precision)),
                    certified_dimension_upper_15_places=str(D(upper_digits)/D(precision)),
                    logarithm_certificate='64-term rational atanh series with explicit geometric tail bound',
                    improvement_diagnostic=str(old-s),
                    recurrence_stability_check='(L-1)*32*y^p<1 verified at rational upper endpoint')

def main():
    result=[]
    for name,rotation,pattern in [('original125',Q,[0,3]),('norm13',Q13,[0])]:
        rels,length,power=relation_family(rotation,pattern)
        data=dict(model=name,rotation=[[str(x) for x in row] for row in rotation],
                  coefficient_definition='q=1/4; other matrices as in parent membrane model',
                  forbidden_count=32,word_length=length,contraction_power_of_two=power,
                  exact_affine_equalities_checked=32,
                  proper_prefix_suffix_overlap=False,relations=rels,
                  improved_bound=root_bracket(power,length))
        (HERE/f'{name}_certificate.json').write_text(json.dumps(data,indent=2)+'\n')
        result.append({key:data[key] for key in ['model','word_length','contraction_power_of_two','improved_bound']})
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
