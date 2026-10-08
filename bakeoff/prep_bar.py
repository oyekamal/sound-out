import subprocess,soundfile as sf,os
from common import *
APP=HERE+'/../app/public/audio/'
for it in items():
    src=APP+it['bar']['id']+'.ogg'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',src,'-ar',str(SR),'-ac','1','/tmp/_b.wav'],check=True)
    x,sr=sf.read('/tmp/_b.wav'); save(f"{HERE}/out/elevenlabs/{it['id']}.wav",norm(x,sr))
print('ok')
