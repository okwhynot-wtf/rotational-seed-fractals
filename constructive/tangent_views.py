"""Actual disks contained in progressively deeper origin blowups."""
import json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from membrane import maps,HERE
from render_membrane import Renderer

def rotations(depth):
    matrices,_=maps();q=matrices[4:]/.25
    all_rot=[np.eye(3)];front=all_rot
    for _ in range(depth):
        front=[a@b for a in front for b in q]
        all_rot.extend(front)
    return all_rot

def disk_geometry(depth):
    theta=np.linspace(0,2*np.pi,97)
    ring=np.c_[np.cos(theta),np.sin(theta),np.zeros_like(theta)]
    palette=np.array([[.31,.78,.76],[.88,.49,.29],[.69,.64,.83],[.89,.74,.43]])
    result=[]
    for j,r in enumerate(rotations(depth)):
        vertices=ring@r.T;normal=r[:,2]
        for k in range(len(ring)-1):
            for point in (np.zeros(3),vertices[k],vertices[k+1]):
                result.append(np.r_[point,normal,palette[j%4]])
    return np.array(result,dtype='f4')

def main():
    renderer=Renderer(1,.25,(840,840))
    canvas=Image.new('RGB',(3360,1120),'#08121b');draw=ImageDraw.Draw(canvas)
    title=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',50)
    body=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',28)
    draw.text((70,45),'ZERO VOLUME. FULL-BALL TANGENTS.',font=title,fill='#ecf3f4')
    for d in range(4):
        renderer.vao.release();renderer.buffer.release()
        renderer.buffer=renderer.ctx.buffer(disk_geometry(d).tobytes())
        renderer.vao=renderer.ctx.vertex_array(renderer.program,[(renderer.buffer,'3f 3f 3f','point','normal','color')])
        canvas.paste(renderer.image(27,-55,.86),(840*d,160))
        draw.text((840*d+65,135),f'Scale 4⁻{d} · {sum(4**i for i in range(d+1))} contained disks',font=body,fill='#b2c6cd')
    draw.text((70,1030),'Each image shows genuine subsets of (K / t) ∩ B(0,1). More disks reveal increasingly complete directional coverage.',font=body,fill='#b2c6cd')
    canvas.save(HERE/'membrane-tangent-progression.png');renderer.close()
    # Numerical diagnostics, not a rigorous spherical coverage certificate.
    n=12000
    k=np.arange(n);z=1-2*(k+.5)/n;phi=k*np.pi*(3-np.sqrt(5))
    probe=np.c_[np.sqrt(1-z*z)*np.cos(phi),np.sqrt(1-z*z)*np.sin(phi),z]
    rows=[]
    for depth in range(6):
        normals=np.array([r[:,2] for r in rotations(depth)])
        closest=np.ones(n)
        for chunk in np.array_split(normals, max(1,len(normals)//128)):
            closest=np.minimum(closest,np.abs(probe@chunk.T).min(axis=1))
        rows.append({'word_depth':depth,'number_of_disks':len(normals),
                     'sampled_max_distance_to_disks':float(closest.max()),
                     'scale_threshold':4.**(-depth)})
    report={'scope':'Diagnostic only: maximum over 12000 Fibonacci-sphere probes; not a rigorous uniform upper bound.',
            'rows':rows}
    (HERE/'direction_coverage.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
