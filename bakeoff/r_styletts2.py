import time,json,sys,torch,numpy as np,soundfile as sf,os
from scipy.signal import resample_poly
sys.path.insert(0,'.')
from common import *
from build_testset import cmu,mis
t=time.time()
_tl=torch.load
torch.load=lambda *a,**k:_tl(*a,**{**k,"weights_only":False})  # official yl4579 checkpoint pickles getattr; trusted source, noted in REPORT
from styletts2 import tts
m=tts.StyleTTS2()
print('load',round(time.time()-t,1),flush=True)
class Fake:
    cur=''
    def phonemize(self,text): return Fake.cur
m.phoneme_converter=Fake()
def esp(ph):
    for a,b in [('A','eɪ'),('I','aɪ'),('O','oʊ'),('W','aʊ'),('Y','ɔɪ')]: ph=ph.replace(a,b)
    return ph
ref=m.compute_style(__import__('cached_path').cached_path(tts.DEFAULT_TARGET_VOICE_URL))
def say(ph):
    Fake.cur=esp(ph); torch.manual_seed(18); return m.inference('x',ref_s=ref,diffusion_steps=5,alpha=0.3,beta=0.7)
os.makedirs('raw/styletts2',exist_ok=True); log={}
for it in items():
    a,dt=timed(say,it['ph']); save(f"out/styletts2/{it['id']}"+("__direct" if it['kind']=='iso' else '')+".wav",norm(a,24000)); log[it['id']]=dt
    if it['kind']=='iso': sf.write(f"raw/styletts2/{it['id']}__carrier.wav",say(mis(cmu[it['carrier']])),24000)
    print(it['id'],round(dt,2),flush=True)
json.dump(log,open('raw/styletts2_times.json','w'))
