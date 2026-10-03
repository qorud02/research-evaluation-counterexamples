"""Inspect all six model permutations before and after a model-aligned rank repair.
The comparator preserves benchmark order and covers tie-free higher-is-better scores.
"""
from pathlib import Path
import ast
import hashlib
import itertools
import json
import urllib.request
import numpy as np

url = "https://raw.githubusercontent.com/liangzid/ArxivRoll/709b0c5738b1710a4ac6988d70b32ffb1d21458b/rs.py"
expected_hash = "77dcd6558602b24b51ebc035c936be6c09a7b2d0b77527700149f3fcef021237"
with urllib.request.urlopen(url, timeout=45) as response:
    source = response.read()
assert hashlib.sha256(source).hexdigest() == expected_hash
wanted = {"getRSI_absolute", "_getRelSorting", "getRSIRelative4AllModels"}
functions = [node for node in ast.parse(source.decode("utf-8-sig")).body if isinstance(node, ast.FunctionDef) and node.name in wanted]
namespace = {"np": np}
exec(compile(ast.Module(body=functions,type_ignores=[]), url, "exec"), namespace)
public = np.array([[.9,.6],[.7,.8],[.5,.4]])
private = np.array([[.5,.8],[.9,.4],[.7,.6]])

def evaluate(a,b):
    return np.asarray(namespace["getRSIRelative4AllModels"](np.stack([a,b],axis=2).tolist(),a.tolist(),a.tolist()))

def check_all():
    baseline = evaluate(public,private)
    rows=[]
    for values in itertools.permutations(range(3)):
        permutation=np.array(values)
        restored=evaluate(public[permutation],private[permutation])[np.argsort(permutation)]
        rows.append({"permutation":permutation.tolist(),"restored":restored.tolist(),"matches_baseline":bool(np.allclose(restored,baseline))})
    return {"baseline":baseline.tolist(),"permutations":rows}

released=check_all()
# Best score has rank 1; this comparator covers tie-free scores.
namespace["_getRelSorting"] = lambda array: np.argsort(np.argsort(-array,axis=0),axis=0)+1
corrected=check_all()
assert sum(row["matches_baseline"] for row in released["permutations"]) == 1
assert all(row["matches_baseline"] for row in corrected["permutations"])
print(json.dumps({"source_url":url,"source_sha256":expected_hash,"released":released,"corrected":corrected},indent=2))
