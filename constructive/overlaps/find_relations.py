"""Search explicit membrane overlaps using exact rational plane intersections."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from functools import reduce
from math import gcd,lcm,log2
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from export_exact import Q,Z,I,mul,transpose,vector,recipe

HERE=Path(__file__).resolve().parent
R=[];z=I
for k in range(4):
    R.append(mul(mul(z,Q),transpose(z)));z=mul(Z,z)

def primitive_pair(rotation):
    # w lies in the input xy plane and its image lies in the output xy plane.
    w=(rotation[2][1],-rotation[2][0],F(0))
    if w[:2]==(0,0):return None
    v=vector(rotation,w)
    denominator=lcm(*(x.denominator for x in w+v))
    nums=tuple(int(x*denominator) for x in w+v)
    common=reduce(gcd,(abs(x) for x in nums))
    nums=tuple(x//common for x in nums)
    w,v=nums[:3],nums[3:]
    if not all(x%2 for x in w[:2]+v[:2]):return None
    assert vector(rotation,w)==v
    return w,v

def base_word(numerators,length):
    """Decode odd vector /2^length as a word in the 4 square tiling maps."""
    assert all(abs(v)<2**length and v%2 for v in numerators)
    unsigned=[(v+2**length-1)//2 for v in numerators]
    return [2*((unsigned[0]>>j)&1)+((unsigned[1]>>j)&1) for j in range(length-1,-1,-1)]

def compose(word,maps):
    matrix=I;shift=(F(0),)*3
    for i in word:
        a,b,*_=maps[i]
        shift=tuple(x+y for x,y in zip(vector(matrix,b),shift));matrix=mul(matrix,a)
    return matrix,shift

def make_relation(hword,rotation):
    pair=primitive_pair(rotation)
    if pair is None:return None
    w,v=pair;n=len(hword)
    for d in range(1,100):
        if max(abs(x) for x in v[:2])>=2**d:continue
        for tiny in product((-1,1),repeat=2):
            large=tuple(tiny[j]+2**(1+2*n)*w[j] for j in range(2))
            if max(abs(x) for x in large)>=2**(d+1):continue
            inside=base_word(large,d+1);outer=base_word(v[:2],d);inner=base_word(tiny,1)
            h=[j+4 for j in hword]
            left=h+inside;right=outer+h+inner
            assert left!=right and len(left)==len(right)
            maps=recipe(F(1,4))
            assert compose(left,maps)==compose(right,maps)
            return dict(hword=h,rotation=[[str(x) for x in row] for row in rotation],
                        W=list(w),V=list(v),outer_length=d,
                        long_inner_numerators=list(large),short_inner_numerators=list(tiny),
                        left=left,right=right,word_length=len(left),
                        contraction_power_of_two=(d+1+2*n),
                        identity='F_left = F_right exactly; both act x -> 2^(-contraction_power_of_two) R x + t')
    raise RuntimeError('No relation found')

def main():
    records=[]
    for n in range(1,5):
        for word in product(range(4),repeat=n):
            mat=I
            for j in word:mat=mul(mat,R[j])
            rel=make_relation(word,mat)
            if rel:records.append(rel)
    records.sort(key=lambda row:(row['word_length'],row['contraction_power_of_two'],row['hword']))
    output={'scope':'Exact search within the two-block plane-intersection construction; no global shortest-word claim.',
            'rotation_words_checked':sum(4**n for n in range(1,5)),
            'relation_count':len(records),'best':records[:12]}
    (HERE/'exact_relations.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))

if __name__=='__main__':main()
