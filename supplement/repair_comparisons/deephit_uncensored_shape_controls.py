"""Positive controls for the uncensored Dynamic-DeepHit Brier shape repair.
Fetches one pinned original source; the source file is not redistributed.
This experiment covers 24 synthetic conditions and two rejected input contracts.
"""
from pathlib import Path
import ast
import hashlib
import json
import platform
import sys
import urllib.request
import numpy as np

URL = "https://raw.githubusercontent.com/chl8856/Dynamic-DeepHit/b2e208f65233405079a462b703a94556ad30d1f4/utils_eval.py"
SHA256 = "5bdef36df094af8eae29c4c7801933d0e559029efaefb9edae5927c2e13db010"
with urllib.request.urlopen(URL,timeout=45) as response:
    source=response.read()
assert hashlib.sha256(source).hexdigest()==SHA256
functions=[node for node in ast.parse(source.decode("utf-8-sig")).body if isinstance(node,ast.FunctionDef) and node.name=="brier_score"]
assert len(functions)==1
namespace={"np":np}
exec(compile(ast.Module(body=functions,type_ignores=[]),URL,"exec"),namespace)
released=namespace["brier_score"]

def checked_shape_brier(predictions,times,events,horizon):
    predictions=np.asarray(predictions,dtype=float)
    times=np.asarray(times,dtype=float)
    events=np.asarray(events)
    if times.ndim==2 and times.shape[1]==1:
        times=times[:,0]
    elif times.ndim!=1:
        raise ValueError("times must be a flat vector or a single-column array")
    if predictions.ndim!=1 or events.ndim!=1:
        raise ValueError("predictions and events must be flat vectors")
    if not (len(predictions)==len(times)==len(events)):
        raise ValueError("observation counts must agree")
    if len(times)==0:
        raise ValueError("at least one observation is required")
    return float(released(predictions,times,events,horizon))

rows=[]
for n in (2,3,5,10):
    times=np.arange(1,2*n,2,dtype=float)
    events=np.ones(n,dtype=int)
    # Both horizons have patients on each side. At n=2, different horizons
    # necessarily induce the same split between these two distinct times.
    for horizon_label,horizon in (("early",1),("late",2*n-2)):
        target=np.array([float(time<=horizon) for time in times])
        assert 0<target.sum()<n
        for mode in ("perfect","reversed","constant"):
            predictions=target.copy() if mode=="perfect" else 1-target if mode=="reversed" else np.full(n,.25)
            # Independent mathematical oracle over paired patient records.
            oracle=float(sum((float(pred)-float(truth))**2 for pred,truth in zip(predictions,target))/n)
            original=float(released(predictions,times[:,None],events,horizon))
            repaired=checked_shape_brier(predictions,times[:,None],events,horizon)
            analytic_broadcast=float(np.mean(predictions**2)-2*np.mean(predictions)*np.mean(target)+np.mean(target))
            assert np.isclose(original,analytic_broadcast,atol=1e-12,rtol=0)
            rows.append({"n":n,"times":times.tolist(),"events":events.tolist(),"horizon_label":horizon_label,"horizon":horizon,"prediction_mode":mode,"predictions":predictions.tolist(),"target":target.tolist(),"oracle":oracle,"original":original,"repaired":repaired,"analytic_broadcast":analytic_broadcast,"original_matches_oracle":bool(np.isclose(original,oracle,atol=1e-12,rtol=0)),"repaired_matches_oracle":bool(np.isclose(repaired,oracle,atol=1e-12,rtol=0))})

rejections=[]
invalid=[("multi_column_times",np.array([1.,0.]),np.array([[1.,2.],[3.,4.]]),np.ones(2,dtype=int)),("mismatched_observation_count",np.array([1.,0.]),np.array([[1.],[3.],[5.]]),np.ones(2,dtype=int))]
for label,predictions,times,events in invalid:
    try:
        checked_shape_brier(predictions,times,events,2)
    except ValueError as error:
        rejections.append({"case":label,"rejected":True,"error":str(error)})
    else:
        rejections.append({"case":label,"rejected":False})
summary={"valid_conditions":len(rows),"original_oracle_mismatches":sum(not row["original_matches_oracle"] for row in rows),"repaired_oracle_mismatches":sum(not row["repaired_matches_oracle"] for row in rows),"constant_positive_controls":sum(row["prediction_mode"]=="constant" and row["original_matches_oracle"] for row in rows),"unsupported_inputs":len(rejections),"unsupported_inputs_rejected":sum(row["rejected"] for row in rejections)}
assert summary=={"valid_conditions":24,"original_oracle_mismatches":16,"repaired_oracle_mismatches":0,"constant_positive_controls":8,"unsupported_inputs":2,"unsupported_inputs_rejected":2}
result={"source_url":URL,"source_sha256":SHA256,"python":sys.version,"platform":platform.platform(),"numpy":np.__version__,"scope":"uncensored one-event Brier score with flat predictions/events and flat-or-single-column times; no censoring/IPCW or paper-table repair","tolerance":1e-12,"summary":summary,"conditions":rows,"unsupported_inputs":rejections,"analytic_relation":"For all events=1, broadcast Brier=mean(p^2)-2*mean(p)*mean(y)+mean(y); paired Brier=mean(p^2)-2*mean(p*y)+mean(y). Difference is 2*Cov_population(p,y)."}
output=Path(__file__).with_name("deephit_uncensored_shape_controls_result.json")
output.write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({"output":str(output),"summary":summary},indent=2))
