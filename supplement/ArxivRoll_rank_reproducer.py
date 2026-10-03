"""Synthetic counterexample using hash-checked functions from a fixed source."""
import json
import numpy as np
from pinned_functions import load_functions
load_functions('https://raw.githubusercontent.com/liangzid/ArxivRoll/709b0c5738b1710a4ac6988d70b32ffb1d21458b/rs.py', '77dcd6558602b24b51ebc035c936be6c09a7b2d0b77527700149f3fcef021237', ['getRSI_absolute', '_getRelSorting', 'getRSIRelative4AllModels'], globals())

pub=np.array([[.9,.6],[.7,.8],[.5,.4]])
pri=np.array([[.5,.8],[.9,.4],[.7,.6]])
def compute(a,b):
    pairs=np.stack([a,b],axis=2).tolist()
    # Identical unmatched matrices ensure their contribution is zero.
    return getRSIRelative4AllModels(pairs,a.tolist(),a.tolist())
permutation=np.array([1,0,2])
before=compute(pub,pri)
after=np.array(compute(pub[permutation],pri[permutation]))[np.argsort(permutation)].tolist()
assert np.allclose(before,[.7,-.7,0.])
assert np.allclose(after,[-.7,.7,0.])
assert not np.allclose(before,after)
print(json.dumps({'names':['A','B','C'],'public':pub.tolist(),'private':pri.tolist(),
                  'original_relative_RSI':before,'permuted_then_restored_relative_RSI':after},indent=2))
