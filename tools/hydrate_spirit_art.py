from pathlib import Path
import json
from PIL import Image,ImageOps,ImageDraw

def hydrate(game,out):
    root=Path(__file__).resolve().parents[1]
    manifest=json.loads((root/'spirit-art-manifest.json').read_text(encoding='utf-8'))
    dest=out/'gfx/interface/v65_spirits';dest.mkdir(parents=True,exist_ok=True)
    for role,texture in manifest['sources'].items():
        with Image.open(game/texture) as source:
            picture=ImageOps.contain(source.convert('RGBA'),(60,60),Image.Resampling.LANCZOS)
        icon=Image.new('RGBA',(64,64),(22,29,27,255))
        icon.alpha_composite(picture,((64-picture.width)//2,(64-picture.height)//2))
        ImageDraw.Draw(icon).rectangle((0,0,63,63),outline=(146,128,82,255))
        icon.save(dest/(role+'.dds'))
    # The theater's Park/ROK expedition uses the Taeguk flag from the local installation.
    with Image.open(game/'gfx/flags/KOR_democratic.tga') as source:
        flag=source.convert('RGB')
        for folder,size in [('',(82,52)),('medium',(41,26)),('small',(10,7))]:
            for suffix in ['','_neutrality','_communism','_democratic','_fascism']:
                flag.resize(size,Image.Resampling.LANCZOS).save(out/'gfx/flags'/folder/('PKS'+suffix+'.tga'))
