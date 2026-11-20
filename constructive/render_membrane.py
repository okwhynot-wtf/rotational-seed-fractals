"""Depth-buffered rendering of genuine planar square subsets of K."""
import argparse
import math
from pathlib import Path
import numpy as np
import moderngl as gl
from PIL import Image, ImageDraw, ImageFont
from membrane import sheets, HERE

VERT = '''#version 330
in vec3 point; in vec3 normal; in vec3 color;
uniform mat3 camera; uniform float scale; uniform float aspect;
out vec3 vnormal; out vec3 vcolor;
void main(){vec3 p=camera*point;gl_Position=vec4(p.x*scale/aspect,p.y*scale,-p.z/5.,1.);vnormal=normal;vcolor=color;}
'''
FRAG = '''#version 330
in vec3 vnormal; in vec3 vcolor; out vec4 frag;
void main(){vec3 n=normalize(vnormal);float a=.48+.52*abs(dot(n,normalize(vec3(.3,-.4,.85))));frag=vec4(vcolor*a,1.);}
'''

def geometry(depth, q):
    palette=np.array([[.30,.70,.73],[.32,.49,.75],[.76,.60,.36],[.83,.45,.26],
                      [.90,.49,.28],[.30,.77,.72],[.68,.57,.83],[.85,.68,.32]])
    data=[]
    for verts,n,label in sheets(depth,q):
        normal=np.cross(verts[1]-verts[0],verts[2]-verts[0]);normal/=np.linalg.norm(normal)
        color=np.array([.16,.33,.43]) if n==0 else palette[label]
        for j in (0,1,2,0,2,3):data.append(np.r_[verts[j],normal,color])
    return np.array(data,dtype='f4')

def view(elev,azim):
    el,az=map(math.radians,(elev,azim))
    eye=np.array([math.cos(el)*math.cos(az),math.cos(el)*math.sin(az),math.sin(el)])
    right=np.cross([0,0,1],eye);right/=np.linalg.norm(right)
    up=np.cross(eye,right)
    return np.array([right,up,eye],dtype='f4')

class Renderer:
    def __init__(self, depth=4, q=.25, size=(1280,960)):
        self.size=size
        self.ctx=gl.create_standalone_context(require=330)
        self.program=self.ctx.program(vertex_shader=VERT,fragment_shader=FRAG)
        self.buffer=self.ctx.buffer(geometry(depth,q).tobytes())
        self.vao=self.ctx.vertex_array(self.program,[(self.buffer,'3f 3f 3f','point','normal','color')])
        self.frame=self.ctx.simple_framebuffer(size,components=3,samples=4)
        self.output=self.ctx.simple_framebuffer(size,components=3)
        self.ctx.enable(gl.DEPTH_TEST)
    def image(self,elev=28,azim=-55,scale=.68):
        self.frame.use();self.frame.clear(8/255,18/255,27/255,depth=1.)
        self.program['camera'].write(view(elev,azim).T.tobytes())
        self.program['scale'].value=scale
        self.program['aspect'].value=self.size[0]/self.size[1]
        self.vao.render(mode=gl.TRIANGLES)
        self.ctx.copy_framebuffer(self.output,self.frame)
        return Image.frombytes('RGB',self.size,self.output.read(components=3,alignment=1)).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    def close(self):
        for obj in (self.vao,self.buffer,self.frame,self.output,self.program):obj.release()
        self.ctx.release()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--q',type=float,default=.25);ap.add_argument('--depth',type=int,default=4)
    args=ap.parse_args()
    renderer=Renderer(args.depth,args.q,(1400,1100))
    out=Image.new('RGB',(2800,1500),'#08121b')
    out.paste(renderer.image(25,-55),(0,210));out.paste(renderer.image(60,-42),(1400,210))
    draw=ImageDraw.Draw(out)
    try:
        title=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',53)
        body=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',28)
    except OSError:title=body=ImageFont.load_default()
    draw.text((90,60),'MEMBRANE CONTINUUM',fill='#ecf3f4',font=title)
    draw.text((90,140),f'Fourfold self-similarity · q={args.q:g} · genuine contained squares through depth {args.depth}',fill='#b2c6cd',font=body)
    draw.text((90,1360),'Dense orientations of exact sheets; zero volume; full-ball tangents at a dense set of centres.',fill='#b2c6cd',font=body)
    path=HERE/f'membrane-depthbuffer-q{str(args.q).replace(".","")}.png';out.save(path);print(path)
    renderer.close()

if __name__=='__main__':main()
