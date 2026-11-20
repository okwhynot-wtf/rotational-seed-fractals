"""Reproducible native 1280×720 films. No AI imagery or upscaling."""
from pathlib import Path
import argparse,json,math,time,hashlib
import numpy as np
from scipy.spatial.transform import Rotation
from PIL import Image
import imageio_ffmpeg
from adaptive_volume import ROOT,Renderer,view,build

ASSETS=ROOT/'site'/'assets'
ID='borromean-m3-q1_2-a1_3-overlap-c1_8-ax6'

def writer(path,seconds,fps=24):
    w=imageio_ffmpeg.write_frames(str(path),(1280,720),fps=fps,codec='libx264',pix_fmt_in='rgb24',pix_fmt_out='yuv420p',
       output_params=['-crf','20','-preset','medium','-movflags','+faststart','-threads','2'],ffmpeg_log_level='error')
    w.send(None);return w

def record(name,frames,renderer,callback,seconds,receipt):
    path=ASSETS/(name+'.mp4');temporary=ASSETS/(name+'.partial.mp4')
    w=writer(temporary,seconds);start=time.time()
    try:
        for i in range(frames):
            im=callback(i/frames)
            if name=='hero' and i==0:
                im.save(ASSETS/'hero-poster.jpg',quality=96,subsampling=0)
                im.save(ASSETS/'linked.jpg',quality=96,subsampling=0)
            if name=='descent' and i in [0,frames//2,frames-1]:im.save(ASSETS/f'descent-{i}.jpg',quality=95)
            w.send(np.asarray(im).tobytes())
            if i%24==0:
                status=dict(film=name,frame=i,total=frames,elapsed=time.time()-start)
                (ROOT/'rendering'/'film-progress.json').write_text(json.dumps(status)+'\n')
                print(name,i,frames,round(time.time()-start,1),flush=True)
    finally:w.close()
    actual_frames,actual_seconds=imageio_ffmpeg.count_frames_and_secs(str(temporary))
    if actual_frames != frames:
        raise RuntimeError(f'{name}: expected {frames} frames, decoded {actual_frames}')
    temporary.replace(path)
    entry=dict(file=path.name,frames=frames,fps=24,duration=seconds,width=1280,height=720,
        bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),render_seconds=time.time()-start)
    receipt[:]=[v for v in receipt if v['file']!=path.name]
    receipt.append(entry);(ROOT/'rendering'/'film-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only',nargs='+',choices=['hero','descent','membrane-orbit'],default=['hero','descent','membrane-orbit'])
    args=parser.parse_args()
    ASSETS.mkdir(parents=True,exist_ok=True)
    receipt_path=ROOT/'rendering'/'film-receipt.json'
    receipt=json.loads(receipt_path.read_text()) if receipt_path.exists() else []
    d=json.loads((ROOT/'survey'/(ID+'.json')).read_text())
    r=None
    if 'hero' in args.only or 'descent' in args.only:
        data=build(d,224,3000000);r=Renderer(d,data,(1280,720))
    if 'hero' in args.only:
        record('hero',576,r,lambda t:r.image(basis=view(-48+360*t,25+7*math.sin(2*math.pi*t)),frame=5.8),24,receipt)
    m=d['maps'][6];scale=m['r'];q=np.array(m['R']);translation=np.array(m['t']);p=np.linalg.solve(np.eye(3)-scale*q,translation)
    rv=Rotation.from_matrix(q).as_rotvec();base=view(-48,27)
    def descent(t):
        # Smooth log-scale camera from whole to two actual nested branch-6 copies.
        u=2*(3*t*t-2*t*t*t);rotation=Rotation.from_rotvec(rv*u).as_matrix();s=scale**u
        c=p-s*rotation@p
        return r.image(c,base@rotation.T,5.8*s)
    if 'descent' in args.only:
        record('descent',384,r,descent,16,receipt)
    if r is not None:r.close()
    if 'membrane-orbit' in args.only:
        from render_sheets import Renderer as SheetRenderer
        sr=SheetRenderer(5,True,(1280,720))
        record('membrane-orbit',384,sr,lambda t:sr.image(-55+360*t,30+12*math.sin(2*math.pi*t),5.6),16,receipt)
        sr.image(-55,27,5.6).save(ASSETS/'membrane.jpg',quality=96,subsampling=0);sr.close()
    print('All films complete',flush=True)

if __name__=='__main__':main()
