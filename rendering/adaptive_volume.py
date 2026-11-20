"""Adaptive similarity copies of the finite sampled field, with real depth.

This renews geometric detail in actual descendant copies during a camera zoom.
Every displayed instance comes from an IFS word. Skin/field approximation is
still finite and explicitly distinguished from the mathematical set.
"""
from pathlib import Path
import json,math,time,argparse
import numpy as np
import moderngl as gl
from PIL import Image
from render_volume import ROOT,build

VERT='''#version 430
in vec3 instanceCentre,row0,row1,row2,instanceColour;
in float instanceScale;
uniform vec3 cameraCentre,right,up,eye;
uniform float frame,aspect,radius,skin;
out vec2 screen;
flat out vec3 c;
flat out mat3 rot;
flat out float s;
flat out vec3 material;
void main(){vec2 corners[6]=vec2[6](vec2(-1,-1),vec2(1,-1),vec2(1,1),vec2(-1,-1),vec2(1,1),vec2(-1,1));
 c=instanceCentre;rot=mat3(row0,row1,row2);s=instanceScale;material=instanceColour;
 vec3 p=c-cameraCentre;vec2 centre=vec2(dot(p,right),dot(p,up));
 screen=centre+corners[gl_VertexID]*(radius*s+skin);
 gl_Position=vec4(screen/vec2(frame*.5*aspect,frame*.5),-(dot(p,eye)+radius*s+skin)/10.,1.);}
'''
FRAG='''#version 430
in vec2 screen;flat in vec3 c;flat in mat3 rot;flat in float s;
flat in vec3 material;
out vec4 frag;
uniform sampler3D fieldTex,colourTex;
uniform vec3 cameraCentre,right,up,eye;
uniform float extent,spacing,skin,exposure;
float dist(vec3 p){vec3 c=clamp(p,vec3(-extent),vec3(extent));return texture(fieldTex,c/(2.*extent)+.5).r+length(p-c)-skin/s;}
vec3 normal(vec3 p){float e=spacing*.85;return normalize(vec3(
dist(p+vec3(e,0,0))-dist(p-vec3(e,0,0)),dist(p+vec3(0,e,0))-dist(p-vec3(0,e,0)),dist(p+vec3(0,0,e))-dist(p-vec3(0,0,e))));}
float shadow(vec3 p,vec3 light){float t=spacing*3.,result=1.;
 for(int i=0;i<45;++i){float d=dist(p+t*light);result=min(result,9.*d/t);if(d<spacing*.12)return .2;
 t+=max(spacing*.8,d*.8);if(t>4.)break;}return .2+.8*clamp(result,0.,1.);}
void main(){float depth=dot(c-cameraCentre,eye);
 vec3 origin=cameraCentre+screen.x*right+screen.y*up+depth*eye;
 vec3 p0=transpose(rot)*(origin-c)/s,ray=transpose(rot)*(-eye);
 float closest=dot(-p0,ray);float discr=closest*closest-dot(p0,p0)+(extent+skin/s)*(extent+skin/s);
 if(discr<0.)discard;float t=closest-sqrt(discr),end=closest+sqrt(discr);bool hit=false;
 for(int i=0;i<360;++i){float d=dist(p0+t*ray);if(d<spacing*.12){hit=true;break;}
 t+=max(spacing*.12,d*.65);if(t>end)break;}if(!hit)discard;
 vec3 p=p0+t*ray,nLocal=normal(p),n=rot*nLocal;
 vec3 key=normalize(-.6*right+.9*up+.65*eye),fill=normalize(.9*right+.4*up+.2*eye);
 vec3 colour=mix(material,texture(colourTex,p/(2.*extent)+.5).rgb,.2);
 float ao=0.;for(int i=1;i<=4;i++){float d=float(i)*.09;ao+=max(0.,d-dist(p+nLocal*d))*.8;}ao=exp(-2.*ao);
 float sh=shadow(p+nLocal*spacing*2.,transpose(rot)*key);
 float diffuse=max(0.,dot(n,key)),spec=pow(max(0.,dot(n,normalize(key+eye))),28.);
 float rim=pow(1.-max(0.,dot(n,eye)),2.4);
 vec3 col=colour*(.14+sh*diffuse*1.5)*vec3(1.07,.94,.81)*ao;
 col+=colour*.3*max(0.,dot(n,fill))*vec3(.35,.76,1.);
 col+=mix(vec3(.7,.75,.8),colour,.6)*spec*.9*sh*ao+vec3(.09,.21,.29)*rim*ao;
 col=pow(1.-exp(-exposure*col),vec3(1./2.2));frag=vec4(col,1.);
 gl_FragDepth=.5-.05*(depth-s*t);}
'''

def view(az,elev):
    az,el=map(math.radians,(az,elev));eye=np.array([math.cos(az)*math.cos(el),math.sin(az)*math.cos(el),math.sin(el)])
    right=np.array([-math.sin(az),math.cos(az),0]);up=np.cross(eye,right)
    return np.array([right,up,eye])

def select(d,centre,basis,frame,aspect,relative=.15,max_leaves=60000):
    maps=d['maps'];r=np.array([m['r'] for m in maps]);Q=np.array([m['R'] for m in maps]);T=np.array([m['t'] for m in maps])
    radius=float(d['screen']['invariant_ball_radius'])+.10
    scale_ref=frame/5.8
    palette=np.array([[.80,.32,.09],[.025,.46,.43],[.43,.39,.64],[.16,.26,.32],[.30,.36,.39]])
    edge_scale=next(m['r'] for m in maps if m['kind']=='ring')
    detail=max(0.,math.log(max(scale_ref,1e-15))/math.log(edge_scale))
    colour_depth=int(detail);blend=detail-colour_depth
    pending=[(1.,np.eye(3),np.zeros(3),0,())];leaves=[]
    while pending:
        s,u,c,dep,address=pending.pop();p=basis@(c-centre);rad=radius*s+frame*.002
        if abs(p[0])>frame*.5*aspect+rad or abs(p[1])>frame*.5+rad:continue
        if s<=relative*scale_ref or dep>=16:
            first=address[min(colour_depth,len(address)-1)]
            second=address[min(colour_depth+1,len(address)-1)]
            colour=palette[maps[first]['orbit']]*(1-blend)+palette[maps[second]['orbit']]*blend
            leaves.append((p[2]+rad,np.r_[c,u.T.ravel(),s,colour]))
            if len(leaves)>max_leaves:raise RuntimeError('Adaptive leaf budget exceeded')
        else:
            children=T@u.T*s+c;rotations=np.einsum('ij,njk->nik',u,Q)
            pending.extend((s*ri,ui,ci,dep+1,address+(j,)) for j,(ri,ui,ci) in enumerate(zip(r,rotations,children)))
    leaves.sort(key=lambda x:-x[0])
    return np.array([row for _,row in leaves],dtype='f4')

class Renderer:
    def __init__(self,d,data,size=(1280,720)):
        self.d=d;self.size=size;self.ctx=ctx=gl.create_standalone_context(require=430)
        self.program=p=ctx.program(vertex_shader=VERT,fragment_shader=FRAG)
        n=data['distance'].shape[0]
        self.field=ctx.texture3d((n,n,n),1,data['distance'].astype('f4').tobytes(),dtype='f4')
        self.colour=ctx.texture3d((n,n,n),3,data['colour'].tobytes())
        for i,tex in enumerate([self.field,self.colour]):
            tex.filter=gl.LINEAR,gl.LINEAR;tex.repeat_x=tex.repeat_y=tex.repeat_z=False;tex.use(i)
        p['fieldTex'].value=0;p['colourTex'].value=1;p['extent'].value=float(data['extent'])
        p['radius'].value=float(d['screen']['invariant_ball_radius'])+.1
        p['spacing'].value=float(data['spacing']);p['skin'].value=float(data['spacing'])*.85
        p['exposure'].value=1.3;p['aspect'].value=size[0]/size[1]
        self.output=ctx.simple_framebuffer(size,components=3);self.buffer=None;self.vao=None
        ctx.enable(gl.DEPTH_TEST)
    def image(self,centre=(0,0,0),basis=None,frame=5.8,relative=.15):
        centre=np.array(centre);basis=view(-48,27) if basis is None else np.array(basis)
        start=time.time();leaves=select(self.d,centre,basis,frame,self.size[0]/self.size[1],relative)
        if self.vao:self.vao.release();self.buffer.release()
        self.buffer=self.ctx.buffer(leaves.tobytes());self.vao=self.ctx.vertex_array(self.program,[(self.buffer,'3f 3f 3f 3f 1f 3f /i','instanceCentre','row0','row1','row2','instanceScale','instanceColour')])
        p=self.program
        for name,v in [('cameraCentre',centre),('right',basis[0]),('up',basis[1]),('eye',basis[2])]:p[name].value=tuple(v)
        p['frame'].value=frame;p['skin'].value=frame*.0018;self.output.use();self.output.clear(.008,.014,.022,depth=1.)
        self.vao.render(mode=gl.TRIANGLES,vertices=6,instances=len(leaves))
        im=Image.frombytes('RGB',self.size,self.output.read(components=3,alignment=1)).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        self.last={'leaves':len(leaves),'seconds':time.time()-start};return im
    def close(self):
        for x in [self.vao,self.buffer,self.output,self.field,self.colour,self.program]:
            if x:x.release()
        self.ctx.release()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--id',default='borromean-m3-q1_2-a1_3-overlap-c1_8-ax6');ap.add_argument('--width',type=int,default=960);ap.add_argument('--branch',type=int,default=10);args=ap.parse_args()
    d=json.loads((ROOT/'survey'/(args.id+'.json')).read_text());field=build(d,224,3000000)
    renderer=Renderer(d,field,(args.width,args.width*3//4));basis=view(-48,27)
    c=np.zeros(3);u=np.eye(3);s=1.;m=d['maps'][args.branch];receipts=[]
    for depth in range(3):
        output=ROOT/'rendering'/(args.id+f'-adaptive-{depth}.png')
        renderer.image(c,basis@u.T,5.8*s).save(output);print(depth,renderer.last,flush=True)
        receipts.append(dict(depth=depth,centre=c.tolist(),orientation=u.tolist(),scale=s,**renderer.last))
        c+=s*u@np.array(m['t']);s*=m['r'];u=u@np.array(m['R'])
    (ROOT/'rendering'/(args.id+'-adaptive-receipt.json')).write_text(json.dumps(dict(branch=args.branch,frames=receipts,
        method='Adaptive complete word cover after frustum culling; each leaf uses sampled local field. Geometry is renewed inside actual copies; finite envelope, not proof.'),indent=2)+'\n')
    renderer.close()

if __name__=='__main__':main()
