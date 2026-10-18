"""Render the authored layout for inspection; this is not a game screenshot."""
from pathlib import Path
import json,re
from PIL import Image,ImageDraw,ImageFont

R=Path(__file__).resolve().parents[1];M=R/'mod';runtime=R/'runtime/theater-mod'
layout=json.loads((R/'command-panel-layout.json').read_text(encoding='utf-8'))
im=Image.open(M/'gfx/interface/v65_command/dossier.dds').convert('RGBA')
loc={}
for p in (M/'localisation/simp_chinese').glob('*v65_panel*.yml'):
 for l in p.read_text(encoding='utf-8-sig').splitlines():
  m=re.match(r'\s*(\w+):0 "(.*)"',l)
  if m:loc[m[1]]=m[2]
sample={'SVN.v65_central_prestige':'55','DNM.v65_regional_loyalty':'65','DNM.v65_rear_hotspots':'0'}
font_path='C:/Windows/Fonts/msyh.ttc';draw=ImageDraw.Draw(im)
for w in layout['widgets']:
 if w['kind']=='portrait':
  path=next((p for p in [M/w['texture'],runtime/w['texture']] if p.exists()),None)
  if path:
   pic=Image.open(path).convert('RGBA');pic.thumbnail((w['width'],w['height']),Image.Resampling.LANCZOS);im.alpha_composite(pic,(w['x'],w['y']))
 else:
  text=loc.get(w['key'],w['key'])
  text=re.sub(r'\[\?([^]|]+)\|0\]',lambda m:sample.get(m[1],'0'),text)
  if w['name'].startswith('status_'):text='独立指挥' if w['name'] in ['status_DNM','status_PKS'] else '无独立司令部'
  size=24 if '24' in w['font'] else 18 if '18' in w['font'] else 14
  font=ImageFont.truetype(font_path,size)
  draw.text((w['x'],w['y']-1),text,font=font,fill=(221,215,187))
draw.rectangle((18,115,18+round(439*.55),122),fill=(175,151,88))
dest=R/'runtime/previews';dest.mkdir(exist_ok=True)
im.convert('RGB').resize((960,1096),Image.Resampling.LANCZOS).save(dest/'command-dossier-layout.png')
print('Layout preview saved; live game rendering has not been inspected.')
