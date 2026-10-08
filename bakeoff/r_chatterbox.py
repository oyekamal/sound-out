import time,json,sys,torch,numpy as np,soundfile as sf,os
sys.path.insert(0,'.')
from common import *
t=time.time()
from chatterbox.tts_turbo import ChatterboxTurboTTS
m=ChatterboxTurboTTS.from_pretrained(device='cpu'); print('load',round(time.time()-t,1),flush=True)
def say(txt):
    torch.manual_seed(18)
    return m.generate(txt).squeeze().cpu().numpy()
os.makedirs('raw/chatterbox',exist_ok=True); log={}
for it in items():
    if it['kind']=='iso':
        a,dt=timed(say,it['carrier']+'.'); sf.write(f"raw/chatterbox/{it['id']}__carrier.wav",
            __import__('scipy.signal',fromlist=['x']).resample_poly(a,SR,m.sr) if m.sr!=SR else a,SR)
    else:
        a,dt=timed(say,it['text']+'.'); save(f"out/chatterbox/{it['id']}.wav",norm(a,m.sr))
    log[it['id']]=dt; print(it['id'],round(dt,1),flush=True)
json.dump(log,open('raw/chatterbox_times.json','w'))
