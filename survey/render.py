"""Finite deterministic-seed point previews of the Borromean IFS survey."""
from pathlib import Path
import argparse
import json
import math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import moderngl
from model import ROOT,sample

class Renderer:
    def __init__(self):
        self.ctx=moderngl.create_standalone_context(require=330)
        self.program=self.ctx.program(vertex_shader='''#version 330
in vec3 position; in vec3 colour;
uniform mat3 basis; uniform vec3 centre; uniform vec3 halfsize;
uniform float pointsize; out vec3 col; out float shade;
void main(){vec3 v=basis*(position-centre);gl_Position=vec4(v/halfsize,1.);
gl_PointSize=pointsize;col=colour;shade=clamp(.93-.18*v.z/halfsize.z,.65,1.13);}
''',fragment_shader='''#version 330
in vec3 col;in float shade;out vec4 frag;
void main(){vec2 p=gl_PointCoord*2.-1.;float d=dot(p,p);if(d>1.)discard;
float light=.54+.46*sqrt(max(0.,1.-d));frag=vec4(col*light*shade,1.);}
''')
    def image(self,points,colour,size=(1000,1000),az=45,el=35.264,centre=(0,0,0),span=2.25):
        az,el=np.deg2rad([az,el]);eye=np.array([np.cos(el)*np.cos(az),np.cos(el)*np.sin(az),np.sin(el)])
        right=np.cross([0,0,1],eye);right/=np.linalg.norm(right);up=np.cross(eye,right)
        basis=np.array([right,up,-eye]);aspect=size[0]/size[1]
        data=np.column_stack((points,colour)).astype('f4');buf=self.ctx.buffer(data.tobytes())
        vao=self.ctx.vertex_array(self.program,[(buf,'3f 3f','position','colour')])
        fbo=self.ctx.simple_framebuffer((size[0]*2,size[1]*2),components=3)
        fbo.use();fbo.clear(.018,.027,.04,depth=1.)
        self.ctx.enable(moderngl.DEPTH_TEST|moderngl.PROGRAM_POINT_SIZE)
        self.program['basis'].write(basis.T.astype('f4').tobytes())
        self.program['centre'].value=centre;self.program['halfsize'].value=(span*aspect,span,4.)
        self.program['pointsize'].value=3.8
        vao.render(moderngl.POINTS)
        im=Image.frombytes('RGB',fbo.size,fbo.read(components=3)).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        vao.release();buf.release();fbo.release()
        return im.resize(size,Image.Resampling.LANCZOS)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--count',type=int,default=900000)
    parser.add_argument('--summary',default='summary.json');parser.add_argument('--sheet',default='contact-sheet.jpg');args=parser.parse_args()
    output=ROOT/'previews';output.mkdir(exist_ok=True)
    rend=Renderer();summary=json.loads((ROOT/args.summary).read_text());cards=[]
    palette=np.array([[.24,.77,.79],[.94,.57,.29],[.69,.65,.96],[.53,.64,.70],[.88,.85,.70]])
    font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',20)
    for item in summary:
        d=json.loads((ROOT/(item['id']+'.json')).read_text());points,ids=sample(d,args.count)
        groups=np.array([m['orbit'] for m in d['maps']]);colors=palette[groups[ids]]
        span=max(2.25,d['screen']['invariant_ball_radius']*.9)
        im=rend.image(points,colors,span=span)
        im.save(output/(d['id']+'.png'))
        oblique=rend.image(points,colors,az=-45,el=22,span=span)
        oblique.save(output/(d['id']+'-oblique.png'))
        thumb=im.resize((500,500));card=Image.new('RGB',(500,566),'#071019');card.paste(thumb)
        draw=ImageDraw.Draw(card);draw.text((16,504),d['id'].replace('borromean-',''),font=font,fill='#dce7ed')
        draw.text((16,532),f"{len(d['maps'])} maps · dim_H ≤ {item['similarity_dimension_upper_bound']:.4f}",font=font,fill='#9badb5')
        cards.append(card)
        print(d['id'],flush=True)
    cols=2 if len(cards)==4 else 3
    sheet=Image.new('RGB',(cols*500,math.ceil(len(cards)/cols)*566),'#071019')
    for i,card in enumerate(cards):sheet.paste(card,((i%cols)*500,(i//cols)*566))
    sheet.save(output/args.sheet,quality=94)
    print(output/args.sheet)

if __name__=='__main__':main()
