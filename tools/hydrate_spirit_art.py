from pathlib import Path
import json
from PIL import Image,ImageOps,ImageDraw

def hydrate(game,out):
    root=Path(__file__).resolve().parents[1]
    manifest=json.loads((root/'spirit-art-manifest.json').read_text(encoding='utf-8'))
    dest=out/'gfx/interface/v65_spirits';dest.mkdir(parents=True,exist_ok=True)
    for role,texture in manifest['sources'].items():
        with Image.open(game/texture) as source:
            picture=ImageOps.contain(source.convert('RGBA'),(54,54),Image.Resampling.LANCZOS)
        icon=Image.new('RGBA',(64,64),(18,28,35,255))
        frame=ImageDraw.Draw(icon)
        frame.polygon([(8,1),(55,1),(62,8),(62,55),(55,62),(8,62),(1,55),(1,8)],fill=(30,44,52),outline=(169,146,98))
        frame.line((9,4,54,4),fill=(213,187,130))
        icon.alpha_composite(picture,((64-picture.width)//2,(64-picture.height)//2))
        if '_rank' in role:
            rank=int(role.rsplit('_rank',1)[1]);draw=ImageDraw.Draw(icon)
            draw.rectangle((13,54,50,60),fill=(15,24,31))
            for n in range(5):draw.rectangle((15+n*7,56,19+n*7,58),fill=(218,186,118) if n<rank else (61,77,83))
        if '_support' in role:
            percent=int(role.rsplit('_support',1)[1]);draw=ImageDraw.Draw(icon)
            draw.rectangle((10,54,53,60),fill=(15,24,31))
            draw.rectangle((12,56,12+round(39*percent/100),58),fill=(119,184,186))
        icon.save(dest/(role+'.dds'))
    # The theater's Park/ROK expedition uses the Taeguk flag from the local installation.
    with Image.open(game/'gfx/flags/KOR_democratic.tga') as source:
        flag=source.convert('RGB')
        for folder,size in [('',(82,52)),('medium',(41,26)),('small',(10,7))]:
            for suffix in ['','_neutrality','_communism','_democratic','_fascism']:
                flag.resize(size,Image.Resampling.LANCZOS).save(out/'gfx/flags'/folder/('PKS'+suffix+'.tga'))
