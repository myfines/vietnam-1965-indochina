"""Render authored panel geometry offline; this is not an in-game screenshot."""
from pathlib import Path
import json,re
from PIL import Image,ImageDraw,ImageFont,ImageOps
R=Path(__file__).resolve().parents[1];M=R/'mod';O=R/'runtime/theater-mod'
font=Path('C:/Windows/Fonts/msyh.ttc')
layout=json.loads((R/'command-panel-layout.json').read_text())
panel=Image.open(M/'gfx/interface/v65_command/dossier.dds').convert('RGBA')
L={m[0]:m[1] for m in re.findall(r'^ ([^:]+):0 "(.*)"$',(M/'localisation/simp_chinese/zzzzzzzz_v65_panel_l_simp_chinese.yml').read_text(encoding='utf-8-sig'),re.M)}
draw=ImageDraw.Draw(panel)
for w in layout['widgets']:
    if w['kind']=='portrait':
        p=O/w['texture']
        if p.exists():
            with Image.open(p) as im:
                im=ImageOps.contain(im.convert('RGBA'),(w['width'],w['height']))
                panel.alpha_composite(im,(w['x'],w['y']))
    else:
        value=L[w['key']].replace('[PKS.GetLeader]','蔡命新').replace('[PHQ.GetLeader]','李威炎').replace('[v65_park_where]','韩军本部').replace('[v65_park_metrics]','人脉 0  军援 0')
        value=re.sub(r'\[\?[^\]]+\]',lambda m:'0' if 'rear_hotspots' in m[0] else '65' if 'regional_loyalty' in m[0] else '55',value)
        value=re.sub(r'\[v65_status_text_[A-Z]+\]','依指挥协定听令',value)
        draw.text((w['x'],w['y']),value,fill='#dfdacb',font=ImageFont.truetype(str(font),22 if '24header' in w['font'] else 14))
draw.rectangle((18,115,457,122),fill='#353c33');draw.rectangle((18,115,260,122),fill='#c5a970')
out=R/'runtime/test-results';out.mkdir(parents=True,exist_ok=True)
panel.convert('RGB').save(out/'command-panel-preview.png')
manifest=json.loads((R/'spirit-art-manifest.json').read_text())
roles=sorted(manifest['sources']);sheet=Image.new('RGB',(640,((len(roles)+7)//8)*100),'#131b22');d=ImageDraw.Draw(sheet)
for i,role in enumerate(roles):
    p=O/f'gfx/interface/v65_spirits/{role}.dds'
    if p.exists():
        with Image.open(p) as im:sheet.paste(im.convert('RGB'),(8+(i%8)*80,(i//8)*100))
    d.text((4+(i%8)*80,66+(i//8)*100),role,fill='#dfdacb',font=ImageFont.truetype(str(font),10))
sheet.save(out/'spirit-atlas-preview.png')
print('Offline command and spirit atlas previews written')
