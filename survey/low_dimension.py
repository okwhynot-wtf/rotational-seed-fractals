"""Topological dimension one linked member and matched unlinked-skeleton control."""
from copy import deepcopy
from fractions import Fraction as F
import json
import numpy as np
from model import ROOT,construct,checks,G
from verify_exact import certify

d=construct(6,overlap=True,central_scale='1/8',axis_subdivisions=6)
d['checks']=checks(d)
d['claims']={'topological_dimension':1,'reason':'Contains a nondegenerate interval, and dim_H<23/12<2.',
             'hausdorff_strict_upper':'23/12','assouad_dimension':3,
             'retained_triple':'Borromean rectangles; see independent root link certificate.'}
(ROOT/(d['id']+'.json')).write_text(json.dumps(d,indent=2)+'\n')
c=deepcopy(d);c['id']+='-unlink-control';c['name']='C3 unlinked-skeleton control'
R=np.array([[0.,-1.,0.],[1.,0.,0.],[0.,0.,1.]])
shift=np.array([2.,0.,0.])
for entry in c['maps']:
    if entry['kind']!='ring':continue
    U=np.linalg.matrix_power(G,entry['orbit']);V=U@R@U.T;v=U@shift
    entry['R']=(V@np.array(entry['R'])).tolist()
    entry['t']=(V@np.array(entry['t'])+v).tolist()
    entry['edge']=[(V@np.array(p)+v).tolist() for p in entry['edge']]
c['definition']['rectangle_corners']=[[3,-2,0],[3,2,0],[1,2,0],[1,-2,0]]
c['definition']['control_transform']='Rotate seed ring90 degrees about(1,1,0), leave bridge fixed; repeat under G.'
c['screen']['invariant_ball_radius']=4.0
c['checks']=checks(c)
c['claims']['retained_triple']='Three unlinked rectangles with pairwise disjoint spanning disks.'
c['claims']['scope']='Only the designated triple is proved unlinked; other links in the whole attractor are not excluded.'
(ROOT/(c['id']+'.json')).write_text(json.dumps(c,indent=2)+'\n')
assert [m['r'] for m in c['maps']]==[m['r'] for m in d['maps']]
summary=[{'id':v['id'],'map_count':len(v['maps']),**v['screen'],**v['checks']} for v in [d,c]]
(ROOT/'low-dimension-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
certificate=certify(6,True,F(1,8),6,F(23,12))
# Control midpoint norm squared <=3^2+2^2=13. R=4 and r<289/6000.
assert (F(4)*(1-F(289,6000)))**2>13
certificate['unlinked_control']={'same_contraction_ratios':True,'invariant_radius':'4',
   'ring_translation_norm_squared_upper':'13','spanning_disks':[
   '[1,3]x[-2,2]x{0}','{0}x[1,3]x[-2,2]','[-2,2]x{0}x[1,3]'],
   'unlink_proof':'Each pair of these spanning disks is disjoint: the fixed0 coordinate of one lies outside the other positive[1,3] interval.'}
certificate['topological_dimension']=1
certificate['topological_dimension_reason']='1<=dim_top K<=dim_H K<23/12<2 and topological dimension is integer-valued.'
(ROOT/'low-dimension-exact-certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
print(json.dumps(summary,indent=2))
