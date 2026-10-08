import time,json,numpy as np
from piper import PiperVoice
from common import *
from build_testset import cmu,mis
v=PiperVoice.load('models/piper/en_US-lessac-medium.onnx')
def esp(ph):
    for a,b in [('A','eɪ'),('I','aɪ'),('O','oʊ'),('W','aʊ'),('Y','ɔɪ'),('ʤ','dʒ'),('ʧ','tʃ')]: ph=ph.replace(a,b)
    return ph
def say(ph):
    ids=v.phonemes_to_ids(list(esp(ph)))
    a=v.phoneme_ids_to_audio(ids)
    a=np.asarray(a,dtype=np.float32)
    if a.dtype!=np.float32 or np.abs(a).max()>5: a=a/32768.0
    return a
os.makedirs('raw/piper',exist_ok=True); log={}
for it in items():
    a,dt=timed(say,it['ph']); sr=v.config.sample_rate
    save(f"out/piper/{it['id']}"+("__direct" if it['kind']=='iso' else '')+".wav",norm(a,sr)); log[it['id']]=dt
    if it['kind']=='iso':
        c=say(mis(cmu[it['carrier']])); 
        from scipy.signal import resample_poly
        sf.write(f"raw/piper/{it['id']}__carrier.wav",resample_poly(c,160,147),24000)
print({k:round(x,2) for k,x in log.items()}); json.dump(log,open('raw/piper_times.json','w'))
