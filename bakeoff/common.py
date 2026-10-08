import json,os,subprocess,time,numpy as np,soundfile as sf,pyloudnorm as pyln
from scipy.signal import resample_poly
SR=24000; HERE=os.path.dirname(os.path.abspath(__file__))
def items(): return json.load(open(HERE+'/testset.json'))
def norm(x,sr=SR,target=-18.0):
    x=np.asarray(x,dtype=np.float64)
    if x.ndim>1: x=x.mean(1)
    if sr!=SR:
        from math import gcd
        g=gcd(sr,SR); x=resample_poly(x,SR//g,sr//g)
    # trim silence edges
    th=10**(-45/20); idx=np.where(np.abs(x)>th)[0]
    if len(idx): x=x[max(0,idx[0]-int(.02*SR)):idx[-1]+int(.05*SR)]
    pad=np.concatenate([x,np.zeros(max(0,int(1.0*SR)-len(x)))])
    L=pyln.Meter(SR).integrated_loudness(pad)
    if not np.isfinite(L): return x
    y=x*10**((target-L)/20)
    pk=np.abs(y).max()
    if pk>0.97: y=y*0.97/pk   # peak-limit by gain only; may land a little under -18 LUFS on peaky clips
    return y.astype(np.float32)
def save(path,x):
    os.makedirs(os.path.dirname(path),exist_ok=True); sf.write(path,x,SR,subtype='PCM_16')
def timed(f,*a):
    t=time.time(); r=f(*a); return r,time.time()-t
