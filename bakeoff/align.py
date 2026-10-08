"""Extract an isolated phone from a carrier-word render: CTC forced alignment with the phoneme recogniser
facebook/wav2vec2-lv-60-espeak-cv-ft (cached locally), own numpy Viterbi."""
import sys,glob,json,torch,numpy as np,soundfile as sf
from transformers import Wav2Vec2ForCTC
from common import *
P=glob.glob(os.path.expanduser('~/.cache/huggingface/hub/models--facebook--wav2vec2-lv-60-espeak-cv-ft/snapshots/*'))[0]
V=json.load(open(P+'/vocab.json')); M=Wav2Vec2ForCTC.from_pretrained(P).eval()
IPA=dict(s='s',æ='æ',t='t',p='p',ɪ='ɪ',ɑ='ɑ',m='m',n='n',d='d',ɡ='ɡ',b='b',ɹ='ɹ')
ARPA=dict(S='s',AE='æ',T='t',P='p',IH='ɪ',AA='ɑ',M='m',N='n',D='d',G='ɡ',B='b',R='ɹ')
def logp(x16):
    x=(x16-x16.mean())/(x16.std()+1e-7)
    with torch.no_grad(): return torch.log_softmax(M(torch.tensor(x,dtype=torch.float32)[None]).logits[0],-1).numpy()
def viterbi(lp,ids,blank=0):
    L=[blank]; 
    for i in ids: L+= [i,blank]
    T,S=len(lp),len(L); NEG=-1e9; d=np.full((T,S),NEG); b=np.zeros((T,S),int)
    d[0,0]=lp[0,L[0]]; d[0,1]=lp[0,L[1]]
    for t in range(1,T):
        for s in range(S):
            c=[(d[t-1,s],s)]
            if s>0: c.append((d[t-1,s-1],s-1))
            if s>1 and L[s]!=blank and L[s]!=L[s-2]: c.append((d[t-1,s-2],s-2))
            v,a=max(c); d[t,s]=v+lp[t,L[s]]; b[t,s]=a
    s=S-1 if d[-1,S-1]>d[-1,S-2] else S-2; path=[]
    for t in range(T-1,-1,-1): path.append(s); s=b[t,s]
    return path[::-1],L
def phone_span(x24,phones,idx):
    from math import gcd
    x16=resample_poly(x24,2,3)
    lp=logp(x16); ids=[V[p] for p in phones]; blank=V.get('<pad>',0)
    path,L=viterbi(lp,ids,blank)
    first=[None]*len(phones)
    for t,s in enumerate(path):
        if s%2==1 and first[s//2] is None: first[s//2]=t
    st=first[idx]; en=first[idx+1] if idx+1<len(phones) else len(lp)
    f=len(x16)/len(lp)/16000   # seconds per frame
    s0=0 if idx==0 else st*f; s1=en*f
    return s0,s1
def refine(x,letter,idx,s0,s1):
    # CTC spikes are late, so an onset span runs into the vowel. Cut onsets s/t/p where voicing (<500 Hz share) starts;
    # other onsets keep 60% of the span. Vowels/finals keep the span.
    if idx!=0 or letter in 'aio': return s1
    seg=x[int(s0*SR):int(s1*SR)]; h=int(.01*SR)
    if letter in 's':
        for k in range(0,len(seg)-2*h,h//2):
            w=seg[k:k+2*h]*np.hanning(2*h); S=np.abs(np.fft.rfft(w))**2; f=np.fft.rfftfreq(2*h,1/SR)
            if S[f<500].sum()/(S.sum()+1e-12)>0.5 and np.sqrt((w**2).mean())>0.01: return s0+max(k/SR,0.06)
        return s0+0.6*(s1-s0)
    cap={'p':.12,'t':.12,'d':.12,'g':.12,'b':.12}.get(letter,.25)
    return s0+min(cap,0.6*(s1-s0))
if __name__=='__main__':
    model=sys.argv[1]; res={}
    for it in items():
        if it['kind']!='iso': continue
        x,sr=sf.read(f"raw/{model}/{it['id']}__carrier.wav"); assert sr==24000
        phones=[ARPA[re.sub(r'\d','',p)] for p in it['carrier_arpa']] if (re:=__import__('re')) else 0
        s0,s1=phone_span(x,phones,it['carrier_idx'])
        s1=refine(x,it['text'],it['carrier_idx'],s0,s1)
        seg=x[int(s0*SR):int(s1*SR)+int(.01*SR)]
        # fade edges
        n=int(.008*SR); seg=seg.copy(); seg[:n]*=np.linspace(0,1,n); seg[-n:]*=np.linspace(1,0,n)
        save(f"out/{model}/{it['id']}__carrier.wav",norm(seg,SR)); res[it['id']]=round(s1-s0,3)
        print(it['id'],it['carrier'],phones,round(s0,2),round(s1,2),flush=True)
    json.dump(res,open(f'raw/{model}_carrier_durs.json','w'))
