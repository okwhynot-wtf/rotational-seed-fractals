"""Exact rational link-diagram and Fox 3-colouring checks.

Independent of the survey generator. This certifies a polygonal subset,
not the topology of the whole similarity attractor or its complement.
"""
from fractions import Fraction as F
from pathlib import Path
import json
from itertools import combinations

HERE = Path(__file__).resolve().parent

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def mul(a,t): return tuple(x*t for x in a)
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def proj(a): return (17*a[0]-7*a[2], 17*a[1]-11*a[2])
def cyclic(a): return (a[2],a[0],a[1])

R0 = [tuple(map(F,p)) for p in [(-2,-1,0),(2,-1,0),(2,1,0),(-2,1,0)]]
RINGS=[R0,[cyclic(p) for p in R0],[cyclic(cyclic(p)) for p in R0]]

def rank_mod(a,p):
    a=[[int(x)%p for x in row] for row in a]
    if not a:return 0
    row=0
    for col in range(len(a[0])):
        pivot=next((i for i in range(row,len(a)) if a[i][col]),None)
        if pivot is None:continue
        a[row],a[pivot]=a[pivot],a[row]
        inv=pow(a[row][col],-1,p)
        a[row]=[(x*inv)%p for x in a[row]]
        for i in range(len(a)):
            if i!=row and a[i][col]:
                factor=a[i][col]
                a[i]=[(x-factor*y)%p for x,y in zip(a[i],a[row])]
        row+=1
        if row==len(a):break
    return row

def diagram(ids):
    crossings=[]
    for i,j in combinations(ids,2):
        for ei in range(4):
            a,b=RINGS[i][ei],RINGS[i][(ei+1)%4]
            da=sub(b,a);pa=proj(a);d=proj(da)
            for ej in range(4):
                c,e=RINGS[j][ej],RINGS[j][(ej+1)%4]
                db=sub(e,c);pc=proj(c);f=proj(db)
                determinant=det(d,f)
                if not determinant:continue
                delta=sub(pc,pa)
                t=det(delta,f)/determinant
                s=det(delta,d)/determinant
                if 0<=t<=1 and 0<=s<=1:
                    assert 0<t<1 and 0<s<1, 'Projection has vertex on another segment'
                    ai=add(a,mul(da,t));bj=add(c,mul(db,s))
                    depth=dot(sub(ai,bj),(7,11,17))
                    assert depth != 0, 'Actual intersection between polygon components'
                    over,under=(i,j) if depth>0 else (j,i)
                    ot,ut=(ei+t,ej+s) if depth>0 else (ej+s,ei+t)
                    # Oriented crossing sign, consistent for all components.
                    sign=(1 if determinant>0 else -1)*(1 if depth>0 else -1)
                    crossings.append(dict(over=over,under=under,ot=ot,ut=ut,sign=sign,
                                          plane=proj(ai),depth_gap=abs(depth)))
    assert len(set(x['plane'] for x in crossings))==len(crossings), 'Multiple crossing'
    under_times={i:sorted(c['ut'] for c in crossings if c['under']==i) for i in ids}
    offsets={};count=0
    for i in ids:
        offsets[i]=count;count+=max(1,len(under_times[i]))
    matrix=[]
    for c in crossings:
        u,o=c['under'],c['over'];ut=under_times[u];ot=under_times[o]
        k=ut.index(c['ut']);incoming=offsets[u]+(k-1)%len(ut);outgoing=offsets[u]+k
        prev=max((k for k,t in enumerate(ot) if t<c['ot']),default=len(ot)-1)
        oa=offsets[o]+(prev if ot else 0)
        row=[0]*count;row[oa]+=2;row[incoming]-=1;row[outgoing]-=1
        matrix.append(row)
    rank=rank_mod(matrix,3)
    linking={f'{i}-{j}':sum(c['sign'] for c in crossings if {c['over'],c['under']}=={i,j})//2
             for i,j in combinations(ids,2)}
    return dict(components=list(ids),crossings=crossings,arc_count=count,
                fox3_matrix=matrix,fox3_rank=rank,fox3_colourings=3**(count-rank),
                unlink_colourings=3**len(ids),linking_numbers=linking)

def main():
    full=diagram((0,1,2));pairs=[diagram(pair) for pair in combinations(range(3),2)]
    assert len(full['crossings'])>=6
    assert full['fox3_colourings']==3
    assert all(p['fox3_colourings']==9 for p in pairs)
    assert all(x==0 for x in full['linking_numbers'].values())
    result={'exact_arithmetic':'fractions.Fraction; no tolerance-based decisions',
            'definition':'Rectangles (±2,±1,0), and cyclic coordinate permutations.',
            'projection':'(17x-7z,17y-11z), depth 7x+11y+17z; no projected vertex on a different segment',
            'full':full,'pairs':pairs,
            'conclusion':'The three disjoint polygon components are not the three-component unlink: Fox 3-colouring counts differ. Each pair has zero linking number. Pair colour counts alone do not prove pairwise unlinking; an explicit separation argument is required.',
            'scope':'Embedded polygonal subset only. Does not classify the ambient attractor or establish historical novelty.'}
    (HERE/'link_certificate.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
    print(json.dumps({'crossings':len(full['crossings']),'full_colours':full['fox3_colourings'],
                      'pair_colours':[p['fox3_colourings'] for p in pairs],
                      'linking_numbers':full['linking_numbers']}))

if __name__=='__main__':main()
