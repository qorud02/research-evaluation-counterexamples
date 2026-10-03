# Source: https://github.com/aailab-kaist/DBAE/blob/533f5648a3a1ca419c402c656e305536267c14c8/eval_reconstruction.py
"""NumPy translation of the audited SSIM arithmetic; no model/source module imported.
Matches conv2d groups=channel, 11x11 Gaussian, zero padding and per-image averaging.
Tests synthetic arrays; does not recompute published model results.
"""
import numpy as np
def convolve(x,kernel,mode=None,cval=0):
    k=kernel[0,0]; padded=np.pad(x,((0,0),(0,0),(5,5),(5,5))); out=np.zeros_like(x)
    for i in range(11):
        for j in range(11):out += k[i,j]*padded[:,:,i:i+x.shape[-2],j:j+x.shape[-1]]
    return out
import json

def ssim_axes(x,y):
    g=np.exp(-(np.arange(11)-5)**2/(2*1.5**2)); g=g/g.sum()
    kernel=np.outer(g,g)[None,None,:,:]
    mu1=convolve(x,kernel,mode='constant',cval=0.0);mu2=convolve(y,kernel,mode='constant',cval=0.0)
    a=mu1**2;b=mu2**2;ab=mu1*mu2
    v1=convolve(x*x,kernel,mode='constant',cval=0.0)-a
    v2=convolve(y*y,kernel,mode='constant',cval=0.0)-b
    cov=convolve(x*y,kernel,mode='constant',cval=0.0)-ab
    return float(np.mean(((2*ab+0.01**2)*(2*cov+0.03**2))/((a+b+0.01**2)*(v1+v2+0.03**2))))

rng=np.random.default_rng(20261002)
x=rng.uniform(0,1,(1,128,128,3))
y=x.copy(); y[:,40:88,:,:]=np.roll(y[:,40:88,:,:],1,axis=2)
r={'source_shape':'NHWC [1,128,128,3]','published_call_ssim':ssim_axes(x,y),'correct_nchw_ssim':ssim_axes(x.transpose(0,3,1,2),y.transpose(0,3,1,2)), 'published_call_after_HW_transpose':ssim_axes(x.transpose(0,2,1,3),y.transpose(0,2,1,3)), 'correct_nchw_after_HW_transpose':ssim_axes(x.transpose(0,3,2,1),y.transpose(0,3,2,1))}
print(json.dumps(r,indent=2))
