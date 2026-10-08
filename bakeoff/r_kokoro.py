import glob,time,torch,sys,json
from kokoro import KModel,KPipeline
from common import *
t0=time.time()
m=KModel(repo_id='hexgrad/Kokoro-82M').eval()
vp=glob.glob(os.path.expanduser('~/.cache/huggingface/hub/models--hexgrad--Kokoro-82M/snapshots/*/voices/af_heart.pt'))[0]
voice=torch.load(vp,weights_only=True)
print('load',time.time()-t0)
def say(ph):
    with torch.no_grad(): out=KPipeline.infer(m,ph,voice,speed=0.9)
    return out.audio.numpy()
log={}
for it in items():
    if it['kind']=='iso':
        a,dt=timed(say,it['ph']); save(f"out/kokoro/{it['id']}__direct.wav",norm(a,24000))
        c=[x for x in items() if 0]  # carrier
        from_ph=None
    else:
        a,dt=timed(say,it['ph']); save(f"out/kokoro/{it['id']}.wav",norm(a,24000))
    log[it['id']]=dt; print(it['id'],round(dt,2),flush=True)
# carriers as raw (un-normalised) audio for alignment
import numpy as np
os.makedirs('raw/kokoro',exist_ok=True)
for it in items():
    if it['kind']=='iso':
        w=it['carrier']; from build_testset import cmu,mis
        a=say(mis(cmu[w])); sf.write(f"raw/kokoro/{it['id']}__carrier.wav",a,24000)
json.dump(log,open('raw/kokoro_times.json','w'))
