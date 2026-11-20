"""Separate exact export; does not alter the original membrane definition."""
from pathlib import Path
import hashlib
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from export_exact import verify,encode,block
from certify_bounds import maps_for,Q13

def main():
    folder=Path(__file__).resolve().parent
    maps=maps_for(Q13);permutation=verify(maps)
    source=('# Distinct norm-13 membrane variant; original reference is unchanged.\n'
            '# Exact rational similarities. See OVERLAPS.md for certified claims.\n'+
            block('MembraneNorm13','Membrane norm13 - q1/4 - 8 exact similarities',maps,
                  '[[4,-6,3],[0,0,0],[0,0,1],36]')+'\n')
    target=folder/'Membrane-Norm13-q1_4-Exact.aifs';target.write_text(source,encoding='utf-8')
    recipe={'model':'norm13','q':'1/4','maps':encode(maps),'C4_permutation':permutation,
            'proof':'OVERLAPS.md','topological_dimension':2,'assouad_dimension':3,
            'hausdorff_dimension':'2 < dim_H K < 2.270907424784688; exact value unresolved',
            'shortest_affine_overlap':['410033','211040'],
            'native_import':'not tested','aifs_sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
    (folder/'norm13-exact-recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    print(target)

if __name__=='__main__':main()
