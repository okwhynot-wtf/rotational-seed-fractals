"""Dense m=1 end of the same C3 Borromean family, with exact scalar checks."""
import json
from fractions import Fraction as F
from model import ROOT,construct,checks
from verify_exact import certify

summary=[];certificates=[]
for twist in ['0','1/2','1']:
    d=construct(1,edge_twist=twist,overlap=True,central_scale='1/8',axis_subdivisions=6)
    d['checks']=checks(d)
    (ROOT/(d['id']+'.json')).write_text(json.dumps(d,indent=2)+'\n')
    summary.append({'id':d['id'],'map_count':len(d['maps']),**d['screen'],**d['checks']})
    certificates.append({'id':d['id'],**certify(1,True,F(1,8),6,F(3))})
(ROOT/'dense-variants-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(ROOT/'dense-variants-exact-certificate.json').write_text(json.dumps(certificates,indent=2)+'\n')
print(json.dumps(summary,indent=2))
