"""Bind painted native assets by the action's subject, with explicit phase art."""
from pathlib import Path
import json,re,sys
from build_campaign import M,R,put
from build_art import textures as original
sys.path.insert(0,str(R/'vendor'));import pdx

game=Path(json.loads((R/'runtime/install-report.json').read_text(encoding='utf-8'))['game'])
TEXTURES={
 'command':'focus_generic_military_dictatorship',
 'staff':'focus_generic_military_academy',
 'inspect':'focus_generic_secret_service_agency',
 'reserve':'focus_generic_home_defense',
 'orders':'focus_generic_radio_communication',
 'radio':'focus_generic_radio_communication',
 'press':'focus_generic_printing_press',
 'treaty':'focus_generic_diplomatic_treaty',
 'autonomy':'focus_generic_treaty',
 'ledger':'focus_generic_currency_reforms',
 'payroll':'focus_generic_manpower',
 'contracts':'focus_generic_arms_trade',
 'recruit':'goal_generic_allies_build_infantry',
 'supply':'focus_generic_supply_line',
 'repair':'goal_continuous_repairments',
 'funds':'focus_generic_industry_investment',
 'korea':'focus_generic_diverse_army',
 'academy':'focus_generic_advanced_military_studies',
 'airlift':'focus_generic_long_range_aircraft',
 'adviser':'focus_generic_military_mission',
 'rotation':'focus_generic_jungle_training',
 'reinforce':'focus_generic_reinforcing_the_supply_network',
 'map':'focus_generic_hill_training',
 'proxy':'focus_generic_commonwealth_build_infantry',
 'village':'focus_generic_farmland',
 'garrison':'focus_generic_defensive_reorganization',
 'roads':'goal_generic_construct_infrastructure',
 'intelligence':'focus_generic_secret_agent_operative',
 'security':'focus_generic_national_security',
 'warehouse':'focus_generic_money_for_equipment',
 'port':'focus_generic_coastal_fort',
 'mainland':'goal_generic_fortify_city',
 'evacuation':'focus_generic_air_bases',
 'allocation':'focus_generic_industry_2',
 'mandate':'focus_generic_support_the_left_right',
 'regency':'focus_generic_conspiracy',
 'factory':'focus_generic_industry_3',
 'industry':'focus_generic_modernize_industry',
 'armor':'focus_generic_army_tanks2',
 'motorized':'goal_generic_army_motorized',
 'doctrine':'focus_generic_army_doctrines_2',
 'aircraft':'focus_generic_aircraft_production',
 'airdefence':'focus_generic_air_defense',
 'cas':'focus_generic_cas_aircraft',
 'navy':'focus_generic_large_navy',
 'navalinvasion':'focus_generic_naval_invasion',
 'coast':'focus_generic_naval_discipline',
 'airtraining':'focus_generic_pilot_training',
 'mountain':'focus_generic_mountain_training',
 'fort':'focus_generic_mountain_fortification',
 'revolution':'focus_generic_communist_industry',
 'trade':'focus_generic_trade_interdiction',
 'resources':'focus_generic_mining_industry',
 'civilian':'focus_generic_refit_civilian_ships',
 'leisure':'goal_generic_consumer_goods',
 'housing':'focus_generic_low_cost_housing',
}
for key,texture in TEXTURES.items():
 if not (game/f'gfx/interface/goals/{texture}.dds').exists():raise FileNotFoundError(f'Native focus texture {key}: {texture}')
L={}
for p in (M/'localisation/simp_chinese').glob('*.yml'):
 for line in p.read_text(encoding='utf-8-sig').splitlines():
  m=re.match(r'\s*(\w+):(?:\d+)?\s*"(.*)"',line)
  if m:L[m[1]]=m[2]
phase=json.loads((R/'park-government-manifest.json').read_text(encoding='utf-8'))['art']
chapter_art=json.loads((R/'chapter-focus-manifest.json').read_text(encoding='utf-8'))
phase.update(chapter_art['art'])
RULES=[
 ('navalinvasion',['登陆','渡海']),('airlift',['空运','直升机']),('airdefence',['防空']),('airtraining',['飞行员']),
 ('cas',['空中支援','轰炸']),('aircraft',['空军','航空']),('navy',['海军','舰队']),('coast',['海岸','沿岸']),
 ('resources',['资源','矿业','矿山']),('trade',['贸易','出口']),('factory',['工厂','兵工']),('industry',['工业','生产']),
 ('armor',['装甲','坦克']),('motorized',['摩托','机械化']),('fort',['工事','堡垒']),('mountain',['高地','山区']),
 ('roads',['公路','道路','交通']),('port',['港口','码头']),('warehouse',['仓库','库存']),('repair',['维修','零件']),
 ('regency',['政变','夺权','太上皇']),('payroll',['军饷','薪饷']),('contracts',['日海','合同']),
 ('ledger',['战报','账目','核实']),('inspect',['审计','监察','督察']),('intelligence',['情报','线人','甄别']),
 ('orders',['通信','联络']),('academy',['训练','军校']),('rotation',['轮休','轮换']),('proxy',['代理','地方团']),
 ('recruit',['征兵','招募','扩军']),('reserve',['预备队']),('village',['村庄','村长','乡村']),
 ('security',['清剿','治安']),('supply',['补给','运输']),('adviser',['顾问']),('autonomy',['自治','分权']),
 ('treaty',['协定','谈判','停火']),('command',['指挥','任命']),('civilian',['民政','社会','安置']),
]
bindings=[dict(name='GFX_v65_detail_'+k,texture=f'gfx/interface/goals/{v}.dds') for k,v in TEXTURES.items()]
sprite_lookup={x['name']:x['texture'] for x in bindings}
sprite_lookup.update({'GFX_v65_focus_'+k:f'gfx/interface/goals/{v}.dds' for k,v in original.items()})
assignments={}
for p in (M/'common/national_focus').glob('v65*.txt'):
 blocks=pdx.read(p)
 for _,_,tree in blocks:
  for kind,_,focus in tree:
   if kind!='focus':continue
   ident=next(v for k,_,v in focus if k=='id')
   title=L.get(ident,ident)
   chosen=phase.get(ident)
   if not chosen:chosen=next((role for role,terms in RULES if any(term in title for term in terms)),None)
   if chosen:focus[:]=[(k,op,'GFX_v65_detail_'+chosen if k=='icon' else v) for k,op,v in focus]
   icon=next(v for k,_,v in focus if k=='icon')
   assignments[ident]=dict(icon=icon,texture=sprite_lookup.get(icon,''),title=title)
 p.write_text(pdx.dump(blocks),encoding='utf-8')
put(Path('interface/v65_focus_detail.gfx'),'spriteTypes = {\n'+'\n'.join(f'spriteType = {{ name = "{x["name"]}" texturefile = "{x["texture"]}" }}' for x in bindings)+'\n}')
(R/'focus-art-manifest.json').write_text(json.dumps(dict(bindings=bindings,assignments=assignments),ensure_ascii=False,indent=2),encoding='utf-8')
actual={x['texture'] for x in assignments.values()}
print(f'Focus subjects: {len(actual)} distinct painted textures across {len(assignments)} nodes')
