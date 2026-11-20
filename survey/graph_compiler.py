"""Compile rational polygon graphs into connected similarity attractors.

Requirements: standard Python and numpy; verify_exact.py supplies integer-root
bounds. Exact definitions are rational vertices, radicals in frame construction,
and the specified finite-order rotation. Decimal matrices are numerical exports.

Planning proves a Hausdorff bound BEFORE allocating the map list. Astronomical
requests return a certificate/estimate with materialization disabled.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from fractions import Fraction as F
import json
import math
from pathlib import Path
import numpy as np
from verify_exact import power_upper

HERE=Path(__file__).resolve().parent

def rational(x):
    if isinstance(x,float):raise TypeError('Use integers or rational strings, not float coordinates.')
    return F(x)

def vector(v):
    if len(v)!=3:raise ValueError('Every vertex must have three coordinates.')
    return tuple(rational(x) for x in v)

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def enc(v):return [str(x) for x in v]
def edgekey(a,b):return tuple(sorted((a,b)))

def canonicalize(raw,axis):
    """Canonical unordered graph; add one axis attachment per component as needed."""
    original=[vector(v) for v in raw['vertices']]
    if not original:raise ValueError('The graph must contain at least one vertex.')
    edges=set()
    for pair in raw.get('edges',[]):
        if len(pair)!=2:raise ValueError('Each edge needs two vertex indices.')
        a,b=pair
        if not isinstance(a,int) or not isinstance(b,int) or not(0<=a<len(original) and 0<=b<len(original)):
            raise ValueError('Invalid edge indices.')
        if original[a]!=original[b]:edges.add(edgekey(original[a],original[b]))
    vertices=set(original);neighbours={v:set() for v in vertices}
    for a,b in edges:neighbours[a].add(b);neighbours[b].add(a)
    todo=set(vertices);components=[]
    while todo:
        seed=min(todo);stack=[seed];component=set()
        while stack:
            v=stack.pop()
            if v in component:continue
            component.add(v);stack.extend(neighbours[v]-component)
        todo-=component;components.append(component)
    axis2=dot(axis,axis);zero=(F(0),)*3;attachments=[]
    def on_interval(v):return cross(v,axis)==zero and abs(dot(v,axis))<=axis2
    for component in components:
        if any(on_interval(v) for v in component):continue
        nearest=min(component,key=lambda v:(dot(v,v),v))
        attachments.append(edgekey(zero,nearest));edges.add(edgekey(zero,nearest));vertices.add(zero)
    ordered=sorted(vertices);indices={v:i for i,v in enumerate(ordered)}
    exact_edges=sorted(edges)
    return {'name':str(raw.get('name','Polygon graph')),
            'vertices':[enc(v) for v in ordered],
            'edges':[[indices[a],indices[b]] for a,b in exact_edges],
            'attachments':[[indices[a],indices[b]] for a,b in attachments],
            'original_component_count':len(components),
            'attachment_rule':'Join each component not already meeting the source interval to0 at its smallest-norm vertex; ties lexicographic.',
            'connected_after_including_source_interval':True}

def log2_floor_fraction(x):
    if x<=0:raise ValueError('Positive value required.')
    n,d=x.numerator,x.denominator;k=n.bit_length()-d.bit_length()
    if k>=0:
        if n<(d<<k):k-=1
    elif (n<<(-k))<d:k-=1
    return k

def compact_integer(x):
    if x.bit_length()<333:return str(x)
    shift=max(0,x.bit_length()-53)
    digits=math.floor(math.log10(x>>shift)+shift*math.log10(2))+1
    return {'decimal_digits_approximately':digits,'binary_bits':x.bit_length()}

def plan(raw,epsilon='1/2',axis_endpoint=(2,2,2),axis_pieces=6,
         symmetry_order=1,central_scale=None,max_maps=50000):
    eps=rational(epsilon)
    if eps<=0:raise ValueError('epsilon must be positive.')
    # Also guarantee volume0 when a caller requests a weaker bound than3.
    eps=min(eps,F(3,2));s=1+eps
    if eps.denominator>1000:
        raise ValueError('Exact-root verification supports epsilon denominators<=1000; use a smaller-denominator sufficient bound.')
    B=vector(axis_endpoint)
    if dot(B,B)==0:raise ValueError('The source interval must be nondegenerate.')
    if not isinstance(axis_pieces,int) or axis_pieces<2:raise ValueError('axis_pieces must be an integer>=2.')
    if not isinstance(symmetry_order,int) or symmetry_order<1:raise ValueError('symmetry_order must be an integer>=1.')
    if not isinstance(max_maps,int) or max_maps<1:raise ValueError('max_maps must be a positive integer.')
    graph=canonicalize(raw,B);verts=list(map(vector,graph['vertices']))
    length2=[dot(sub(verts[b],verts[a]),sub(verts[b],verts[a])) for a,b in graph['edges']]
    denominator=4*dot(B,B);ratios2=[v/denominator for v in length2]
    M=axis_pieces;n=symmetry_order;kernel_count=3 if n==1 else n+1
    axis_upper=power_upper(F(1,M),eps.numerator,eps.denominator,den=10**20)
    if not axis_upper<1:raise ArithmeticError('Insufficient root-bound precision for the requested epsilon.')
    kernel_upper=lambda q:kernel_count*power_upper(q,s.numerator,s.denominator,den=10**20)
    if central_scale is None:
        q=F(1,4)
        while kernel_upper(q)>=(1-axis_upper)/4:q/=2
    else:q=rational(central_scale)
    if not 0<q<=F(1,2):raise ValueError('central_scale must be in(0,1/2].')
    central_upper=kernel_upper(q);budget=1-axis_upper-central_upper
    if budget<=0:raise ValueError('Axis and central maps already exhaust the dimension budget; reduce central_scale or increase axis_pieces.')
    counts=defaultdict(int)
    for x in ratios2:counts[x]+=1
    root_bounds=[];C=F(0)
    for x,multiplicity in sorted(counts.items()):
        upper=power_upper(x,s.numerator,2*s.denominator,den=10**20)
        root_bounds.append({'seed_ratio_squared':str(x),'multiplicity':multiplicity,
                            'power':str(s/2),'rational_upper':str(upper)})
        C+=n*multiplicity*upper
    k=0
    if C:
        # C*2^(-k epsilon)<budget iff 2^(k*p)>(C/budget)^q.
        rhs=(C/budget)**eps.denominator
        k=max(0,log2_floor_fraction(rhs)//eps.numerator+1)
        assert (rhs.denominator<<(k*eps.numerator))>rhs.numerator
    # Every graph-map ratio<=1/2 supplies a uniform invariant ball.
    maxratio=max(ratios2,default=F(0))
    while F(1<<(2*k),4)<maxratio:k+=1
    subdivisions=1<<k;edge_count=n*len(length2)*subdivisions
    map_count=M+kernel_count+edge_count
    maxnorm2=max([dot(B,B)]+[dot(v,v) for v in verts])
    T=power_upper(maxnorm2,1,2,den=10**12)
    radius=2*T
    materialize=map_count<=max_maps
    result={'schema':'polygon-graph-ifs-plan-v1','name':graph['name'],'canonical_graph':graph,
       'definition':{'axis_endpoint':enc(B),'axis_pieces':M,'symmetry_order':n,
           'symmetry_generator':'Right-handed rotation by2*pi/n about B; identity if n=1.',
           'central_scale':str(q),'kernel_count':kernel_count,
           'kernel_rotation_cos':'3/5','kernel_rotation_sin':'4/5',
           'kernel_axes':'n=1:global x,y. n>=2:orbit of a=B+(B cross e_j), where j minimizes |B_j|.',
           'edge_roll_half_tangent':'1/2','axis_roll_half_tangent':'0',
           'subdivision_power_of_two':k,'subdivisions_exact':f'2^{k}'},
       'certificate':{'epsilon_effective':str(eps),'hausdorff_strict_upper':str(s),
           'axis_cover_upper':str(axis_upper),'central_cover_upper':str(central_upper),
           'remaining_edge_budget':str(budget),'unsubdivided_edge_coefficient_upper':str(C),
           'edge_power_bounds':root_bounds,'subdivision_inequality':
           f'2^({k}*{eps.numerator}) > (C/budget)^{eps.denominator}' if C else 'No graph edges.',
           'largest_unsubdivided_ratio_squared':str(maxratio),
           'all_graph_ratios_at_most_half':True,'max_translation_norm_upper':str(T),
           'invariant_ball_radius':str(radius),'exact_arithmetic':'Fraction and integer-root bounds; no floating acceptance decisions.',
           'topological_dimension':1 if s<=2 else 'not established by this bound',
           'assouad_dimension':3,'ball_tangents':'Every normalized radius tends to the unit ball at each cylinder centre; analytic theorem in GRAPH_COMPILER.md.'},
       'allocation':{'seed_edges_with_attachments':len(length2),'symmetry_copies':n,
           'map_count_exact_expression':f'{n*len(length2)}*2^{k}+{M+kernel_count}',
           'map_count':compact_integer(map_count),'maximum_allowed_maps':max_maps,
           'materialization_allowed':materialize,'map_arrays_allocated_by_planning':False,
           'status':'ready' if materialize else 'estimate only: map count exceeds limit'}}
    return result

def rotation(axis,cosine,sine):
    a=np.asarray(axis,float);a=a/np.linalg.norm(a);x,y,z=a
    X=np.array([[0.,-z,y],[z,0.,-x],[-y,x,0.]])
    return cosine*np.eye(3)+(1-cosine)*np.outer(a,a)+sine*X

def frame(axis):
    a=np.asarray(axis,float);a=a/np.linalg.norm(a)
    helper=np.eye(3)[np.argmin(abs(a))];b=np.cross(a,helper);b/=np.linalg.norm(b)
    return np.column_stack((a,b,np.cross(a,b)))

def materialize(p):
    if not p['allocation']['materialization_allowed']:
        raise ValueError('Planning rejected materialization before allocating any map arrays: '+p['allocation']['map_count_exact_expression'])
    definition=p['definition'];graph=p['canonical_graph']
    B=vector(definition['axis_endpoint']);Bnum=np.array(B,float);D=2*np.linalg.norm(Bnum)
    n=definition['symmetry_order'];M=definition['axis_pieces'];m=1<<definition['subdivision_power_of_two']
    q=F(definition['central_scale']);Fsrc=frame(Bnum)
    G=np.eye(3) if n==1 else rotation(Bnum,math.cos(2*math.pi/n),math.sin(2*math.pi/n))
    powers=[np.linalg.matrix_power(G,j) for j in range(n)]
    maps=[];orth=0.;endpoint=0.;conjugacy=0.
    def add(r,Q,t,kind,orbit,exact):
        nonlocal orth
        orth=max(orth,float(abs(Q.T@Q-np.eye(3)).max()))
        maps.append({'r':float(r),'R':Q.tolist(),'t':np.asarray(t).tolist(),
                     'kind':kind,'orbit':orbit,'exact':exact})
    for j in range(M):
        offset=F(2*j+1-M,M)
        add(F(1,M),np.eye(3),float(offset)*Bnum,'axis',-1,{'offset':str(offset),'ratio':str(F(1,M))})
    verts=list(map(vector,graph['vertices']));roll=rotation([1,0,0],F(3,5),F(4,5))
    edge_start=len(maps)
    for orbit,U in enumerate(powers):
        for edge_index,(ia,ib) in enumerate(graph['edges']):
            a,b=verts[ia],verts[ib];delta=sub(b,a)
            Q=frame(np.array(delta,float))@roll@Fsrc.T
            r=math.sqrt(float(dot(delta,delta)))/(m*D)
            for j in range(m):
                u=tuple(a[i]+delta[i]*F(j,m) for i in range(3))
                v=tuple(a[i]+delta[i]*F(j+1,m) for i in range(3))
                t=U@np.array([(u[i]+v[i])/2 for i in range(3)],float)
                childQ=U@Q@U.T
                # B is fixed by U, so conjugation preserves source endpoints.
                endpoint=max(endpoint,float(abs(r*childQ@(-Bnum)+t-U@np.array(u,float)).max()),
                             float(abs(r*childQ@Bnum+t-U@np.array(v,float)).max()))
                add(r,childQ,t,'graph',orbit,{'seed_edge':edge_index,'piece':j,
                     'seed_piece_endpoints':[enc(u),enc(v)],'ratio_squared':str(dot(delta,delta)/(4*dot(B,B)*m*m))})
    add(q,np.eye(3),np.zeros(3),'central_identity',-1,{'ratio':str(q)})
    if n==1:
        central_axes=[np.array([1,0,0],float),np.array([0,1,0],float)]
        central_rotations=[rotation(v,F(3,5),F(4,5)) for v in central_axes]
    else:
        j=min(range(3),key=lambda i:abs(B[i]));helper=tuple(F(int(i==j)) for i in range(3))
        transverse=cross(B,helper);a=tuple(x+y for x,y in zip(B,transverse))
        seed=rotation(np.array(a,float),F(3,5),F(4,5))
        central_rotations=[U@seed@U.T for U in powers]
    for j,Q in enumerate(central_rotations):add(q,Q,np.zeros(3),'central_rotation',j,{'ratio':str(q),'rotation_cos':'3/5','rotation_sin':'4/5'})
    # Check the explicit conjugacy permutation without O(N^2) pair searches.
    if n>1:
        per_orbit=len(graph['edges'])*m
        for orbit in range(n):
            for j in range(per_orbit):
                a=maps[edge_start+orbit*per_orbit+j];b=maps[edge_start+((orbit+1)%n)*per_orbit+j]
                conjugacy=max(conjugacy,float(abs(G@np.array(a['R'])@G.T-np.array(b['R'])).max()),
                              float(abs(G@np.array(a['t'])-np.array(b['t'])).max()))
        for entry in maps[:M]:
            conjugacy=max(conjugacy,float(abs(G@np.array(entry['t'])-entry['t']).max()))
        for j,Q in enumerate(central_rotations):
            conjugacy=max(conjugacy,float(abs(G@Q@G.T-central_rotations[(j+1)%n]).max()))
    assert len(maps)==M+definition['kernel_count']+n*len(graph['edges'])*m
    assert max(orth,endpoint,conjugacy)<2e-11
    radius=float(F(p['certificate']['invariant_ball_radius']))
    worst=max(v['r']*radius+np.linalg.norm(v['t'])-radius for v in maps)
    assert worst<1e-10
    return {'schema':'polygon-graph-ifs-model-v1','name':p['name'],'plan':p,'maps':maps,
            'numerical_checks':{'endpoint_error':endpoint,'orthogonality_error':orth,
                'symmetry_conjugacy_error':conjugacy,'invariant_ball_excess':float(worst),
                'map_count':len(maps),'scope':'Implementation checks. Exact recipe and rational covering certificate are in plan.'}}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input',type=Path);ap.add_argument('--epsilon',default='1/2')
    ap.add_argument('--axis',nargs=3,default=['2','2','2']);ap.add_argument('--axis-pieces',type=int,default=6)
    ap.add_argument('--symmetry',type=int,default=1);ap.add_argument('--central-scale')
    ap.add_argument('--max-maps',type=int,default=50000);ap.add_argument('--plan-only',action='store_true')
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    raw=json.loads(args.input.read_text());p=plan(raw,args.epsilon,args.axis,args.axis_pieces,args.symmetry,args.central_scale,args.max_maps)
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'plan.json').write_text(json.dumps(p,indent=2)+'\n')
    if not args.plan_only and p['allocation']['materialization_allowed']:
        model=materialize(p);(args.output/'model.json').write_text(json.dumps(model,indent=2)+'\n')
        print(json.dumps(model['numerical_checks'],indent=2))
    print(json.dumps({'certificate':{k:p['certificate'][k] for k in ['hausdorff_strict_upper','topological_dimension','assouad_dimension']},'allocation':p['allocation']},indent=2))

if __name__=='__main__':main()
