"""C3-symmetric interval-backed Borromean similarity attractors.

Exact definition: rational vertices, square roots in orthonormal frames,
and angles specified by rational tan(theta/2). Decimal exports are previews.
No files outside this survey directory are written.
"""
from pathlib import Path
from fractions import Fraction
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parent
A = np.array([-1., -1., -1.])
B = -A
G = np.array([[0.,0.,1.],[1.,0.,0.],[0.,1.,0.]])

def rotate(axis, tangent):
    axis = np.asarray(axis, float)
    axis /= np.linalg.norm(axis)
    q = float(tangent)
    c, s = (1-q*q)/(1+q*q), 2*q/(1+q*q)
    x,y,z=axis
    cross=np.array([[0.,-z,y],[z,0.,-x],[-y,x,0.]])
    return c*np.eye(3)+(1-c)*np.outer(axis,axis)+s*cross

def frame(v):
    v=np.asarray(v,float); v=v/np.linalg.norm(v)
    helper=np.eye(3)[int(np.argmin(abs(v)))]
    w=np.cross(v,helper);w/=np.linalg.norm(w)
    return np.column_stack([v,w,np.cross(v,w)])

def edge_map(u,v,tangent):
    u,v=np.asarray(u,float),np.asarray(v,float)
    r=np.linalg.norm(v-u)/np.linalg.norm(B-A)
    Q=frame(v-u)@rotate([1,0,0],tangent)@frame(B-A).T
    return {'r':float(r),'R':Q.tolist(),'t':((u+v)/2).tolist()}

def export_map(r,Q,t,kind,orbit,edge=None):
    result={'r':float(r),'R':np.asarray(Q).tolist(),'t':np.asarray(t).tolist(),
            'kind':kind,'orbit':int(orbit)}
    if edge is not None: result['edge']=np.asarray(edge).tolist()
    return result

def base_edges(subdivisions=2):
    # Square-grid side length 1/subdivisions, starting at (-2,-1,0).
    corners=[(-2,-1,0),(2,-1,0),(2,1,0),(-2,1,0)]
    ring=[]
    for u,v in zip(corners,corners[1:]+corners[:1]):
        u,v=np.array(u,float),np.array(v,float)
        count=int(np.linalg.norm(v-u)*subdivisions)
        for j in range(count):ring.append([u+(v-u)*j/count,u+(v-u)*(j+1)/count])
    bridge=[]
    for j in range(subdivisions):
        bridge.append([B+np.array([0,0,-j/subdivisions]), B+np.array([0,0,-(j+1)/subdivisions])])
    return ring,bridge

def construct(subdivisions=2, edge_twist='1/2', axis_twist='1/3', overlap=False, central_scale='1/4', axis_subdivisions=2, invariant_radius=None):
    edge_twist=Fraction(edge_twist); axis_twist=Fraction(axis_twist)
    maps=[]
    axis=B/np.linalg.norm(B)
    assert isinstance(axis_subdivisions,int) and axis_subdivisions>=2
    for j in range(axis_subdivisions):
        offset=Fraction(2*j+1-axis_subdivisions,axis_subdivisions)
        roll=axis_twist*Fraction(2*j+1-axis_subdivisions,axis_subdivisions-1)
        maps.append(export_map(1/axis_subdivisions,rotate(axis,roll),float(offset)*B,'axis',3))
    ring,bridge=base_edges(subdivisions)
    for kind,edges in [('ring',ring),('bridge',bridge)]:
        for orbit in range(3):
            U=np.linalg.matrix_power(G,orbit)
            for edge in edges:
                m=edge_map(*edge,edge_twist)
                maps.append(export_map(m['r'],U@np.array(m['R'])@U.T,
                                       U@np.array(m['t']),kind,orbit,
                                       [U@edge[0],U@edge[1]]))
    if overlap:
        central_scale=Fraction(central_scale)
        assert 0<central_scale<1
        maps.append(export_map(central_scale,np.eye(3),np.zeros(3),'overlap',4))
        for i in range(3):
            maps.append(export_map(central_scale,rotate(np.eye(3)[i],Fraction(1,2)),np.zeros(3),'overlap',4))
    r=np.array([m['r'] for m in maps])
    lo,hi=0.,10.
    for _ in range(80):
        mid=(lo+hi)/2
        if np.sum(r**mid)>1:lo=mid
        else:hi=mid
    ident=f'borromean-m{subdivisions}-q{str(edge_twist).replace("/","_")}-a{str(axis_twist).replace("/","_")}'
    if overlap:ident+='-overlap'
    if overlap and central_scale!=Fraction(1,4):ident+='-c'+str(central_scale).replace('/','_')
    if axis_subdivisions!=2:ident+='-ax'+str(axis_subdivisions)
    if invariant_radius is None:invariant_radius=3.0 if subdivisions==1 else 2.5
    return {'id':ident,'name':'Borromean axis continuum'+(' with central rotation overlap' if overlap else ''),
            'definition':{'source_endpoints':[A.tolist(),B.tolist()],
                          'symmetry_generator':G.tolist(),'symmetry_order':3,
                          'subdivisions':subdivisions,'edge_twist_half_tangent':str(edge_twist),
                          'axis_twist_half_tangent':str(axis_twist),'central_overlap':bool(overlap),
                          'axis_subdivisions':axis_subdivisions,
                          'axis_half_tangent_rule':'q_j=axis_twist*(2*j+1-M)/(M-1), j=0,...,M-1',
                          'central_scale':str(central_scale) if overlap else None,
                          'rectangle_corners':[[-2,-1,0],[2,-1,0],[2,1,0],[-2,1,0]],
                          'bridge':[B.tolist(),[1,1,0]],
                          'exact_coefficients':'Rational vertices and half-angle tangents; positive square roots in frame(). Decimal matrices are exports.'},
            'maps':maps,'screen':{'similarity_dimension_upper_bound':(lo+hi)/2,
                                 'volume_cover_sum':float(np.sum(r**3)),
                                 'invariant_ball_radius':float(invariant_radius)}}

def checks(d):
    maps=d['maps'];R0=d['screen']['invariant_ball_radius']
    endpoint=0.;orth=0.;radius=-1e9;symmetry=0.;axis_interval=0.
    matrices=[]
    for m in maps:
        r,Q,t=m['r'],np.array(m['R']),np.array(m['t'])
        orth=max(orth,float(abs(Q@Q.T-np.eye(3)).max()))
        radius=max(radius,float(r*R0+np.linalg.norm(t)-R0))
        if 'edge' in m:
            endpoint=max(endpoint,float(abs(r*Q@A+t-np.array(m['edge'][0])).max()),
                         float(abs(r*Q@B+t-np.array(m['edge'][1])).max()))
        matrices.append(np.r_[r,Q.ravel(),t])
    matrices=np.array(matrices)
    M=d['definition'].get('axis_subdivisions',2)
    for j,m in enumerate([v for v in maps if v['kind']=='axis']):
        linear=m['r']*np.array(m['R']);t=np.array(m['t'])
        lo=(-1+2*j/M)*B;hi=(-1+2*(j+1)/M)*B
        axis_interval=max(axis_interval,float(abs(linear@A+t-lo).max()),float(abs(linear@B+t-hi).max()))
    for m in maps:
        Q,t=np.array(m['R']),np.array(m['t'])
        v=np.r_[m['r'],(G@Q@G.T).ravel(),G@t]
        symmetry=max(symmetry,float(abs(matrices-v).max(axis=1).min()))
    assert endpoint<1e-12 and orth<1e-12 and symmetry<1e-12 and axis_interval<1e-12 and radius<0
    return {'endpoint_max_error':endpoint,'orthogonality_max_error':orth,
            'C3_conjugacy_max_error':symmetry,'invariant_ball_slack':-radius,
            'axis_interval_cover_max_error':axis_interval,
            'three_volume_cover_sum':d['screen']['volume_cover_sum'],
            'checks_are':'floating-point implementation checks, not proof of topology or historical novelty'}

def sample(d,count=800000,seed=1783):
    maps=d['maps'];r=np.array([m['r'] for m in maps]);Q=np.array([m['R'] for m in maps]);t=np.array([m['t'] for m in maps])
    s=d['screen']['similarity_dimension_upper_bound'];prob=r**s;prob/=prob.sum()
    rng=np.random.default_rng(seed);batch=min(count,32768);x=np.zeros((batch,3));out=[];labels=[]
    for step in range(40+math.ceil(count/batch)):
        ids=rng.choice(len(r),size=batch,p=prob)
        x=np.einsum('nij,nj->ni',Q[ids],x)*r[ids,None]+t[ids]
        if step>=40:out.append(x.copy());labels.append(ids)
    return np.concatenate(out)[:count],np.concatenate(labels)[:count]

if __name__=='__main__':
    summary=[]
    for m,q,a,ov in [(2,'0','0',False),(2,'1/2','1/3',False),(2,'1','1/2',False),
                     (2,'1/2','1/3',True),(3,'1/2','1/3',True),(4,'1/2','1/3',True)]:
        d=construct(m,q,a,ov);d['checks']=checks(d)
        (ROOT/(d['id']+'.json')).write_text(json.dumps(d,indent=2)+'\n')
        summary.append({'id':d['id'],'map_count':len(d['maps']),**d['screen'],**d['checks']})
    (ROOT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
