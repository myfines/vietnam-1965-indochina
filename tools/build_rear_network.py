"""State-level rear networks, attached to local supply and manpower."""
from pathlib import Path
import re
from build_campaign import M,put
from long_foundation import loc_text,REGIONS

STATES=[14,16,17,18,19,20,21,22,23,24,26,27,28,29,30]
SOUTH=['SVN','PKS','DNM',*REGIONS]
L={'v65_rear_networks':'州内后方与游击网络','v65_rear_networks_desc':'后方网络分三级，直接削弱当地补给与可用人力。清剿与村庄协议影响所选州；解放阵线可培植网络并发动起义。'}
dynamic=''
refresh='v65_refresh_rear_state = { clamp_variable = { var = v65_rear_level min = 0 max = 3 }\n'
for n in [1,2,3]:
 key='v65_rear_pressure_'+str(n)
 dynamic+=f'{key} = {{ icon = 1 enable = {{ always = yes }} local_supplies = {-0.05*n:.2f} local_manpower = {-0.04*n:.2f} }}\n'
 L[key]=['潜伏联络网','活动中的游击网络','武装起义准备'][n-1]
 L[key+'_desc']=f'当地后方压力第{n}级：本地补给减少{n*0.05:.2f}，可用人力减少{n*4}%。军区清剿、村庄协定和外部渗透可改变等级。'
 refresh+=f'if = {{ limit = {{ has_dynamic_modifier = {{ modifier = {key} }} }} remove_dynamic_modifier = {{ modifier = {key} }} }}\n'
for n in [1,2,3]:refresh+=f'if = {{ limit = {{ check_variable = {{ v65_rear_level = {n} }} }} add_dynamic_modifier = {{ modifier = v65_rear_pressure_{n} }} }}\n'
effects=refresh+'}\nv65_rear_relief = { every_owned_state = { limit = { check_variable = { v65_rear_level > 0 } } subtract_from_variable = { v65_rear_level = 1 } v65_refresh_rear_state = yes } }\n'
decisions='v65_rear_networks = {\n'
for sid in STATES:
 state=(M/f'history/states/{sid}.txt').read_text(encoding='utf-8-sig')
 provinces=list(map(int,re.search(r'provinces = \{([^}]+)',state)[1].split()))
 # Pick a non-victory-point province, so a rear incident does not instantly seize a regional capital.
 cities={int(v) for v in re.findall(r'victory_points = \{\s*(\d+)',state)}
 pid=next((p for p in provinces if p not in cities and p not in {243,287,316}),provinces[0])
 owners='OR = { '+' '.join(f'{t} = {{ owns_state = {sid} has_war_with = FNL }}' for t in SOUTH)+' }'
 controllers='OR = { '+' '.join(f'{t} = {{ controls_province = {pid} has_war_with = FNL }}' for t in SOUTH)+' }'
 effects+=f'''v65_rear_rise_{sid} = {{
 if = {{ limit = {{ tag = FNL {owners} {controllers} {sid} = {{ check_variable = {{ v65_rear_level > 2 }} NOT = {{ has_state_flag = v65_rear_cooldown }} }} }}
  set_province_controller = {pid}
  {sid} = {{ create_unit = {{ division = "name = \\"Local Liberation Detachment\\" division_template = \\"Theater Infantry\\" start_equipment_factor = 0.65 start_experience_factor = 0.25 location = {pid}" owner = FNL count = 1 }}
   set_variable = {{ v65_rear_level = 1 }} set_state_flag = v65_rear_cooldown v65_refresh_rear_state = yes
  }}
  country_event = {{ id = v65rear.{100+sid} days = 120 }}
 }}
}}
'''
 for slug,name,cost,effect in [
  ('patrol','清剿',45,f'{sid} = {{ subtract_from_variable = {{ v65_rear_level = 1 }} v65_refresh_rear_state = yes }} subtract_from_variable = {{ v65_public_trust = 2 }}'),
  ('compact','签订村庄保护协定',70,f'{sid} = {{ subtract_from_variable = {{ v65_rear_level = 1 }} v65_refresh_rear_state = yes }} add_to_variable = {{ v65_public_trust = 3 }}'),
 ]:
  key=f'v65_rear_{slug}_{sid}';L[key]=f'$V65_STATE_{sid}$：{name}'
  L[key+'_desc']=f'当前网络等级：[?{sid}.v65_rear_level|0]/3。降低1级，只影响本州。清剿消耗45政治点并降低2民心；村庄协议消耗70政治点并增加3民心。'
  decisions+=f'{key} = {{ icon = generic_political_discourse cost = {cost} visible = {{ owns_state = {sid} NOT = {{ tag = FNL }} {sid} = {{ check_variable = {{ v65_rear_level > 0 }} }} }} available = {{ {sid} = {{ is_fully_controlled_by = ROOT }} }} days_re_enable = 90 complete_effect = {{ {effect} v65_refresh_society = yes }} ai_will_do = {{ factor = 0.5 }} }}\n'
 key=f'v65_rear_network_{sid}';L[key]=f'$V65_STATE_{sid}$：培植地方网络';L[key+'_desc']='消耗40政治点，使该州后方网络上升一级，最高三级。每60天一次。'
 decisions+=f'{key} = {{ icon = generic_political_discourse cost = 40 visible = {{ tag = FNL {owners} }} available = {{ {sid} = {{ check_variable = {{ v65_rear_level < 3 }} }} }} days_re_enable = 60 complete_effect = {{ {sid} = {{ add_to_variable = {{ v65_rear_level = 1 }} v65_refresh_rear_state = yes }} }} ai_will_do = {{ factor = 0.25 }} }}\n'
 key=f'v65_rear_rise_{sid}';L[key]=f'$V65_STATE_{sid}$：发动地方起义';L[key+'_desc']='需要三级网络及仍由交战南方势力控制的后方据点。部署一个解放阵线分队，网络降至一级，本州起义冷却120天。'
 decisions+=f'{key} = {{ icon = generic_prepare_civil_war cost = 65 visible = {{ tag = FNL {owners} }} available = {{ {controllers} {sid} = {{ check_variable = {{ v65_rear_level > 2 }} NOT = {{ has_state_flag = v65_rear_cooldown }} }} }} days_re_enable = 120 complete_effect = {{ v65_rear_rise_{sid} = yes }} ai_will_do = {{ factor = 0.25 }} }}\n'
put(Path('common/dynamic_modifiers/v65_rear.txt'),dynamic)
put(Path('common/scripted_effects/v65_rear.txt'),effects)
put(Path('common/decisions/v65_rear.txt'),decisions+'}')
put(Path('events/v65_rear.txt'),'add_namespace = v65rear\n'+'\n'.join(f'country_event = {{ id = v65rear.{100+sid} hidden = yes is_triggered_only = yes immediate = {{ {sid} = {{ clr_state_flag = v65_rear_cooldown }} }} }}' for sid in STATES))
put(Path('common/decisions/categories/v65_rear.txt'),'v65_rear_networks = { icon = GFX_decision_generic_military allowed = { OR = { '+' '.join('tag = '+t for t in SOUTH+['FNL'])+' } } visible = { always = yes } }')
init=' '.join(f'{sid} = {{ if = {{ limit = {{ NOT = {{ has_state_flag = v65_rear_initialized }} }} set_state_flag = v65_rear_initialized set_variable = {{ v65_rear_level = {2 if sid in [18,23,27] else 1} }} v65_refresh_rear_state = yes }} }}' for sid in STATES)
monthly=''
for tag in SOUTH:
 monthly+=f'{tag} = {{ if = {{ limit = {{ exists = yes }} set_variable = {{ v65_rear_hotspots = 0 }} every_owned_state = {{ limit = {{ check_variable = {{ v65_rear_level > 1 }} }} PREV = {{ add_to_variable = {{ v65_rear_hotspots = 1 }} }} }} }} }}\n'
put(Path('common/on_actions/v65_rear.txt'),'on_actions = { on_startup = { effect = { '+init+' } } on_monthly = { effect = { '+monthly+' } } }')
for lang in ['simp_chinese','english']:put(Path(f'localisation/{lang}/zzzzzzzz_v65_rear_l_{lang}.yml'),loc_text(L,lang))
print('Local rear networks: 15 states, three supply/manpower tiers and targeted local actions')
