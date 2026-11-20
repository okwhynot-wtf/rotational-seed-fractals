"""Bounded exact no-overlap screen using injective modular images as witnesses.

No full rational matrix arrays are retained. If all modular images differ,
all rational affine maps differ; the converse is not assumed.
"""
from pathlib import Path
import json
from certify_bounds import maps_for,Q,Q13

MODULUS=2147483647
IDENTITY=(1,0,0,0,1,0,0,0,1,0,0,0)

def reduced(x):return (x.numerator*pow(x.denominator,-1,MODULUS))%MODULUS

def compose(a,b):
    p=MODULUS
    matrix=tuple(sum(a[3*i+k]*b[3*k+j] for k in range(3))%p for i in range(3) for j in range(3))
    shift=tuple((sum(a[3*i+k]*b[9+k] for k in range(3))+a[9+i])%p for i in range(3))
    return matrix+shift

def screen(rotation,depth=5):
    transforms=[tuple(reduced(x) for row in m for x in row)+tuple(reduced(x) for x in t)
                for m,t,*_ in maps_for(rotation)]
    seen={IDENTITY:''};front=[(IDENTITY,'')];collisions=[];counts=[1]
    for n in range(1,depth+1):
        nxt=[]
        for matrix,word in front:
            for j,t in enumerate(transforms):
                child=compose(matrix,t);childword=word+str(j)
                if child in seen:collisions.append((seen[child],childword))
                else:seen[child]=childword
                nxt.append((child,childword))
        counts.append(len(nxt));front=nxt
    assert not collisions,collisions[:5]
    return dict(max_word_length=depth,word_counts_including_empty=counts,
                total_words=sum(counts),distinct_modular_affine_images=len(seen),
                modular_collisions=0,modulus=MODULUS,
                exact_conclusion='Every two distinct words of length at most 5 define distinct rational affine maps.',
                justification='Rational equality would imply equality after reduction; every denominator is invertible modulo the specified modulus.')

def main():
    result={name:screen(q) for name,q in [('original125',Q),('norm13',Q13)]}
    result['norm13_minimum_maximum_word_length']=6
    result['minimum_scope']='No pair with both lengths <=5 coincides; a length6/length6 pair is explicitly certified. Together with the separate free-core-rotation proof, which forces equal word lengths in every affine coincidence, the minimum combined length is 12.'
    (Path(__file__).resolve().parent/'short_word_screen.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
