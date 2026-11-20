"""Four clarity studies with finer interval subdivision and smaller overlap."""
import json
from fractions import Fraction as F
from model import ROOT,construct,checks
from verify_exact import certify

variants=[(3,3,'1/8'),(3,4,'1/8'),(3,6,'1/8'),(2,4,'3/20')]
summary=[]
certificates=[]
for m,M,q in variants:
    d=construct(m,overlap=True,central_scale=q,axis_subdivisions=M)
    d['checks']=checks(d)
    (ROOT/(d['id']+'.json')).write_text(json.dumps(d,indent=2)+'\n')
    summary.append({'id':d['id'],'map_count':len(d['maps']),**d['screen'],**d['checks']})
    bound={(3,3):F(11,5),(3,4):F(13,6),(3,6):F(17,8),(2,4):F(12,5)}[(m,M)]
    certificates.append({'id':d['id'],**certify(m,True,F(q),M,bound)})
(ROOT/'axis-variants-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(ROOT/'axis-variants-exact-certificate.json').write_text(json.dumps(certificates,indent=2)+'\n')
print(json.dumps(summary,indent=2))
