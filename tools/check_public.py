from pathlib import Path
import re,json,hashlib
r=Path('.')
(r/'tools/prepare_smoke.py').unlink(missing_ok=True)
manifest=[{'path':p.relative_to(r/'mod').as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (r/'mod').rglob('*') if p.is_file()]
(r/'public-manifest.json').write_text(json.dumps(manifest,indent=2))
issues=[]
for p in r.rglob('*'):
 if not p.is_file() or 'runtime' in p.parts or '.git' in p.parts:continue
 if p.suffix in ['.py','.ps1','.md','.json','.txt','.yml','.cmd','.gitignore']:
  t=p.read_text(encoding='utf-8-sig',errors='replace')
  if str(Path.home()).replace('\\','/').lower() in t.replace('\\','/').lower():issues.append(str(p))
assert not issues,issues
assert {p.name for p in (r/'mod/gfx').glob('leaders/**/*.dds')} <= {'park_seicheng.dds'}
print('Public source scan: PASS; only our original fictional portrait is bundled; historical art stays in runtime')
