"""Finite modular premises for elementary quaternion free-group proofs."""
from itertools import product
from pathlib import Path
from fractions import Fraction as F
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from export_exact import Q

def qm(a,b):
    w,x,y,z=a;v,i,j,k=b
    return (w*v-x*i-y*j-z*k,w*i+x*v+y*k-z*j,w*j-x*k+y*v+z*i,w*k+x*j-y*i+z*v)
def conj(q):return (q[0],-q[1],-q[2],-q[3])
def representation(q,p,root):
    a,b,c,d=q
    return ((a+root*b)%p,(c+root*d)%p,(-c+root*d)%p,(a-root*b)%p)
def mm(a,b,p):return ((a[0]*b[0]+a[1]*b[2])%p,(a[0]*b[1]+a[1]*b[3])%p,(a[2]*b[0]+a[3]*b[2])%p,(a[2]*b[1]+a[3]*b[3])%p)
def rotation(q):
    a,b,c,d=q;n=sum(x*x for x in q)
    return tuple(tuple(F(x,n) for x in row) for row in
                 ((a*a+b*b-c*c-d*d,2*(b*c-a*d),2*(b*d+a*c)),
                  (2*(b*c+a*d),a*a-b*b+c*c-d*d,2*(c*d-a*b)),
                  (2*(b*d-a*c),2*(c*d+a*b),a*a-b*b-c*c+d*d)))

def check(p,root,generators):
    assert root*root%p==p-1
    for q in generators:assert sum(x*x for x in q)==p and conj(q) in generators
    matrices=[representation(q,p,root) for q in generators]
    for a in matrices:assert a!=(0,0,0,0) and (a[0]*a[3]-a[1]*a[2])%p==0
    zero_pairs=[]
    for i,a in enumerate(generators):
        for j,b in enumerate(generators):
            assert representation(qm(a,b),p,root)==mm(matrices[i],matrices[j],p)
            zero=mm(matrices[i],matrices[j],p)==(0,0,0,0)
            assert zero==(b==conj(a))
            if zero:zero_pairs.append([i,j])
    return dict(prime=p,square_root_of_minus_one=root,generators=generators,
                nonzero_rank_one_matrices=len(matrices),ordered_pairs_checked=len(matrices)**2,
                zero_products_exactly_inverse_pairs=zero_pairs)

def main():
    g5=[]
    for axis in range(3):
        for sign in (1,-1):
            q=[1,0,0,0];q[1+axis]=2*sign;g5.append(tuple(q))
    g13=[(1,2*a,2*b,2*c) for a,b,c in product((-1,1),repeat=3)]
    for axis in range(3):
        for sign in (1,-1):
            q=[3,0,0,0];q[1+axis]=2*sign;g13.append(tuple(q))
    y=g5[2];z=g5[4]
    product_q=qm(qm(conj(y),conj(z)),y)
    assert product_q==(5,8,0,6) and rotation(product_q)==Q
    p=(1,2,2,2)
    assert rotation(p)==tuple(tuple(F(x,13) for x in row) for row in ((-3,4,12),(12,-3,4),(4,12,-3)))
    data={'norm5':check(5,2,g5),'norm13':check(13,5,g13),
          'original_Q_quaternion':product_q,
          'original_Q_free_word':'Y^-1 T^-1 Y',
          'original_C4_orbit_words':['Y^-1 T^-1 Y','X T^-1 X^-1','Y T^-1 Y^-1','X^-1 T^-1 X'],
          'notation':'X,Y,T denote the norm-5 rotations about the coordinate axes; T is not the C4 symmetry rotation.',
          'norm13_core_quaternions':[(1,2,2,2),(1,-2,2,2),(1,-2,-2,2),(1,2,-2,2)],
          'scope':'Finite premises checked here; full reduced-word argument is in OVERLAPS.md.'}
    (Path(__file__).resolve().parent/'free_rotation_certificate.json').write_text(json.dumps(data,indent=2)+'\n')
    print('Passed: 36 norm-5 and 196 norm-13 pair tests; exact Q quaternion factorization.')

if __name__=='__main__':main()
