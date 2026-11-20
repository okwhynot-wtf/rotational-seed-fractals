"""Two-sided, depth-tested exact sheet subsets with a real shadow map."""
from pathlib import Path
import sys,json,math,time,argparse
import numpy as np
import moderngl as gl
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'constructive'))
from membrane import maps as membrane_maps
from corona import maps as corona_maps

VERT='''#version 430
in vec3 point,normal,colour;
uniform mat3 camera,lightCamera;uniform float frame,aspect,lightRadius;
out vec3 vnormal,vcolour,vpoint;out vec4 shadowPos;
void main(){vec3 p=camera*point;gl_Position=vec4(2.*p.x/(frame*aspect),2.*p.y/frame,-p.z/12.,1.);
 vnormal=normal;vcolour=colour;vpoint=point;vec3 l=lightCamera*point;shadowPos=vec4(l.xy/lightRadius*.5+.5,.5-l.z/(2.*lightRadius),1.);}
'''
FRAG='''#version 430
in vec3 vnormal,vcolour,vpoint;in vec4 shadowPos;out vec4 frag;
uniform sampler2D shadowMap;uniform vec3 eye,key,fill;
float shadow(){float total=0.;vec2 texel=1./vec2(textureSize(shadowMap,0));
 for(int x=-1;x<=1;x++)for(int y=-1;y<=1;y++)total+=shadowPos.z-.0007<=texture(shadowMap,shadowPos.xy+vec2(x,y)*texel).r?1.:0.;return .22+.78*total/9.;}
void main(){vec3 n=normalize(vnormal);if(!gl_FrontFacing)n=-n;float sh=shadow();
 float diffuse=max(0.,dot(n,key)),spec=pow(max(0.,dot(n,normalize(key+eye))),30.);
 float rim=pow(1.-max(0.,dot(n,eye)),3.);
 vec3 col=vcolour*(.11+1.35*diffuse*sh)*vec3(1.08,.96,.83);
 col+=vcolour*.32*max(0.,dot(n,fill))*vec3(.4,.8,1.);
 col+=mix(vec3(.78,.83,.86),vcolour,.6)*spec*.8*sh+rim*vec3(.035,.075,.095);
 frag=vec4(pow(1.-exp(-1.45*col),vec3(1./2.2)),1.);}
'''
SHADOW_VERT='''#version 430
in vec3 point;uniform mat3 lightCamera;uniform float lightRadius;
void main(){vec3 p=lightCamera*point;gl_Position=vec4(p.x/lightRadius,p.y/lightRadius,-p.z/lightRadius,1.);}
'''
SHADOW_FRAG='''#version 430
void main(){}
'''

def basis(az=-55,el=27):
    a,e=map(math.radians,(az,el));eye=np.array([math.cos(e)*math.cos(a),math.cos(e)*math.sin(a),math.sin(e)])
    right=np.array([-math.sin(a),math.cos(a),0]);return np.array([right,np.cross(eye,right),eye],dtype='f4')

def geometry(depth=5,anchored=True):
    if anchored:
        a,t=corona_maps(.1,.45,'slant','corner')
    else:a,t=membrane_maps(.4)
    count=len(a);square=np.array([[-1,-1,0],[1,-1,0],[1,1,0],[-1,1,0.]])
    M=np.eye(3)[None];T=np.zeros((1,3));labels=np.array([-1]);parts=[(square[None],np.array([-1]))]
    for level in range(depth):
        childM=np.einsum('nij,mjk->nmik',M,a).reshape(-1,3,3)
        childT=(np.einsum('nij,mj->nmi',M,t)+T[:,None,:]).reshape(-1,3)
        childlabels=np.tile(np.arange(count),len(M)) if level==0 else np.repeat(labels,count)
        keep=np.tile(np.arange(count)>=4,len(M))
        verts=np.einsum('nij,kj->nki',childM[keep],square)+childT[keep,None,:]
        parts.append((verts,childlabels[keep]));M,T,labels=childM,childT,childlabels
        print('Sheet depth',level+1,'panels',sum(len(v) for v,_ in parts),flush=True)
    panels=np.concatenate([x[0] for x in parts]);labels=np.concatenate([x[1] for x in parts]);del parts,M,T
    normals=np.cross(panels[:,1]-panels[:,0],panels[:,2]-panels[:,0]);normals/=np.linalg.norm(normals,axis=1)[:,None]
    palette=np.array([[.55,.24,.085],[.035,.37,.34],[.34,.39,.44],[.62,.43,.20]])
    colours=palette[np.maximum(0,labels)%4];colours[labels<0]=[.16,.23,.27]
    verts=panels[:,[0,1,2,0,2,3]].reshape(-1,3)
    data=np.concatenate([verts,np.repeat(normals,6,axis=0),np.repeat(colours,6,axis=0)],axis=1).astype('f4')
    return data

class Renderer:
    def __init__(self,depth=5,anchored=True,size=(1280,960)):
        self.size=size;self.ctx=ctx=gl.create_standalone_context(require=430)
        data=geometry(depth,anchored);self.vertices=len(data);self.buffer=ctx.buffer(data.tobytes());del data
        self.program=p=ctx.program(vertex_shader=VERT,fragment_shader=FRAG)
        self.vao=ctx.vertex_array(p,[(self.buffer,'3f 3f 3f','point','normal','colour')])
        self.shadowProg=sp=ctx.program(vertex_shader=SHADOW_VERT,fragment_shader=SHADOW_FRAG)
        self.shadowVao=ctx.vertex_array(sp,[(self.buffer,'3f 24x','point')])
        self.shadowTex=ctx.depth_texture((2048,2048));self.shadowTex.compare_func=''
        self.shadowTex.repeat_x=self.shadowTex.repeat_y=False
        self.shadowFrame=ctx.framebuffer(depth_attachment=self.shadowTex)
        self.scene=ctx.simple_framebuffer(size,components=3,samples=4);self.output=ctx.simple_framebuffer(size,components=3)
        ctx.enable(gl.DEPTH_TEST)
    def image(self,az=-55,el=27,frame=5.6):
        cam=basis(az,el);key=cam.T@np.array([-.6,.9,.65]);key/=np.linalg.norm(key)
        kr=np.cross([0,0,1],key);kr/=np.linalg.norm(kr);lc=np.array([kr,np.cross(key,kr),key],dtype='f4')
        self.shadowFrame.use();self.shadowFrame.clear(depth=1.);self.shadowProg['lightCamera'].write(lc.T.tobytes());self.shadowProg['lightRadius'].value=5.
        self.shadowVao.render(mode=gl.TRIANGLES)
        self.shadowTex.use(0);p=self.program;p['shadowMap'].value=0
        p['camera'].write(cam.T.tobytes());p['lightCamera'].write(lc.T.tobytes());p['lightRadius'].value=5.
        p['frame'].value=frame;p['aspect'].value=self.size[0]/self.size[1]
        fill=cam.T@np.array([.9,.4,.2]);fill/=np.linalg.norm(fill)
        for name,v in [('eye',cam[2]),('key',key),('fill',fill)]:p[name].value=tuple(v)
        self.scene.use();self.scene.clear(.008,.014,.022,depth=1.);self.vao.render(mode=gl.TRIANGLES)
        self.ctx.copy_framebuffer(self.output,self.scene)
        return Image.frombytes('RGB',self.size,self.output.read(components=3,alignment=1)).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    def close(self):
        for x in [self.vao,self.shadowVao,self.buffer,self.scene,self.output,self.shadowFrame,self.shadowTex,self.program,self.shadowProg]:x.release()
        self.ctx.release()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--depth',type=int,default=5);ap.add_argument('--width',type=int,default=1400);args=ap.parse_args()
    renderer=Renderer(args.depth,True,(args.width,args.width*3//4));receipt=[]
    for label,az,el in [('oblique',-55,27),('above',-45,65),('low',-40,12)]:
        start=time.time();output=ROOT/'rendering'/('anchored-slant-'+label+'.png');renderer.image(az,el).save(output)
        receipt.append(dict(file=output.name,azimuth=az,elevation=el,seconds=time.time()-start));print(label,flush=True)
    (ROOT/'rendering'/'anchored-slant-receipt.json').write_text(json.dumps(dict(depth=args.depth,triangles=renderer.vertices//3,
        geometry='Exact contained square sheets through finite word depth; residual set omitted. No artificial sheet thickness.',renders=receipt),indent=2)+'\n')
    renderer.close()

if __name__=='__main__':main()
