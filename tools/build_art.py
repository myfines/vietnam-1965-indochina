"""Convert licensed Font Awesome glyphs and our original painting to game assets."""
from pathlib import Path
import json,shutil,math
from PIL import Image,ImageDraw,ImageFont,ImageOps
R=Path(__file__).resolve().parents[1];M=R/'mod';ref=R/'runtime/reference'
FONT=ref/'fa-solid-900.ttf'
if not FONT.exists():raise SystemExit('Fetch Font Awesome Free fa-solid-900.ttf into runtime/reference first')
icons={'flag':0xf024,'radio':0xf519,'shield':0xf3ed,'tree':0xf1bb,'factory':0xf275,'landmark':0xf66f,'helmet':0xf807,'scroll':0xf70e,'truck':0xf0d1}
out=M/'gfx/interface/goals';out.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype(str(FONT),43)
for key,code in icons.items():
 im=Image.new('RGBA',(96,96));d=ImageDraw.Draw(im)
 d.polygon([(48,3),(85,20),(83,68),(48,92),(13,68),(11,20)],fill=(28,36,33,255),outline=(181,147,83,255),width=3)
 d.line([(48,8),(80,23),(78,65),(48,85),(18,65),(16,23),(48,8)],fill=(88,100,88,255),width=1)
 d.text((48,44),chr(code),font=font,anchor='mm',fill=(233,206,144,255),stroke_width=0)
 d.line((30,74,66,74),fill=(181,147,83,255),width=2)
 im.save(out/f'v65_{key}.dds')
gfx='spriteTypes = {\n'+'\n'.join(f' spriteType = {{ name = "GFX_v65_focus_{k}" texturefile = "gfx/interface/goals/v65_{k}.dds" }}' for k in icons)+'\n}'
(M/'interface/v65_focus_icons.gfx').write_text(gfx,encoding='utf-8')
shutil.copyfile(ref/'FontAwesome-LICENSE.txt',R/'LICENSE-FontAwesome.txt')
# Our own faction flags. Four game sizes, no third-party flag artwork.
for tag,colors in {'PKS':[(39,80,68),(227,208,149)],'DNM':[(166,95,36),(247,223,152)],'FNL':[(159,36,42),(32,98,162)]}.items():
 flag=Image.new('RGB',(82,52),colors[0]);d=ImageDraw.Draw(flag)
 if tag=='FNL':d.rectangle((0,26,82,52),fill=colors[1])
 if tag=='PKS':d.rectangle((7,7,75,45),outline=colors[1],width=2)
 pts=[]
 for i in range(10):
  angle=-math.pi/2+i*math.pi/5;radius=14 if i%2==0 else 6
  pts.append((41+radius*math.cos(angle),26+radius*math.sin(angle)))
 d.polygon(pts,fill=(242,216,119))
 for folder,size in [('',(82,52)),('medium',(41,26)),('small',(10,7))]:
  dest=M/'gfx/flags'/folder;dest.mkdir(parents=True,exist_ok=True)
  for suffix in ['','_neutrality','_communism','_fascism','_democratic']:flag.resize(size,Image.Resampling.LANCZOS).save(dest/f'{tag}{suffix}.tga')
print('Focus art:',len(icons),'licensed glyphs; three faction flag sets')
