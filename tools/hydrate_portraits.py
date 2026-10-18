"""Fetch third-party art for local use; never copy it into public mod sources."""
from pathlib import Path
import json,urllib.request,urllib.parse,concurrent.futures
R=Path(__file__).resolve().parents[1]
BASE='https://raw.githubusercontent.com/Cold-War-Iron-Curtain-Dev-Team/ColdWarIronCurtain/development-branch/Cold War Iron Curtain/gfx/leaders/'
def hydrate(out):
 def fetch(item):
  p=out/item['target'];p.parent.mkdir(parents=True,exist_ok=True)
  if p.exists() and p.read_bytes()[:4]==b'DDS ':return item['id'],True
  try:
   req=urllib.request.Request(urllib.parse.quote(BASE+item['source'],safe=':/'),headers={'User-Agent':'Vietnam1965Mod/0.4'})
   with urllib.request.urlopen(req,timeout=25) as res:data=res.read()
   if data[:4]!=b'DDS ':raise ValueError('Invalid DDS download')
   p.write_bytes(data);return item['id'],True
  except Exception as error:return item['id'],str(error)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(fetch,json.loads((R/'portrait-catalog.json').read_text(encoding='utf-8-sig'))))
 failures=[x for x in results if x[1] is not True]
 (R/'runtime/portrait-download-report.json').write_text(json.dumps({'downloaded':len(results)-len(failures),'failures':failures},indent=2))
 print('Historical portraits:',len(results)-len(failures),'loaded;',len(failures),'download failures')
 if failures:raise RuntimeError(str(failures))
if __name__=='__main__':hydrate(R/'runtime/theater-mod')
