"""Use native category illustrations, not one small action icon everywhere."""
from pathlib import Path
import json,sys
from build_campaign import M,R
sys.path.insert(0,str(R/'vendor'));import pdx
SUBJECTS={
 'theater':'military_operation','allied_missions':'generic_foreign_policy',
 'story_archive':'generic_propaganda','command_politics':'generic_political_actions',
 'contract_operations':'generic_arms_trade','story_governance':'generic_economy',
 'guest_stories':'generic_foreign_policy','us_mission':'military_operation',
 'north_plans':'generic_communist_revolution','personal_connections':'generic_trade',
 'politics':'generic_crisis','park':'generic_foreign_policy',
 'trail':'generic_mountain_fortification','rear_networks':'generic_fortification',
 'regional_government':'generic_political_actions','private_war':'generic_arms_trade',
 'union':'generic_political_actions','cambodian_rear':'generic_trade',
}
manifest={}
for path in sorted((M/'common/decisions/categories').glob('v65*.txt')):
    blocks=pdx.read(path)
    for key,_,body in blocks:
        sprite='GFX_decision_category_'+SUBJECTS[key.removeprefix('v65_')]
        body[:]=[(k,op,sprite if k=='icon' else v) for k,op,v in body]
        manifest[key]=sprite
    path.write_text(pdx.dump(blocks),encoding='utf-8')
(R/'category-art-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Native decision-category illustrations:',len(manifest),'categories;',len(set(manifest.values())),'subjects')
