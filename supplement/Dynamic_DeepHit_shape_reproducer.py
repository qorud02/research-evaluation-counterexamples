"""Synthetic counterexample using hash-checked functions from a fixed source."""
import json
import numpy as np
from pinned_functions import load_functions
load_functions('https://raw.githubusercontent.com/chl8856/Dynamic-DeepHit/b2e208f65233405079a462b703a94556ad30d1f4/utils_eval.py', '5bdef36df094af8eae29c4c7801933d0e559029efaefb9edae5927c2e13db010', ['c_index', 'brier_score'], globals())

t = np.array([[1.0], [3.0]])
d = np.array([1, 1])
perfect = np.array([1.0, 0.0])
out = {'times':t.tolist(), 'events':d.tolist(), 'horizon':2,
       'broadcast_target_shape':list(((t<=2)*d).shape),
       'brier_column_time_perfect':float(brier_score(perfect,t,d,2)),
       'brier_flat_time_perfect':float(brier_score(perfect,t[:,0],d,2)),
       'brier_column_time_reversed':float(brier_score(1-perfect,t,d,2)),
       'brier_flat_time_reversed':float(brier_score(1-perfect,t[:,0],d,2)),
       'cindex_column_time_perfect':float(c_index(perfect,t,d,2)),
       'cindex_flat_time_perfect':float(c_index(perfect,t[:,0],d,2))}
assert out['brier_column_time_perfect']==0.5
assert out['brier_flat_time_perfect']==0.0
assert out['brier_flat_time_reversed']==1.0
assert out['cindex_column_time_perfect']==0.5
assert out['cindex_flat_time_perfect']==1.0
print(json.dumps(out,indent=2))
