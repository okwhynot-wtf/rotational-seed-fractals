"""Finite-resolution surface envelope of a sampled similarity attractor.

All point geometry comes from the candidate maps. The displayed skin is an
explicit visualization parameter, never a claim of positive mathematical volume.
"""
from pathlib import Path
import sys,json,math,time,argparse
import numpy as np
from scipy.ndimage import distance_transform_edt,gaussian_filter
from PIL import Image
import moderngl as gl

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'survey'))
from model import sample

VERT='''#version 430
out vec2 uv;
void main(){vec2 b=vec2((gl_VertexID<<1)&2,gl_VertexID&2);gl_Position=vec4(b*2.-1.,0.,1.);uv=b;}
'''
FRAG='''#version 430
in vec2 uv;out vec4 frag;
uniform sampler3D fieldTex,colourTex;
uniform vec3 right,up,eye,centre;
uniform float aspect,frame,extent,spacing,skin,exposure;
float dist(vec3 p){vec3 c=clamp(p,vec3(-extent),vec3(extent));
 return texture(fieldTex,c/(2.*extent)+.5).r+length(p-c)-skin;}
vec3 normal(vec3 p){float e=spacing*.85;return normalize(vec3(
 dist(p+vec3(e,0,0))-dist(p-vec3(e,0,0)),
 dist(p+vec3(0,e,0))-dist(p-vec3(0,e,0)),
 dist(p+vec3(0,0,e))-dist(p-vec3(0,0,e))));}
float shade(vec3 p,vec3 light){float t=spacing*3.,s=1.;
 for(int i=0;i<70;++i){float d=dist(p+t*light);s=min(s,10.*d/t);if(d<spacing*.15)return .14;
 t+=max(spacing*.7,d*.75);if(t>5.)break;}return .14+.86*clamp(s,0.,1.);}
void main(){vec2 xy=(uv-.5)*vec2(aspect,1.);vec3 origin=centre+frame*(xy.x*right+xy.y*up)+8.*eye;vec3 ray=-eye;
 vec3 background=mix(vec3(.008,.014,.022),vec3(.027,.048,.064),exp(-3.*dot(xy,xy)));
 float closest=dot(-origin,ray);float ds=closest*closest-dot(origin,origin)+extent*extent;
 if(ds<0.){frag=vec4(background,1);return;}float t=max(0.,closest-sqrt(ds));float end=closest+sqrt(ds);bool hit=false;
 for(int i=0;i<440;++i){vec3 p=origin+t*ray;float d=dist(p);if(d<spacing*.12){hit=true;break;}
 t+=max(spacing*.12,d*.65);if(t>end)break;}
 if(!hit){frag=vec4(background,1);return;}
 vec3 p=origin+t*ray;vec3 n=normal(p);
 vec3 key=normalize(-.6*right+.9*up+.65*eye),fill=normalize(.9*right+.4*up+.2*eye);
 vec3 c=texture(colourTex,p/(2.*extent)+.5).rgb;
 float ao=0.;for(int i=1;i<=5;i++){float s=float(i)*.07;ao+=max(0.,s-dist(p+n*s))*.7;}
 ao=exp(-ao*2.5);float shadow=shade(p+n*spacing*2.,key);
 float diffuse=max(0.,dot(n,key));float spec=pow(max(0.,dot(n,normalize(key+eye))),30.);
 float rim=pow(1.-max(0.,dot(n,eye)),2.4);
 vec3 col=c*(.14+shadow*diffuse*1.5)*vec3(1.07,.94,.81)*ao;
 col+=c*.3*max(0.,dot(n,fill))*vec3(.35,.76,1.);
 col+=mix(vec3(.7,.75,.8),c,.6)*spec*.9*shadow*ao;
 col+=vec3(.09,.21,.29)*rim*ao;
 col=pow(1.-exp(-exposure*col),vec3(1./2.2));frag=vec4(col,1.);}
'''

def build(d,n=256,count=8000000):
    cache=ROOT/'rendering'/(d['id']+f'-field{n}.npz')
    if cache.exists():return np.load(cache)
    start=time.time();extent=max(2.6,float(d['screen']['invariant_ball_radius'])+.1);spacing=2*extent/(n-1)
    points,labels=sample(d,count=count)
    ijk=np.rint((points+extent)/spacing).astype(np.int32)
    if ijk.min()<0 or ijk.max()>=n:raise ValueError('Out of volume')
    occupied=np.zeros((n,n,n),dtype=bool);labelgrid=np.zeros((n,n,n),dtype=np.uint8)
    occupied[ijk[:,2],ijk[:,1],ijk[:,0]]=True
    palette=np.array([[.80,.32,.09],[.025,.46,.43],[.43,.39,.64],[.16,.26,.32],[.30,.36,.39]],dtype='f4')
    groups=np.array([m['orbit'] for m in d['maps']],dtype=np.uint8)
    labelgrid[ijk[:,2],ijk[:,1],ijk[:,0]]=groups[labels]
    del points,labels,ijk
    print('Computing distance field',flush=True)
    distance,indices=distance_transform_edt(~occupied,return_indices=True)
    colour=palette[labelgrid[tuple(indices)]]
    del indices,labelgrid,occupied
    colour=np.stack([gaussian_filter(colour[...,i],.7) for i in range(3)],axis=-1)
    distance=(distance*spacing).astype('f4')
    np.savez_compressed(cache,distance=distance,colour=(colour*255).astype('u1'),extent=extent,spacing=spacing,
                        points=count,seed=1783)
    print('Field completed',round(time.time()-start,2),flush=True)
    return np.load(cache)

class Renderer:
    def __init__(self,data,size=(1280,960)):
        self.size=size;self.ctx=ctx=gl.create_standalone_context(require=430)
        self.program=ctx.program(vertex_shader=VERT,fragment_shader=FRAG)
        n=data['distance'].shape[0]
        self.field=ctx.texture3d((n,n,n),1,data['distance'].astype('f4').tobytes(),dtype='f4')
        self.colour=ctx.texture3d((n,n,n),3,data['colour'].tobytes())
        for i,tex in enumerate([self.field,self.colour]):
            tex.filter=(gl.LINEAR,gl.LINEAR);tex.repeat_x=tex.repeat_y=tex.repeat_z=False;tex.use(i)
        p=self.program;p['fieldTex'].value=0;p['colourTex'].value=1
        p['aspect'].value=size[0]/size[1];p['extent'].value=float(data['extent']);p['spacing'].value=float(data['spacing'])
        p['skin'].value=float(data['spacing'])*.85;p['exposure'].value=1.3
        self.frame=ctx.simple_framebuffer(size,components=3);self.vao=ctx.vertex_array(p,[])
    def image(self,az=-48,elev=27,frame=5.8,centre=(0,0,0)):
        az,el=map(math.radians,(az,elev));eye=np.array([math.cos(az)*math.cos(el),math.sin(az)*math.cos(el),math.sin(el)])
        right=np.array([-math.sin(az),math.cos(az),0]);up=np.cross(eye,right)
        for name,val in [('right',right),('up',up),('eye',eye),('centre',centre)]:self.program[name].value=tuple(val)
        self.program['frame'].value=frame;self.frame.use();self.vao.render(vertices=3)
        return Image.frombytes('RGB',self.size,self.frame.read(components=3,alignment=1)).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    def close(self):
        for o in [self.vao,self.frame,self.field,self.colour,self.program]:o.release()
        self.ctx.release()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--id',default='borromean-m3-q1_2-a1_3-overlap');ap.add_argument('--grid',type=int,default=256)
    ap.add_argument('--points',type=int,default=8000000);ap.add_argument('--width',type=int,default=1280);args=ap.parse_args()
    d=json.loads((ROOT/'survey'/(args.id+'.json')).read_text());field=build(d,args.grid,args.points)
    r=Renderer(field,(args.width,args.width*3//4));print(r.ctx.info['GL_RENDERER'],flush=True)
    receipt=[]
    for label,az,el in [('oblique',-48,27),('axis',45,35.26438968),('side',-90,8)]:
        start=time.time();output=ROOT/'rendering'/(args.id+'-'+label+'.png');r.image(az,el).save(output)
        receipt.append(dict(file=output.name,azimuth=az,elevation=el,seconds=time.time()-start));print(label,flush=True)
    (ROOT/'rendering'/(args.id+'-receipt.json')).write_text(json.dumps(dict(id=args.id,grid=args.grid,points=args.points,
        samples='random orbit samples from exact recipe, binary64 approximation',skin_in_voxels=.85,
        purpose='finite surface envelope; not evidence of mathematical solidity or topology',renders=receipt),indent=2)+'\n')
    r.close()

if __name__=='__main__':main()
