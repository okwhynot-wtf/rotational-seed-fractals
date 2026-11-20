"""Embedded DAT module: deterministic finite-point exploration of three IFSs."""
import json
import math
from pathlib import Path
import numpy as np

PALETTE=np.array([[.22,.78,.78],[.94,.55,.28],[.66,.60,.94],[.51,.64,.70],[.90,.83,.65]],dtype=float)

def sample(recipe,count):
    r=np.array([m['r'] for m in recipe['maps']],float)
    Q=np.array([m['R'] for m in recipe['maps']],float)
    t=np.array([m['t'] for m in recipe['maps']],float)
    exponent=recipe['screen']['similarity_dimension_upper_bound']
    probs=r**exponent;probs/=probs.sum()
    rng=np.random.default_rng(20261120)
    x=np.zeros((count,3))
    for _ in range(max(32,math.ceil(math.log(1e-12)/math.log(float(max(r)))))):
        ids=rng.choice(len(r),count,p=probs)
        x=np.einsum('nij,nj->ni',Q[ids],x)*r[ids,None]+t[ids]
    groups=np.array([m['orbit'] for m in recipe['maps']])
    colors=PALETTE[groups[ids]]
    # A common fixed camera frame makes the threefold rotation axis face the viewer.
    eye=np.array([1.,1.,1.])/math.sqrt(3)
    right=np.array([-1.,1.,0.])/math.sqrt(2);up=np.cross(eye,right)
    basis=np.array([right,up,eye])
    span=max(float(np.ptp(x,axis=0).max()),1e-9)
    return (x@basis.T)*(2/span),colors

def rebuild():
    b=parent();recipes=json.loads(b.op('recipes').text)
    key=b.par.Candidate.eval();recipe=recipes[key]
    count=int(b.par.Pointcount);b.par.Status='Generating deterministic finite samples...'
    x,color=sample(recipe,count)
    b.store('point_data',(x,color))
    sop=b.op('geometry/points');sop.lock=False
    try:
        sop.cook(force=True)
        if sop.numPoints!=count:raise RuntimeError('Script SOP did not generate the requested points')
        sop.lock=True
    finally:
        b.unstore('point_data')
    b.par.Status='{} | {:,} finite points | not a solid mesh'.format(recipe['viewer_label'],count)
    b.op('render').cook(force=True)
    return {'candidate':key,'points':sop.numPoints,'source':'embedded exact-recipe numerical matrices',
            'seed':20261120,'finite_sample':True}

def open_studio():parent().op('studio_window').par.winopen.pulse()

def snapshot():
    b=parent();folder=Path(b.par.Outputfolder.eval())
    folder.mkdir(parents=True,exist_ok=True)
    path=folder/(b.par.Candidate.eval()+'-native-preview.png')
    b.op('render').save(path.as_posix());b.par.Status='Saved '+path.name
    return str(path)

def reset_view():
    b=parent();b.par.Yaw=0;b.par.Pitch=0;b.par.Zoom=1;b.par.Orbit=False
