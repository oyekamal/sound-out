import json,re
R='../content/'
cmu={}
for ln in open(R+'cmudict/cmudict.dict'):
    p=ln.split('#')[0].split()
    if p and '(' not in p[0]: cmu[p[0]]=p[1:]
A=json.load(open(R+'audio_index.json'))['clips']
real="sat mug chunk full cat dog win quit fox hill what said".split()  # ship/think/queen/wind/read/pull have no shipped River clip
made="tas mip gid cak nuzz zox quab wux".split()
iso="s a t p i o m n d g b r".split()
carrier=dict(s='sat',a='sat',t='tap',p='pat',i='sit',o='dot',m='map',n='nap',d='dad',g='gap',b='bat',r='rat')
carrier_pos=dict(s=0,a=1,t=0,p=0,i=1,o=1,m=0,n=0,d=0,g=0,b=0,r=0)
# misaki (Kokoro) phoneme set
M=dict(AA='ɑ',AE='æ',AH='ʌ',AO='ɔ',AW='W',AY='I',EH='ɛ',ER='ɜɹ',EY='A',IH='ɪ',IY='i',OW='O',OY='Y',UH='ʊ',UW='u',
 B='b',CH='ʧ',D='d',DH='ð',F='f',G='ɡ',HH='h',JH='ʤ',K='k',L='l',M='m',N='n',NG='ŋ',P='p',R='ɹ',S='s',SH='ʃ',T='t',TH='θ',V='v',W='w',Y='j',Z='z',ZH='ʒ')
def mis(arpa,stress=True):
    out=[];first=True
    for p in arpa:
        b=re.sub(r'\d','',p)
        if b in('AA','AE','AH','AO','AW','AY','EH','ER','EY','IH','IY','OW','OY','UH','UW') and first and stress:
            out.append('ˈ');first=False
        out.append(M[b])
    return ''.join(out)
# made-up words have no CMUdict entry: hand arpabet from letters
L=dict(a='AE',e='EH',i='IH',o='AA',u='AH',c='K',q='K',x=None,j='JH',y='Y',z='Z',w='W')
def guess(w):
    out=[];i=0
    while i<len(w):
        c=w[i]
        if w[i:i+2]=='qu': out+=['K','W'];i+=2;continue
        if c=='x': out+=['K','S'];i+=1;continue
        if i+1<len(w) and w[i+1]==c and c not in 'aeiou': i+=1;continue  # doubled consonant
        out.append(L.get(c) or c.upper().replace('H','HH') if c in 'aeiou' else (L.get(c) or c.upper()));i+=1
    return out
items=[]
for w in real:
    a=cmu[w]; items.append(dict(id='w_'+w,kind='real',text=w,arpa=a,ph=mis(a),bar=A.get('w:'+w) or A.get(w)))
for w in made:
    a=guess(w); items.append(dict(id='m_'+w,kind='made',text=w,arpa=a,ph=mis(a),bar=A.get('w:'+w) or A.get(w)))
I=dict(s='s',a='æ',t='t',p='p',i='ɪ',o='ɑ',m='m',n='n',d='d',g='ɡ',b='b',r='ɹ')
for s in iso:
    items.append(dict(id='s_'+s,kind='iso',text=s,ph=I[s],carrier=carrier[s],carrier_idx=carrier_pos[s],carrier_arpa=cmu[carrier[s]],bar=A.get('ph:'+s)))
#print([ (i['id'],i['ph'],i['bar']) for i in items if i['kind']!='iso'])
#print([i['id'] for i in items if not i['bar']])
if __name__=="__main__": json.dump(items,open("testset.json","w"),indent=1,ensure_ascii=False)
