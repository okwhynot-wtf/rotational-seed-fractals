"""Anchored-wing extension of the membrane family. Separate from base example."""
import argparse
import itertools
import json
import math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from membrane import maps as base_maps,HERE,Z,N
from render_membrane import Renderer

def rodrigues(axis,c,s):
    a=np.array(axis,float);a/=np.linalg.norm(a)
    x,y,z=a;cross=np.array([[0,-z,y],[z,0,-x],[-y,x,0]])
    return c*np.eye(3)+(1-c)*np.outer(a,a)+s*cross

def maps(q=.1,r=.45,kind='slant',anchor='corner'):
    a,t=base_maps(q);a=list(a);t=list(t)
    if kind=='slant':q0=N/125
    elif kind=='radial':q0=rodrigues([1,1,0],0,1)
    elif kind=='tangent':q0=rodrigues([-1,1,0],0,1)
    elif kind=='sweep':q0=rodrigues([3,4,0],-3/5,4/5)
    else:raise ValueError(kind)
    p0=np.array([1,1,0] if anchor=='corner' else [1,0,0],float)
    for k in range(4):
        z=np.linalg.matrix_power(Z,k);qk=z@q0@z.T;p=z@p0
        a.append(r*qk);t.append(p-r*qk@p)
    return np.array(a),np.array(t)

def dimension(q,r):
    lo,hi=2.,3.
    assert .5+4*q**3+4*r**3<1
    for _ in range(80):
        m=(lo+hi)/2
        if 4*.5**m+4*q**m+4*r**m>1:lo=m
        else:hi=m
    return (lo+hi)/2

def panels(q,r,kind,anchor,depth):
    a,t=maps(q,r,kind,anchor)
    s=np.array([[-1,-1,0],[1,-1,0],[1,1,0],[-1,1,0]],float)
    result=[(s,-1)]
    front=[(np.eye(3),np.zeros(3),-1)]
    for n in range(depth):
        nxt=[]
        for mat,shift,first in front:
            for j in range(12):
                m,b=mat@a[j],mat@t[j]+shift;label=j if first<0 else first
                if j>=4:result.append((s@m.T+b,label))
                if n<depth-1:nxt.append((m,b,label))
        front=nxt
    return result

def geometry(q,r,kind,anchor,depth):
    palette=np.array([[.28,.58,.63],[.48,.62,.76],[.76,.60,.40],[.77,.45,.30],
                      [.77,.52,.34],[.29,.66,.63],[.56,.50,.69],[.77,.64,.38],
                      [.84,.51,.30],[.35,.73,.70],[.59,.65,.77],[.84,.67,.44]])
    result=[]
    for vertices,label in panels(q,r,kind,anchor,depth):
        normal=np.cross(vertices[1]-vertices[0],vertices[2]-vertices[0]);normal/=np.linalg.norm(normal)
        color=np.array([.23,.35,.42]) if label<0 else palette[label]
        for j in (0,1,2,0,2,3):result.append(np.r_[vertices[j],normal,color])
    return np.array(result,dtype='f4')

def load_geometry(renderer,data):
    renderer.vao.release();renderer.buffer.release()
    renderer.buffer=renderer.ctx.buffer(data.tobytes())
    renderer.vao=renderer.ctx.vertex_array(renderer.program,[(renderer.buffer,'3f 3f 3f','point','normal','color')])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--depth',type=int,default=4);args=ap.parse_args()
    q=.1
    recipes=[('slant','corner',.35),('slant','corner',.45),('slant','corner',.49),
             ('radial','corner',.35),('radial','corner',.45),('radial','corner',.49),
             ('tangent','corner',.45),('sweep','corner',.45),('sweep','edge',.49)]
    renderer=Renderer(1,q,(1050,850))
    canvas=Image.new('RGB',(3150,2880),'#08121b');draw=ImageDraw.Draw(canvas)
    title=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',49)
    label=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',27)
    draw.text((70,40),'ANCHORED MEMBRANES · SCULPTURE SURVEY',font=title,fill='#ecf3f4')
    rows=[]
    for j,(kind,anchor,r) in enumerate(recipes):
        data=geometry(q,r,kind,anchor,args.depth);load_geometry(renderer,data)
        elev=-18 if kind in ('slant','tangent') else 23
        image=renderer.image(elev,-55,.48)
        col,row=j%3,j//3
        canvas.paste(image,(col*1050,160+row*900))
        text=f'{kind} · {anchor} · r={r:g} · dim H ≤ {dimension(q,r):.4f}'
        draw.text((col*1050+60,155+row*900),text,font=label,fill='#bed0d5')
        image.save(HERE/f'corona-{kind}-{anchor}-r{str(r).replace(".","")}.png')
        a,t=maps(q,r,kind,anchor)
        # Numerical supplementary checks; formulas are the exact definition.
        for k in range(4):
            p=np.linalg.matrix_power(Z,k)@np.array([1,1,0] if anchor=='corner' else [1,0,0])
            assert np.linalg.norm(a[8+k]@p+t[8+k]-p)<1e-14
        assert all(any(np.max(np.abs(Z@x@Z.T-y))<1e-14 and np.linalg.norm(Z@u-v)<1e-14
                       for y,v in zip(a,t)) for x,u in zip(a,t))
        rows.append(dict(kind=kind,anchor=anchor,q=q,r=r,hausdorff_upper=dimension(q,r),
                         cubed_ratio_sum=.5+4*q**3+4*r**3,depth=args.depth,
                         rendered_triangles=len(data)//3))
    canvas.save(HERE/'corona-survey.png');renderer.close()
    (HERE/'corona-recipes.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps(rows,indent=2))

if __name__=='__main__':main()
