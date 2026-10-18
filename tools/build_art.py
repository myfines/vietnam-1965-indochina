"""Bind native painted focus art and generate original faction flags."""
from pathlib import Path
import json,math
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];M=R/'mod';ref=R/'runtime/reference'
# Reuse installed HOI4 painted focus textures, referenced rather than redistributed.
# No downloaded game textures are stored in the public repository.
textures={
 'flag':'goal_generic_propaganda','radio':'goal_generic_intelligence_exchange',
 'shield':'goal_generic_fortify_city','tree':'goal_generic_allies_build_infantry',
 'factory':'goal_generic_construction2','landmark':'focus_generic_treaty',
 'helmet':'focus_generic_military_academy','scroll':'focus_generic_diplomatic_treaty',
 'truck':'goal_generic_construct_infrastructure',
 'armor':'goal_generic_army_tanks','motorized':'goal_generic_army_motorized',
 'doctrine':'goal_generic_army_doctrines','industry':'goal_generic_construction',
 'artillery':'goal_generic_army_artillery','pressure':'goal_generic_forceful_treaty',
 'sanctuary':'focus_generic_coastal_fort','union':'focus_generic_treaty',
}
icons=textures
out=M/'gfx/interface/goals'
for old in out.glob('v65_*.dds'):old.unlink()
gfx='spriteTypes = {\n'+'\n'.join(f' spriteType = {{ name = "GFX_v65_focus_{k}" texturefile = "gfx/interface/goals/{v}.dds" }}' for k,v in textures.items())+'\n}'
(M/'interface/v65_focus_icons.gfx').write_text(gfx,encoding='utf-8')
(R/'native-art-catalog.json').write_text(json.dumps(textures,indent=2),encoding='utf-8')
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
print('Focus art:',len(icons),'native painted references; three faction flag sets')
