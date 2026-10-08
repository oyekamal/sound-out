"""Indicative phone-error check: greedy CTC decode with the espeak phoneme recogniser vs the CMUdict target. Not a quality score."""
import sys,json,glob,re,torch,numpy as np,soundfile as sf
from align import *
iv={v:k for k,v in V.items()}
A=dict(AA='ɑ',AE='æ',AH='ʌ',AO='ɔ',AW='aʊ',AY='aɪ',EH='ɛ',ER='ɜ',EY='eɪ',IH='ɪ',IY='i',OW='oʊ',OY='ɔɪ',UH='ʊ',UW='u',B='b',CH='tʃ',D='d',DH='ð',F='f',G='ɡ',HH='h',JH='dʒ',K='k',L='l',M='m',N='n',NG='ŋ',P='p',R='ɹ',S='s',SH='ʃ',T='t',TH='θ',V='v',W='w',Y='j',Z='z')
def norm_p(s):  # collapse near-equivalents so we do not punish dialect noise
    s=s.replace('ː','').replace('ʰ','').replace('ɐ','ʌ').replace('ə','ʌ').replace('ɚ','ɜ').replace('ɝ','ɜ').replace('ᵻ','ɪ').replace('ɫ','l').replace('ɾ','t').replace('ɑ','ɑ').replace('ɒ','ɑ').replace('g','ɡ').replace('ʧ','tʃ').replace('ʤ','dʒ')
    return [c for c in re.findall(r'tʃ|dʒ|aʊ|aɪ|eɪ|oʊ|ɔɪ|.',s) if c.strip() and c not in 'ˈˌ ']
def ed(a,b):
    d=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        p,d[0]=d[0],i
        for j,y in enumerate(b,1): p,d[j]=d[j],min(d[j]+1,d[j-1]+1,p+(x!=y))
    return d[-1]
def dec(x24):
    x16=resample_poly(x24,2,3); lp=logp(x16); ids=lp.argmax(-1); out=[];prev=-1
    for i in ids:
        if i!=prev and i!=V.get('<pad>',0): out.append(iv[int(i)])
        prev=i
    return norm_p(''.join(out))
res={}
for m in ['elevenlabs','kokoro','chatterbox','piper','styletts2']:
    e=n=0;dets=[]
    for it in items():
        if it['kind']=='iso': continue
        x,sr=sf.read(f"out/{m}/{it['id']}.wav"); got=dec(x); exp=norm_p(''.join(A[re.sub(r'\d','',p)] for p in it['arpa']))
        k=ed(got,exp); e+=k; n+=len(exp); dets.append((it['text'],''.join(got),''.join(exp)))
    res[m]=dict(per=round(e/n,3),n=n); print(m,res[m],[d for d in dets if d[1]!=d[2]][:6],flush=True)
json.dump(res,open('raw/per.json','w'))
