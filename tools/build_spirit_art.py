"""Give every authored spirit an explicit icon; hydrate native pixels locally."""
from pathlib import Path
import json,sys,re
from build_campaign import M,R,put
sys.path.insert(0,str(R/'vendor'));import pdx

catalog=json.loads((R/'focus-art-manifest.json').read_text(encoding='utf-8'))
sources={x['name'].removeprefix('GFX_v65_detail_'):x['texture'] for x in catalog['bindings']}
sources.update(rokflag='gfx/flags/KOR_democratic.tga',rocflag='gfx/flags/CHI_neutrality.tga')
rules=[('airlift',['us_firepower']),('revolution',['jungle','revolution']),('contract',['contract','daihai']),('staff',['staff','command','central','council']),('training',['training','rotation']),('intelligence',['intelligence','signals','spy']),('supply',['supply','logistics','exhaustion','weariness']),('security',['security','coercion','guerrilla','pressure']),('port',['island','sanctuary']),('mandate',['mandate','regency','democratic','ruler']),('funds',['payroll','patron','fund','clique']),('reinforce',['prepared','defence'])]
assignments={};used={}
for path in sorted((M/'common/ideas').glob('v65*.txt')):
    blocks=pdx.read(path)
    for _,_,group in blocks:
        for kind,_,ideas in group:
            if kind!='country':continue
            for key,_,body in ideas:
                role=next((r for r,terms in rules if any(term in key for term in terms)),'treaty')
                if key=='v65_rok_liaison':role='rokflag'
                if key=='v65_roc_mission':role='rocflag'
                # All roles must refer to a real catalog entry; no generic missing picture fallback.
                if role=='contract':role='contracts'
                if role=='training':role='academy'
                texture=sources[role]
                picture='v65_spirit_'+role
                body[:]=[(k,op,picture if k=='picture' else v) for k,op,v in body]
                if not any(k=='picture' for k,_,v in body):body.insert(0,('picture','=',picture))
                assignments[key]=role;used[role]=texture
    path.write_text(pdx.dump(blocks),encoding='utf-8')
put(Path('interface/v65_spirit_art.gfx'),'spriteTypes = { '+' '.join(f'spriteType = {{ name = "GFX_idea_v65_spirit_{role}" texturefile = "gfx/interface/v65_spirits/{role}.dds" }}' for role in used)+' }')
(R/'spirit-art-manifest.json').write_text(json.dumps(dict(sources=used,assignments=assignments),indent=2),encoding='utf-8')
# Counts come from final generated files, including the new seven-node island line.
count=len(catalog['assignments'])
for filename in ['narrative-manifest.json','campaign-manifest.json']:
    path=R/filename;d=json.loads(path.read_text())
    d['version']='0.7.1'
    # The campaign manifest uses a nested narrative section in some source revisions.
    def update(obj):
        if isinstance(obj,dict):
            for k,v in obj.items():
                if k=='total_focuses':obj[k]=count
                elif k=='version':obj[k]='0.7.1'
                elif isinstance(v,(dict,list)):update(v)
        elif isinstance(obj,list):
            for v in obj:update(v)
    update(d);path.write_text(json.dumps(d,ensure_ascii=True,indent=2),encoding='utf-8')
print('Explicit spirit art:',len(assignments),'spirits;',len(used),'locally hydrated subjects')
