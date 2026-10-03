# Audited Rmd: https://github.com/OpportunityInsights/Experimental-Selection-Correction-Replication-Code/blob/a5fc1167d4c28477920d0d10b9bd35adf9e614a1/code/ESC_main_code_ext.Rmd
"""Independent NumPy implementation of the published Rmd paired-index bootstrap.
Synthetic inputs only: no estimate here is the authors' private-data estimate.
No downloaded code is executed.
"""
import numpy as np
import json
rng=np.random.default_rng(20261002)
n=600; B=3000
d1=rng.binomial(1,.5,n).astype(float); z1=d1+rng.normal(size=n)
d2=rng.binomial(1,.5,n).astype(float); u=rng.normal(size=n)
z2=d2+u; y=.2*d2+u+rng.normal(size=n)
exp=np.column_stack([d1,z1]); obs=np.column_stack([d2,z2,y])
def fit(e,o):
    b=np.linalg.lstsq(np.column_stack([np.ones(len(e)),e[:,0]]),e[:,1],rcond=None)[0][1]
    X=np.column_stack([np.ones(len(o)),o[:,0],o[:,1]-b*o[:,0]])
    return float(np.linalg.lstsq(X,o[:,2],rcond=None)[0][1])
# Influences used only to permute an unchanged sample; sorting cannot change OLS.
xe=np.column_stack([np.ones(n),exp[:,0]])
be=np.linalg.lstsq(xe,exp[:,1],rcond=None)[0]
ife=(xe@np.linalg.inv(xe.T@xe)[:,1])*(exp[:,1]-xe@be)
xo=np.column_stack([np.ones(n),obs[:,0],obs[:,1]])
bo=np.linalg.lstsq(xo,obs[:,2],rcond=None)[0]
target=np.array([0.,1.,be[1]])
ifo=(xo@np.linalg.inv(xo.T@xo)@target)*(obs[:,2]-xo@bo)
io=np.argsort(ifo); ie=np.argsort(ife)
obs_sort=obs[io]
out={"seed":20261002,"n_each":n,"bootstrap_draws":B,"synthetic":True,"downloaded_R_execution":False,"tests":[]}
for label,e in [('original',exp),('sorted_same_direction',exp[ie]),('sorted_reverse_direction',exp[ie[::-1]])]:
    o=obs if label=='original' else obs_sort
    paired=[]; separate=[]
    draws=np.random.default_rng(991)
    for b in range(B):
        i=draws.integers(0,n,n); j=draws.integers(0,n,n)
        paired.append(fit(e[i],o[i]))
        separate.append(fit(e[i],o[j]))
    out['tests'].append({'row_order':label,'point_estimate':fit(e,o),'paired_bootstrap_se':float(np.std(paired,ddof=1)),'independent_bootstrap_se':float(np.std(separate,ddof=1))})
print(json.dumps(out,indent=2))
