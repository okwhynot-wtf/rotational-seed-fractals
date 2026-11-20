"""Independent rational audit of saved graph-compiler planning certificates."""
from fractions import Fraction as F
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def vec(v):return tuple(map(F,v))
def verify(path):
    p=json.loads(path.read_text());c=p['certificate'];d=p['definition'];g=p['canonical_graph']
    eps=F(c['epsilon_effective']);s=F(c['hausdorff_strict_upper']);assert s==1+eps and 0<eps<=F(3,2)
    M=d['axis_pieces'];n=d['symmetry_order'];q=F(d['central_scale']);k=d['subdivision_power_of_two']
    assert M>=2 and n>=1 and 0<q<=F(1,2) and k>=0
    N=3 if n==1 else n+1;assert d['kernel_count']==N
    a=F(c['axis_cover_upper']);b=F(c['central_cover_upper']);budget=F(c['remaining_edge_budget'])
    assert a**eps.denominator>=F(1,M)**eps.numerator
    assert (b/N)**s.denominator>=q**s.numerator
    assert budget==1-a-b and budget>0
    B=vec(d['axis_endpoint']);D2=4*dot(B,B);vertices=list(map(vec,g['vertices']));counts={}
    for i,j in g['edges']:
        delta=tuple(y-x for x,y in zip(vertices[i],vertices[j]));x=dot(delta,delta)/D2
        assert x>0;counts[x]=counts.get(x,0)+1
    coefficients=F(0)
    assert len(counts)==len(c['edge_power_bounds'])
    for record in c['edge_power_bounds']:
        x=F(record['seed_ratio_squared']);multiplicity=record['multiplicity'];u=F(record['rational_upper'])
        assert counts[x]==multiplicity
        assert u**(2*s.denominator)>=x**s.numerator
        coefficients+=n*multiplicity*u
    assert coefficients==F(c['unsubdivided_edge_coefficient_upper'])
    assert (1<<(k*eps.numerator))*budget**eps.denominator>coefficients**eps.denominator
    assert max(counts,default=F(0))<=F(1<<(2*k),4)
    T=F(c['max_translation_norm_upper']);R=F(c['invariant_ball_radius'])
    assert T*T>=max([dot(B,B)]+[dot(v,v) for v in vertices]) and R==2*T
    expected=M+N+n*len(g['edges'])*(1<<k)
    assert p['allocation']['materialization_allowed']==(expected<=p['allocation']['maximum_allowed_maps'])
    return {'plan':str(path.relative_to(HERE)),'rational_certificate':'passed',
            'hausdorff_strict_upper':str(s),'subdivision_exponent':k,
            'map_count_expression':p['allocation']['map_count_exact_expression'],
            'materialization_allowed':p['allocation']['materialization_allowed']}

if __name__=='__main__':
    reports=[verify(HERE/name/'plan.json') for name in ['compiler-demo-one','compiler-demo-half','compiler-demo-estimate']]
    # Confirm the code's allocation guard is reached before the map list is built.
    from graph_compiler import materialize,plan
    huge=json.loads((HERE/'compiler-demo-estimate'/'plan.json').read_text())
    try:materialize(huge)
    except ValueError as error:assert 'before allocating' in str(error)
    else:raise AssertionError('Astronomical plan was not rejected')
    # Rational canonicalization handles duplicates, reverse edges, and isolated components.
    test={'vertices':[[1,0,0],[2,0,0],[1,0,0],[0,2,0]],'edges':[[0,1],[1,2]]}
    p=plan(test,'1',axis_endpoint=(0,0,1))
    assert p['canonical_graph']['original_component_count']==2
    assert len(p['canonical_graph']['attachments'])==2
    assert len(p['canonical_graph']['edges'])==3
    result={'plans':reports,'allocation_guard':'passed before array construction',
            'canonical_graph_case':'duplicate vertices/reversed edge merged; isolated component attached',
            'scope':'Exact scalar certificate audit plus meaningful planner checks; topology theorem reviewed separately.'}
    (HERE/'compiler-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
