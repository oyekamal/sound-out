import json,os,glob,random
T=json.load(open('testset.json')); names={'elevenlabs':'ElevenLabs River (the bar)','kokoro':'Kokoro-82M af_heart','piper':'Piper lessac-medium','chatterbox':'Chatterbox Turbo','styletts2':'StyleTTS2 LJSpeech'}
data=[]
for it in T:
    v=[]
    for m in names:
        for f in sorted(glob.glob(f'out/{m}/{it["id"]}.wav')+glob.glob(f'out/{m}/{it["id"]}__*.wav')):
            meth=f.split('__')[1][:-4] if '__' in f else ''
            v.append(dict(model=names[m]+(f' [{meth}]' if meth else ''),file=f))
    data.append(dict(id=it['id'],label={'real':'real word','made':'made-up word','iso':'isolated sound'}[it['kind']]+': '+it['text'],ph=it['ph'],variants=v))
html='''<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Sound Out TTS bakeoff</title>
<style>:root{--bg:#fff;--fg:#1d2330;--mut:#6b7385;--ln:#dde1ea;--ac:#2557d6;--ok:#14803c}@media(prefers-color-scheme:dark){:root{--bg:#12151c;--fg:#e8ebf2;--mut:#98a0b3;--ln:#2a3040;--ac:#7aa2ff;--ok:#4ade80}}
body{background:var(--bg);color:var(--fg);font:16px/1.45 system-ui,sans-serif;margin:0 auto;max-width:860px;padding:16px}h1{font-size:1.3rem}
.it{border:1px solid var(--ln);border-radius:10px;padding:12px;margin:12px 0}.it h2{font-size:1rem;margin:0 0 8px}.it small{color:var(--mut)}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}.v{display:flex;flex-direction:column;align-items:center;gap:4px;min-width:64px}
button{font:inherit;padding:8px 14px;border:1px solid var(--ln);border-radius:8px;background:var(--bg);color:var(--fg);cursor:pointer}button:hover{border-color:var(--ac)}
.lab{font-size:.72rem;color:var(--mut);text-align:center;max-width:110px;min-height:2em}.rev .lab{color:var(--ok)}label{font-size:.8rem}
table{border-collapse:collapse;width:100%;font-size:.9rem}td,th{border:1px solid var(--ln);padding:4px 8px;text-align:left}.top{display:flex;gap:8px;flex-wrap:wrap}</style>
<h1>Sound Out local TTS bakeoff (blind)</h1><p>Press each letter to listen. Pick the one that sounds best for the job (clear, natural, correct sound). Names are hidden until you press Reveal. Picks save in this browser.</p>
<div class=top><button onclick="revealAll()">Reveal all names</button><button onclick="if(confirm('Clear picks?')){localStorage.removeItem('bk_picks');render()}">Clear picks</button></div>
<div id=items></div><h2>Summary</h2><div id=sum></div>
<script>const D=__DATA__;let P={};try{P=JSON.parse(localStorage.getItem('bk_picks')||'{}')}catch(e){}
const seed=(s)=>{let h=2166136261;for(const c of s){h^=c.charCodeAt(0);h=Math.imul(h,16777619)}return()=>(h=Math.imul(h^h>>>15,2246822519)>>>0)/4294967296};
D.forEach(d=>{const r=seed(d.id+'bk1');d.order=d.variants.map((_,i)=>i).sort(()=>r()-.5)});
let cur=null;function play(f){if(cur)cur.pause();cur=new Audio(f);cur.play()}
function save(){try{localStorage.setItem('bk_picks',JSON.stringify(P))}catch(e){}}
function pick(id,m){P[id]=m;save();sum()}
function reveal(id){document.getElementById('it-'+id).classList.add('rev')}
function revealAll(){document.querySelectorAll('.it').forEach(e=>e.classList.add('rev'))}
function render(){const el=document.getElementById('items');el.innerHTML='';D.forEach(d=>{const L='ABCDEFGHIJ';const o=document.createElement('div');o.className='it';o.id='it-'+d.id;
o.innerHTML='<h2>'+d.label+' <small>/'+d.ph+'/</small></h2><div class=row>'+d.order.map((vi,k)=>{const v=d.variants[vi];return '<div class=v><button onclick="play(\\''+v.file+'\\')">'+L[k]+'</button><div class=lab><span class=hid>?</span><span class=shown style="display:none">'+v.model+'</span></div><label><input type=radio name="r-'+d.id+'" '+(P[d.id]===v.model?'checked':'')+' onchange="pick(\\''+d.id+'\\',\\''+v.model.replace(/'/g,"")+'\\')"> best</label></div>'}).join('')+'</div><p><button onclick="reveal(\\''+d.id+'\\')">Reveal</button></p>';el.appendChild(o)});
const st=document.createElement('style');st.textContent='.rev .hid{display:none}.rev .shown{display:inline!important}';document.head.appendChild(st);sum()}
function sum(){const c={};Object.values(P).forEach(m=>c[m]=(c[m]||0)+1);const rows=Object.entries(c).sort((a,b)=>b[1]-a[1]);document.getElementById('sum').innerHTML=rows.length?'<table><tr><th>Model [method]</th><th>Wins</th></tr>'+rows.map(r=>'<tr><td>'+r[0]+'</td><td>'+r[1]+'</td></tr>').join('')+'</table><p>'+Object.keys(P).length+' of '+D.length+' items picked.</p>':'<p>No picks yet.</p>'}
render()</script>'''
open('listen.html','w').write(html.replace('__DATA__',json.dumps(data,ensure_ascii=False)))
print(len(data),sum(len(d['variants']) for d in data))
