import argparse,json,pathlib,hashlib,subprocess,os
from PIL import Image,ImageDraw
import imageio_ffmpeg
ROOT=pathlib.Path(__file__).resolve().parents[1]
def save(p,d):
 t=p.with_suffix('.tmp');t.write_text(json.dumps(d,ensure_ascii=False,indent=2));t.replace(p)
def run(c): subprocess.run(c,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
p=argparse.ArgumentParser();p.add_argument('action',choices=['demo','render']);p.add_argument('--shot');p.add_argument('--redo',action='store_true');a=p.parse_args()
ff=imageio_ffmpeg.get_ffmpeg_exe(); assets=ROOT/'assets';assets.mkdir(exist_ok=True);out=ROOT/'renders';out.mkdir(exist_ok=True)
if a.action=='demo':
 im=Image.new('RGB',(960,540),'#a9d9ee');d=ImageDraw.Draw(im);d.rectangle((0,360,960,540),fill='#75996b');d.ellipse((720,40,820,140),fill='#ffe5a0');im.save(assets/'background.png')
 fg=Image.new('RGBA',(960,540));d=ImageDraw.Draw(fg);d.ellipse((350,210,490,380),fill='#d59e76');d.ellipse((365,160,400,260),fill='#d59e76');d.ellipse((440,160,475,260),fill='#d59e76');d.ellipse((390,265,400,275),fill='black');fg.save(assets/'foreground.png')
 im=im.convert('RGBA');im.alpha_composite(fg);im.convert('RGB').save(assets/'page.png')
 save(ROOT/'storyboard.json',{'version':'0.1','rights':{'local_adaptation':True,'cloud_storage':False,'video_service_upload':False,'evidence':'Original geometric artwork created by pipeline.py'},'shots':[{'id':'S01','duration':15,'mode':'pan','source':'assets/page.png','review':'approved'},{'id':'S02','duration':15,'mode':'layers','source':'assets/background.png','foreground':'assets/foreground.png','review':'approved'}]})
m=json.loads((ROOT/'storyboard.json').read_text());assert m['rights']['local_adaptation'],'Missing adaptation permission';assert 30<=sum(s['duration'] for s in m['shots'])<=60
statep=ROOT/'state.json';state=json.loads(statep.read_text()) if statep.exists() else {}; fps=24
for s in m['shots']:
 assert s['review'] in ['draft','approved','changes_requested']; assert s['id'].isalnum()
 if a.shot and s['id']!=a.shot:continue
 if s['review']!='approved':raise ValueError('Shot requires approval: '+s['id'])
 sources=[ROOT/s['source']]+([ROOT/s['foreground']] if s['mode']=='layers' else [])
 key=hashlib.sha256(json.dumps(s,sort_keys=True).encode()+b''.join(x.read_bytes() for x in sources)).hexdigest();dest=out/(s['id']+'.mp4')
 if not a.redo and state.get(s['id'],{}).get('hash')==key and dest.exists() and state[s['id']].get('output_hash')==hashlib.sha256(dest.read_bytes()).hexdigest():continue
 n=int(s['duration']*fps);c=[ff,'-y','-loop','1','-i',str(sources[0])]
 if s['mode']=='layers':
  c+=['-loop','1','-i',str(sources[1]),'-filter_complex',"[0:v]scale=960:540[b];[b][1:v]overlay=x='20*sin(t/6)':y=0:eval=frame,scale=640:360[v]",'-map','[v]']
 else:c+=['-vf',f"scale=960:540,zoompan=z='1+0.08*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=640x360:fps={fps}"]
 temp=out/(s['id']+'.tmp.mp4');c+=['-t',str(s['duration']),'-r',str(fps),'-an','-c:v','libx264','-pix_fmt','yuv420p',str(temp)];run(c);temp.replace(dest);state[s['id']]={'hash':key,'output_hash':hashlib.sha256(dest.read_bytes()).hexdigest(),'status':'rendered','review':'approved'};save(statep,state)
if not a.shot and all((out/(s['id']+'.mp4')).exists() and state.get(s['id'],{}).get('status')=='rendered' for s in m['shots']):
 # Re-run render without --shot before final assembly after storyboard changes.
 listing=out/'concat.txt';listing.write_text(''.join("file '"+s['id']+".mp4'\n" for s in m['shots']));run([ff,'-y','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(out/'preview.mp4')])
print(json.dumps(state,indent=2))
