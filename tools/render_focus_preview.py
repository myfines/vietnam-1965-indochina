"""Offline geometry preview, not a screenshot of the game's interface."""
from pathlib import Path
import json,sys
from PIL import Image,ImageDraw,ImageFont

R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'vendor'))
import pdx
catalog=json.loads((R/'focus-art-manifest.json').read_text(encoding='utf-8'))['assignments']
layout=json.loads((R/'focus-layout-manifest.json').read_text(encoding='utf-8'))
game=Path(json.loads((R/'runtime/install-report.json').read_text())['game'])
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',19)
small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',15)
out=R/'runtime/test-results';out.mkdir(parents=True,exist_ok=True)
for tag in ['PKS','PARK_GOVERNMENT']:
    tree=pdx.read(R/f'mod/common/national_focus/v65_{tag}.txt')[0][2]
    nodes={dict((k,v) for k,_,v in n)['id']:dict((k,v) for k,_,v in n) for k,_,n in tree if k=='focus'}
    sx,sy=48,70
    def point(n):return int(float(n['x'])*sx+140),int(float(n['y'])*sy+140)
    panel=layout['v65_'+tag]['continuous_panel_y']
    im=Image.new('RGB',(int(max(float(n['x']) for n in nodes.values())*sx+300),int(panel/130*sy+240)),(27,34,37))
    d=ImageDraw.Draw(im)
    d.text((25,15),'国策坐标预览 · 非游戏截图 · '+tag,font=font,fill='#e5dbbe')
    for ident,n in nodes.items():
        x,y=point(n)
        for k,_,group in next(v for a,_,v in tree if a=='focus' and dict((b,c) for b,_,c in v)['id']==ident):
            if k=='prerequisite':
                for _,_,parent in group:
                    if parent in nodes:
                        px,py=point(nodes[parent]);middle=y-67
                        d.line([(px,py+54),(px,middle),(x,middle),(x,y-46)],fill='#7c8d85',width=2)
    for ident,n in nodes.items():
        x,y=point(n);d.rounded_rectangle((x-77,y-46,x+77,y+58),8,fill='#38433e',outline='#b5a372',width=2)
        asset=game/catalog[ident]['texture']
        if asset.is_file():
            icon=Image.open(asset).convert('RGBA');icon.thumbnail((60,60));im.paste(icon,(x-icon.width//2,y-44),icon)
        title=catalog[ident]['title'];lines=[title[i:i+8] for i in range(0,len(title),8)][:2]
        for row,line in enumerate(lines):d.text((x-d.textlength(line,font=small)/2,y+17+row*18),line,font=small,fill='#faf0d2')
    py=int(panel/130*sy+140)
    d.rounded_rectangle((60,py,650,py+100),8,outline='#a4956a',width=2)
    d.text((80,py+30),'持续国策面板：位于所有剧情节点下方',font=font,fill='#e5dbbe')
    im.save(out/f'focus-layout-{tag}.png')
    chapter=[point(n) for ident,n in nodes.items() if ident.startswith('v65chapter_')]
    im.crop((min(x for x,y in chapter)-100,min(y for x,y in chapter)-85,
        max(x for x,y in chapter)+100,max(y for x,y in chapter)+95)).save(out/f'chapter-focus-{tag}.png')
    print(tag,len(nodes),'nodes; offline previews written')
