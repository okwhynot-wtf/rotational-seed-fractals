"""Decode every published film; verify frames, size, hashes and finite visual output."""
from pathlib import Path
import hashlib,json
import imageio_ffmpeg
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[1]

def main():
    receipts=json.loads((ROOT/'rendering/film-receipt.json').read_text())
    expected={'hero.mp4':576,'descent.mp4':384,'membrane-orbit.mp4':384}
    if {r['file'] for r in receipts}!=set(expected):raise RuntimeError('Incomplete film receipt')
    sheet=Image.new('RGB',(4*384,3*238),'#080d10');draw=ImageDraw.Draw(sheet)
    result=[]
    for row,r in enumerate(receipts):
        path=ROOT/'site/assets'/r['file']
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        if digest!=r['sha256']:raise RuntimeError(f'Hash mismatch: {path}')
        stream=imageio_ffmpeg.read_frames(str(path),pix_fmt='rgb24');meta=next(stream)
        if tuple(meta['size'])!=(1280,720):raise RuntimeError('Unexpected resolution')
        picks=[0,expected[r['file']]//3,2*expected[r['file']]//3,expected[r['file']]-1]
        hashes=[];variances=[];count=0
        for i,frame in enumerate(stream):
            a=np.frombuffer(frame,dtype=np.uint8).reshape(720,1280,3)
            if i in picks:
                col=picks.index(i);image=Image.fromarray(a)
                sheet.paste(image.resize((384,216)),(col*384,row*238+22))
                draw.text((col*384+5,row*238+5),f"{r['file']}  frame {i}",fill='#c7efea')
                hashes.append(hashlib.sha256(frame).hexdigest());variances.append(float(a.var()))
            count+=1
        if count!=expected[r['file']]:raise RuntimeError(f'Frame count mismatch: {path}: {count}')
        if min(variances)<20 or len(set(hashes))<3:raise RuntimeError(f'Empty or static film: {path}')
        result.append(dict(file=r['file'],decoded_frames=count,size=list(meta['size']),fps=meta['fps'],
                           duration=meta['duration'],sha256=digest,sample_pixel_variances=variances))
    sheet.save(ROOT/'rendering/film-contact-sheet.jpg',quality=92)
    (ROOT/'rendering/media-validation.json').write_text(json.dumps(dict(status='passed',films=result,
        scope='Full decode, metadata, hashes and finite-frame variation. Contact sheet inspected separately; this is not a mathematical proof.'),indent=2)+'\n')
    print(json.dumps(dict(status='passed',decoded_frames=sum(v['decoded_frames'] for v in result),films=len(result))))

if __name__=='__main__':main()
