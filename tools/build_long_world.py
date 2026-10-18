"""Cambodian civil war and four optional South Vietnamese regional governments."""
from build_campaign import put,M,R
from long_foundation import REGIONS,ALL,loc_text
from pathlib import Path
import re,json

def state(sid):return (M/f'history/states/{sid}.txt').read_text(encoding='utf-8-sig')
def provinces(sid):return list(map(int,re.search(r'provinces = \{([^}]+)',state(sid))[1].split()))
def city(sid):
 vp=re.findall(r'victory_points = \{ (\d+) (\d+) \}',state(sid))
 return int(max(vp,key=lambda x:int(x[1]))[0]) if vp else provinces(sid)[0]
TEMPLATE='division_template = { name = "Theater Infantry" regiments = { infantry = { x = 0 y = 0 } infantry = { x = 0 y = 1 } infantry = { x = 0 y = 2 } infantry = { x = 1 y = 0 } infantry = { x = 1 y = 1 } infantry = { x = 1 y = 2 } } }'
EXTRA={'RKH':('红色高棉','Khmer Rouge',36,[36,37,38,43],'127 28 39','pol_pot','波尔布特','KMP/Pol_Pot_70s.dds'),**REGIONS}
tags=(M/'common/country_tags/v65.txt').read_text(encoding='utf-8')
for tag in EXTRA:tags+='\n'+tag+' = "countries/'+tag+'.txt"'
put(Path('common/country_tags/v65.txt'),tags)
catalog=json.loads((R/'portrait-catalog.json').read_text(encoding='utf-8'))
names={}
for tag,(cn,en,capital,states,rgb,key,person,source) in EXTRA.items():
 ideology='communism' if tag=='RKH' else 'neutrality'
 put(Path(f'common/countries/{tag}.txt'),f'graphical_culture = asian_gfx\ngraphical_culture_2d = asian_2d\ncolor = {{ {rgb} }}')
 put(Path(f'history/countries/{tag} - Theater.txt'),f'''capital = {capital}
oob = "{tag}_1965"
set_research_slots = 3
set_stability = 0.55
set_war_support = 0.65
set_politics = {{ ruling_party = {ideology} elections_allowed = no }}
set_popularities = {{ {ideology} = 100 }}
set_technology = {{ infantry_weapons = 1 infantry_weapons1 = 1 infantry_weapons2 = 1 tech_support = 1 tech_trucks = 1 }}
add_ideas = {{ limited_conscription partial_economic_mobilisation export_focus }}
add_political_power = 150
add_equipment_to_stockpile = {{ type = infantry_equipment_2 amount = 12000 producer = {tag} }}
recruit_character = v65_{key}
''')
 units=[]
 if tag=='RKH':
  for sid in states:
   text=state(sid);text=re.sub(r'owner = \w+','owner = RKH',text,count=1)
   if 'add_core_of = RKH' not in text:text=text.replace('owner = RKH','owner = RKH add_core_of = RKH')
   put(Path(f'history/states/{sid}.txt'),text)
  for n,sid in enumerate(states+[36,37]):units.append(f' division = {{ name = "Khmer Revolutionary Regiment {n+1}" location = {city(sid)} division_template = "Theater Infantry" start_equipment_factor = 0.7 start_experience_factor = 0.3 }}')
 put(Path(f'history/units/{tag}_1965.txt'),TEMPLATE+'\nunits = {\n'+'\n'.join(units)+'\n}')
 cid='v65_'+key;portrait=f'gfx/leaders/v65/{key}.dds' if source else f'gfx/flags/{tag}.tga'
 if source:catalog.append({'id':key,'source':source,'target':portrait,'provider':'Cold War Iron Curtain','distribution':'downloaded into runtime only; not bundled in public repository'})
 names[cid]=person
 role='marxism' if tag=='RKH' else 'despotism'
 general='' if tag=='PHQ' else 'corps_commander = { skill = 3 attack_skill = 3 defense_skill = 3 planning_skill = 3 logistics_skill = 3 traits = { } }'
 put(Path(f'common/characters/v65_{tag}.txt'),f'characters = {{ {cid} = {{ name = {cid} portraits = {{ civilian = {{ large = "{portrait}" small = "{portrait}" }} army = {{ large = "{portrait}" small = "{portrait}" }} }} country_leader = {{ ideology = {role} expire = "1990.1.1" }} {general} }} }}')
(R/'portrait-catalog.json').write_text(json.dumps(catalog,indent=2),encoding='utf-8')
# Government and insurgency both receive real field armies on their own land.
gov_states=[32,33,34,35,39,40,41,42]
put(Path('history/units/KHM_1965.txt'),TEMPLATE+'\nunits = {\n'+'\n'.join(f' division = {{ name = "Royal Regiment {n+1}" location = {city(sid)} division_template = "Theater Infantry" start_equipment_factor = 0.8 start_experience_factor = 0.3 }}' for n,sid in enumerate(gov_states))+'\n}')
p=M/'common/bookmarks/v65.txt';text=p.read_text(encoding='utf-8');text=text[:-4]+' RKH = { history = V65_RKH_DESC ideology = communism }\n} }\n';p.write_text(text,encoding='utf-8')

# Names are authoritative in one replacement file, not competing overlays.
base={'SVN':('越南共和国','Republic of Vietnam'),'NVN':('北越','North Vietnam'),'FNL':('南方民族解放阵线','National Liberation Front'),'PKS':('朴世诚远征集团','Park Expeditionary Group'),'DNM':('岘港军区','Da Nang Military Command'),'KHM':('柬埔寨王国','Kingdom of Cambodia')}
base.update({t:(v[0],v[1]) for t,v in EXTRA.items()})
pattern=r'\s*(?:'+'|'.join(ALL)+r')(?:_(?:DEF|ADJ|neutrality|communism|democratic|fascism)(?:_(?:DEF|ADJ))?)?:\d'
for p in (M/'localisation').rglob('*.yml'):
 if p.name.startswith('v65_country_names_'):continue
 text='\n'.join(s for s in p.read_text(encoding='utf-8-sig').splitlines() if not re.match(pattern,s) and not re.match(r'\s*V65_BOOKMARK_DESC:',s))
 p.write_text(text+'\n',encoding='utf-8-sig')
for lang in ['simp_chinese','english']:
 loc={}
 loc['V65_BOOKMARK_DESC']='七个开局可玩势力：北越、南越、解放阵线、朴世诚、岘港军区、柬埔寨王国和红色高棉。南越可分权给四个自治军区。1965—1979的军事、社会与人物选择共同决定战争结局。' if lang=='simp_chinese' else 'Seven playable factions, two Cambodian belligerents and four optional regional governments. A 1965–1979 narrative campaign of military, social and personal choices.'
 for tag,pair in base.items():
  name=pair[0 if lang=='simp_chinese' else 1]
  for suffix in ['','_DEF','_ADJ']+[f'_{i}{s}' for i in ['neutrality','democratic','communism','fascism'] for s in ['','_DEF','_ADJ']]:loc[tag+suffix]=name
 for key,name in names.items():loc[key]=name if lang=='simp_chinese' else key[4:].replace('_',' ').title()
 loc['V65_RKH_DESC']='丛林中的革命根据地正在与金边政府交战。对越南的秘密通道、对村庄的控制和与北方的关系，将共同决定红色高棉的未来。此1965内战开局为小说启发的架空设定。'
 put(Path(f'localisation/replace/v65_country_names_l_{lang}.yml'),loc_text(loc,lang))

regions_effect='v65_devolve_regions = { if = { limit = { tag = SVN NOT = { has_country_flag = v65_regionalized } }\n set_country_flag = v65_regionalized add_ideas = v65_decentralized_command\n'
events='add_namespace = v65regions\n'
decisions='v65_regional_government = {\n v65_devolve = { icon = generic_political_discourse cost = 100 visible = { tag = SVN NOT = { has_country_flag = v65_regionalized } } available = { controls_state = 25 } complete_effect = { country_event = { id = v65regions.1 days = 1 } } ai_will_do = { factor = 0 } }\n'
L={'v65_regional_government':'军区、中央与地方战争','v65_devolve':'将治安与军政权下放各战区','v65_devolve_desc':'提出军区自治方案。确认后将中央实际掌握的西原、东南、湄公河与富国岛地区交给拥有本地部队的自治附属军区；各区动员驻军、处理本地叛乱并承担财政。中央失去直接控制，可援助并协商重新整合。','v65_decentralized_command':'军区自治体制','v65_decentralized_command_desc':'各区独立掌握土地和驻军，负责辖区治安。中央命令协调较慢，但不必亲自处置每一处乡村冲突。','v65_local_command':'本地军政司令部','v65_local_command_desc':'军区依靠自己的预算、警务和部队维持统治。中央援助提高忠诚，军警镇压与乡村协商各有长期代价。','v65_reintegrated_command':'重新签署的战区协定','v65regions.1.t':'一张地图，几本军饷账','v65regions.1.d':'联络官把西原、湄公河、东南与富国岛涂成了不同颜色。\n\n“每个司令都说自己能管好辖区。”总统府秘书停了一下，“条件是军饷和任命都由他们自己签。”\n\n下放权力可以让地方部队专心对付自己的游击网络，也会把中央的命令变成下一轮谈判。归仁和岘港现有的独立指挥体系将继续存在。','v65regions.1.a':'签署军区自治协议。','v65regions.1.b':'暂缓，仍由中央直接负责。','v65regions.2.t':'自治后的第一份治安报告','v65regions.2.d':'县长在白天报平安，巡逻队却在夜里失去了两名向导。司令部桌上放着征粮清单、村长的请愿书和中央迟来的电报。\n\n自治没有让战争消失，只让每一个决定都更靠近负责签字的人。选择清剿、协商或情报甄别，将影响当地民心与下一次武装爆发。','v65regions.2.a':'从本地的账开始。'}
for tag,(cn,en,capital,states,rgb,key,person,source) in REGIONS.items():
 pid=city(capital)
 regions_effect+=f' if = {{ limit = {{ owns_state = {capital} controls_province = {pid} {capital} = {{ is_fully_controlled_by = SVN }} }}\n'
 for sid in states:regions_effect+=f' if = {{ limit = {{ owns_state = {sid} {sid} = {{ is_fully_controlled_by = SVN }} }} {sid} = {{ add_core_of = {tag} }} }}\n'
 regions_effect+=f' release_puppet = {tag}\n'
 for sid in states:regions_effect+=f' if = {{ limit = {{ {tag} = {{ owns_state = {sid} }} }} {tag} = {{ set_state_controller = {sid} }} }}\n'
 regions_effect+=f' {tag} = {{ set_capital = {{ state = {capital} }} add_manpower = 12000 load_oob = "{tag}_1965" add_ideas = v65_local_command set_variable = {{ v65_regional_loyalty = 50 }} set_variable = {{ v65_local_unrest = 3 }} set_variable = {{ v65_public_trust = 50 }} set_variable = {{ v65_patronage = 20 }} set_variable = {{ v65_intelligence = 1 }} set_country_flag = v65_story_initialized country_event = {{ id = v65regions.2 days = 3 }}\n {capital} = {{ create_unit = {{ division = "name = \\"Regional Security Regiment\\" division_template = \\"Theater Infantry\\" start_equipment_factor = 0.8 location = {pid}" owner = {tag} count = 2 }} }} }}\n'
 regions_effect+=f' {tag} = {{ country_event = {{ id = v65regions.10 days = 2 }} }}\n }}\n'
 decisions+=f' v65_subsidize_{tag} = {{ icon = generic_political_discourse cost = 60 visible = {{ tag = SVN {tag} = {{ exists = yes }} }} available = {{ is_in_faction_with = {tag} }} days_re_enable = 90 complete_effect = {{ {tag} = {{ add_to_variable = {{ v65_regional_loyalty = 10 }} add_to_variable = {{ v65_public_trust = 5 }} add_political_power = 30 add_equipment_to_stockpile = {{ type = infantry_equipment_2 amount = 600 producer = SVN }} }} }} ai_will_do = {{ factor = 0.5 }} }}\n'
 decisions+=f' v65_reintegrate_{tag} = {{ icon = generic_political_discourse cost = 120 visible = {{ tag = SVN {tag} = {{ exists = yes }} }} available = {{ {tag} = {{ is_ai = yes check_variable = {{ v65_regional_loyalty > 74 }} controls_province = {pid} }} is_in_faction_with = {tag} }} complete_effect = {{ v65_regional_reintegration_{tag} = yes }} ai_will_do = {{ factor = 0.5 }} }}\n'
 decisions+=f' v65_play_{tag} = {{ icon = generic_political_discourse cost = 0 visible = {{ tag = SVN {tag} = {{ exists = yes }} is_ai = no }} complete_effect = {{ {tag} = {{ change_tag_from = ROOT }} }} }}\n'
 L.update({f'v65_subsidize_{tag}':f'向{cn}拨付军需',f'v65_reintegrate_{tag}':f'协商整合{cn}',f'v65_play_{tag}':f'接手扮演{cn}'})
regions_effect+='} }\n'
for tag,(_,_,capital,states,_,key,_,_) in REGIONS.items():
 regions_effect+=f'''v65_regional_reintegration_{tag} = {{ if = {{ limit = {{ tag = SVN {tag} = {{ exists = yes is_ai = yes check_variable = {{ v65_regional_loyalty > 74 }} }} }}
 if = {{ limit = {{ has_country_leader = {{ character = v65_duong_van_minh }} }} set_country_flag = v65_preserve_minh }}
 {tag} = {{ v65_{key} = {{ set_nationality = SVN }} }}
 annex_country = {{ target = {tag} transfer_troops = yes }} add_ideas = v65_reintegrated_command
 if = {{ limit = {{ has_country_flag = v65_preserve_minh }} promote_character = {{ character = v65_duong_van_minh ideology = despotism }} clr_country_flag = v65_preserve_minh }}
 else = {{ promote_character = {{ character = v65_nguyen_van_thieu ideology = despotism }} }}
}} }}\n'''
# Let the engine rebuild diplomatic and theatre data between handovers.
import sys
sys.path.insert(0,str(R/'vendor'))
import pdx
blocks=pdx.parse(regions_effect)
root=blocks[0][2][0][2]
regional=[entry for entry in root if entry[0]=='if']
base=[entry for entry in root if entry[0]!='if']
for index,(tag,entry) in enumerate(zip(REGIONS,regional),11):
 # A fresh regional country must join its inherited war before its new army
 # is materialised; otherwise adjacent old fronts cache a neutral army area.
 capital=REGIONS[tag][2]
 handover=[]
 for key,op,value in entry[2]:
  if key==tag and any(e[0]=='set_capital' for e in value):
   value=[e for e in value if e[0]!=str(capital)]
   value+=pdx.parse('country_event = { id = v65regions.20 days = 3 }')
  handover.append((key,op,value))
 entry=('if','=',handover)
 base+=pdx.parse(f'country_event = {{ id = v65regions.{index} days = {index-10} }}')
 blocks.append((f'v65_devolve_{tag}','=',[entry]))
 events+=f'country_event = {{ id = v65regions.{index} hidden = yes is_triggered_only = yes immediate = {{ v65_devolve_{tag} = yes }} }}\n'
blocks[0]=('v65_devolve_regions','=',[('if','=',base)])
put(Path('common/scripted_effects/v65_regions.txt'),pdx.dump(blocks))
mobilize=''
for tag,(_,_,capital,*_) in REGIONS.items():
 pid=city(capital)
 mobilize+=f'if = {{ limit = {{ tag = {tag} controls_province = {pid} }} {capital} = {{ create_unit = {{ division = "name = \\"Regional Security Regiment\\" division_template = \\"Theater Infantry\\" start_equipment_factor = 0.8 location = {pid}" owner = {tag} count = 2 }} }} }}\n'
events+='country_event = { id = v65regions.20 hidden = yes is_triggered_only = yes immediate = { '+mobilize+'} }\n'
events+='country_event = { id = v65regions.10 hidden = yes is_triggered_only = yes immediate = { if = { limit = { SVN = { has_war_with = NVN } NOT = { has_war_with = NVN } } add_to_war = { targeted_alliance = SVN enemy = NVN hostility_reason = asked_to_join } } if = { limit = { SVN = { has_war_with = FNL } NOT = { has_war_with = FNL } } add_to_war = { targeted_alliance = SVN enemy = FNL hostility_reason = asked_to_join } } SVN = { add_to_faction = ROOT } } }\n'
events+='country_event = { id = v65regions.1 title = v65regions.1.t desc = v65regions.1.d picture = GFX_report_event_generic_sign_treaty is_triggered_only = yes option = { name = v65regions.1.a v65_devolve_regions = yes } option = { name = v65regions.1.b add_political_power = 75 } }\n'
events+='country_event = { id = v65regions.2 title = v65regions.2.t desc = v65regions.2.d picture = GFX_report_event_generic_read_write is_triggered_only = yes option = { name = v65regions.2.a add_political_power = 25 } }\n'
put(Path('events/v65_regions.txt'),events)
put(Path('common/decisions/v65_regions.txt'),decisions+'}\n')
put(Path('common/decisions/categories/v65_regions.txt'),'v65_regional_government = { icon = GFX_decision_generic_military allowed = { OR = { tag = SVN tag = HLC tag = MKG tag = BHD tag = PHQ } } visible = { always = yes } }')
put(Path('common/on_actions/v65_cambodia.txt'),'''on_actions = { on_startup = { effect = {
 KHM = { if = { limit = { NOT = { has_country_flag = v65_civil_war_started } } set_country_flag = v65_civil_war_started declare_war_on = { target = RKH type = annex_everything } } }
 RKH = { add_ideas = v65_jungle_revolution set_country_flag = v65_sanctuary_open }
} } on_monthly = { effect = { RKH = { if = { limit = { controls_state = 36 NVN = { has_war_with = SVN } } NVN = { add_to_variable = { v65_trail_level = 1 } clamp_variable = { var = v65_trail_level min = 0 max = 5 } } } } } } }''')
for lang in ['simp_chinese','english']:
 put(Path(f'localisation/{lang}/zzzzzz_v65_regions_l_{lang}.yml'),loc_text(L,lang))
print('Two Cambodian belligerents and four optional regional governments authored')
