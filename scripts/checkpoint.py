"""Save or restore a verified project checkpoint without credentials or real imports."""
import argparse,hashlib,json,pathlib,zipfile
root=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('action',choices=['save','restore']);p.add_argument('archive');a=p.parse_args();archive=pathlib.Path(a.archive).resolve()
def allowed(n):
 return n in ['state.json','storyboard.json'] or (n.startswith(('assets/','renders/')) and not n.endswith('.tmp.mp4'))
if a.action=='save':
 files={str(f.relative_to(root)):f.read_bytes() for d in ['assets','renders'] for f in (root/d).rglob('*') if f.is_file() and allowed(str(f.relative_to(root)))}
 for n in ['state.json','storyboard.json']:files[n]=(root/n).read_bytes()
 manifest={'version':1,'sha256':{n:hashlib.sha256(b).hexdigest() for n,b in files.items()}}
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for n,b in files.items():z.writestr(n,b)
  z.writestr('checkpoint.json',json.dumps(manifest))
else:
 with zipfile.ZipFile(archive) as z:
  m=json.loads(z.read('checkpoint.json'));files={}
  for n,h in m['sha256'].items():
   dest=(root/n).resolve()
   if not dest.is_relative_to(root) or not allowed(n):raise ValueError('Unsafe checkpoint path')
   b=z.read(n)
   if hashlib.sha256(b).hexdigest()!=h:raise ValueError('Checksum mismatch: '+n)
   files[n]=b
  if (root/'state.json').exists():raise ValueError('Restore only into fresh workspace; state already exists')
  for n,b in files.items():
   dest=root/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
print(a.action+' OK: '+str(archive))
