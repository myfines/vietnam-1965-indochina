"""An open northern front, allied intervention and withdrawal-scaled support."""
from pathlib import Path
from build_campaign import M,put
from long_foundation import REGIONS,loc_text

L={
 'v65_us_mission':'美军干涉与撤军安排',
 'v65_us_firepower':'美军干涉：空中与火力支援',
 'v65_island_redoubt':'富国岛海上基地',
 'v65_island_redoubt_desc':'岛屿没有陆地通道。港口、岸防与留守部队构成离岛基地；西贡失守时提前启用独立指挥，避免随大陆投降直接移交。仍可遭受实际海上登陆。',
 'v65_delay_us_withdrawal':'用新一轮捷报争取延后撤军',
 'v65_delay_us_withdrawal_desc':'120政治点，撤军压力-15，每180天一次。只能在1968—1972年办理；不能无限延后1973年的最终撤军。',
 'v65_accept_us_withdrawal':'接受提前撤军与装备交接',
 'v65us.1.t':'干涉部队的作战边界',
 'v65us.1.a':'把这条界线画清楚。',
 'v65us.2.t':'撤军，交表',
 'v65us.2.a':'先把库存领走。',
}
effects='''v65_begin_intervention = {
 if = { limit = { NOT = { has_global_flag = v65_us_initialized } } set_global_flag = v65_us_initialized set_global_flag = v65_us_active
  10 = { set_demilitarized_zone = no clr_state_flag = v65_supervised_dmz }
  SVN = { set_variable = { v65_us_withdraw_pressure = 0 }
   11 = { create_unit = { division = "name = \\"US Intervention Combat Group\\" division_template = \\"Theater Infantry\\" start_equipment_factor = 1 start_experience_factor = 0.8" owner = SVN count = 4 } }
   25 = { create_unit = { division = "name = \\"US Airmobile Reserve\\" division_template = \\"Theater Infantry\\" start_equipment_factor = 1 start_experience_factor = 0.8" owner = SVN count = 2 } }
   31 = { create_unit = { division = "name = \\"Island Marine Garrison\\" division_template = \\"Theater Infantry\\" start_equipment_factor = 1 start_experience_factor = 0.8 location = 361" owner = SVN count = 2 } }
  }
 }
}
v65_withdraw_intervention = {
 if = { limit = { has_global_flag = v65_us_active } clr_global_flag = v65_us_active set_global_flag = v65_us_withdrawn
  10 = { set_demilitarized_zone = no clr_state_flag = v65_supervised_dmz }
  if = { limit = { 10 = { is_owned_by = XTR } SVN = { exists = yes } } SVN = { transfer_state = 10 } }
  SVN = { set_variable = { v65_us_withdraw_pressure = 100 } }
  every_country = { remove_ideas = { v65_us_firepower v65_us_firepower_75 v65_us_firepower_50 v65_us_firepower_25 } delete_unit_template_and_units = { division_template = "US Intervention Group" disband = no } }
  SVN = { add_equipment_to_stockpile = { type = infantry_equipment_2 amount = 1200 producer = SVN } add_equipment_to_stockpile = { type = motorized_equipment_1 amount = 150 producer = SVN } country_event = { id = v65us.2 days = 1 } }
 }
}
v65_evacuate_island = {
 if = { limit = { tag = SVN owns_state = 31 controls_province = 361 NOT = { controls_province = 305 } PHQ = { exists = no } }
  v65_devolve_PHQ = yes
 }
}
'''
# A separate locked template makes withdrawal remove only US mission units.
L.update({
 'v65_us_mission_desc':'美军撤军进度：[?SVN.v65_us_withdraw_pressure|0]/100。1968年起每月增加3，达到100或进入1973年撤走。十七度线正面开放，南方火力按进度四档递减。',
 'v65_us_firepower_desc':'撤军0—24：防御+300%、组织度+60%、进攻+35%、补给消耗-40%。没有非军事区或中立阻隔。',
 'v65_accept_us_withdrawal_desc':'1968年后可提前结束支援。撤走美军专属部队，移除美军加成，获得1200支步枪和150辆卡车。韩军与台湾国军另行安排。',
 'v65us.1.d':'十七度线没有中立屏障。美方提供火力与驻军，南方在撤军前拥有明显优势；撤走多少人，就少一档保障。',
 'v65us.2.d':'美方撤去火力保障，留下移交清单。韩军和国军顾问团各有自己的合同，另行安排。仓库里有什么，接收人签字。',
 'V65_STATE_10':'广治—十七度线',
})
tiers=[('v65_us_firepower',3,0.6,0.35,-0.4),('v65_us_firepower_75',2.25,0.45,0.25,-0.3),('v65_us_firepower_50',1.5,0.3,0.15,-0.2),('v65_us_firepower_25',0.75,0.15,0.05,-0.1)]
remove='remove_ideas = { '+' '.join(t[0] for t in tiers)+' }'
effects+='v65_refresh_us_support = { '+remove+' if = { limit = { has_global_flag = v65_us_active NOT = { has_country_flag = v65_rebel_command } OR = { tag = SVN AND = { is_in_faction_with = SVN NOT = { has_war_with = SVN } } } } '
for i,(key,defence,org,attack,supply) in enumerate(tiers):
 effects+=('if' if i==0 else 'else_if')+f' = {{ limit = {{ SVN = {{ check_variable = {{ v65_us_withdraw_pressure < {(i+1)*25} }} }} }} add_ideas = {key} }} '
 if i:
  L[key]=f'美军火力保障：剩余{100-i*25}%'
  L[key+'_desc']=f'美军撤军进度{i*25}—{i*25+24}：防御+{defence*100:g}%、组织度+{org*100:g}%、进攻+{attack*100:g}%、补给消耗{supply*100:g}%。下一档会替换本精神。'
effects+='} }\n'
effects=effects.replace('division_template = \\"Theater Infantry\\"','division_template = \\"US Intervention Group\\"')
p=M/'history/units/SVN_1965.txt'
template=p.read_text(encoding='utf-8').split('\n',1)[0].replace('"Theater Infantry"','"US Intervention Group" is_locked = yes')
p.write_text(template+'\n'+p.read_text(encoding='utf-8'),encoding='utf-8')
put(Path('common/scripted_effects/v65_intervention.txt'),effects)
allies=['SVN','PKS','DNM',*REGIONS]
support=' '.join(f'{t} = {{ if = {{ limit = {{ exists = yes }} v65_refresh_us_support = yes }} }}' for t in allies)
put(Path('common/on_actions/v65_intervention.txt'),'''on_actions = { on_startup = { effect = { SVN = { v65_begin_intervention = yes } } }
 on_daily = { effect = {
 if = { limit = { 10 = { has_state_flag = v65_supervised_dmz } } 10 = { set_demilitarized_zone = no clr_state_flag = v65_supervised_dmz } if = { limit = { 10 = { is_owned_by = XTR } SVN = { exists = yes } } SVN = { transfer_state = 10 } } }
 if = { limit = { has_global_flag = v65_us_active } SUPPORT }
 SVN = { if = { limit = { exists = yes } v65_evacuate_island = yes } }
 if = { limit = { has_global_flag = v65_us_active OR = { date > 1972.12.31 SVN = { check_variable = { v65_us_withdraw_pressure > 99 } } } } SVN = { v65_withdraw_intervention = yes } }
 } }
 on_monthly = { effect = { if = { limit = { has_global_flag = v65_us_active date > 1967.12.31 } SVN = { add_to_variable = { v65_us_withdraw_pressure = 3 } clamp_variable = { var = v65_us_withdraw_pressure min = 0 max = 100 } } } } }
}'''.replace('SUPPORT',support))
put(Path('common/ideas/v65_intervention.txt'),'ideas = { country = { '+' '.join(f'{key} = {{ picture = generic_army_chief allowed = {{ always = no }} modifier = {{ army_defence_factor = {defence} army_org_factor = {org} supply_consumption_factor = {supply} army_attack_factor = {attack} }} }}' for key,defence,org,attack,supply in tiers)+' } }')
put(Path('common/dynamic_modifiers/v65_island.txt'),'v65_island_redoubt = { icon = 1 enable = { always = yes } local_supplies = 2 }')
put(Path('events/v65_intervention.txt'),'add_namespace = v65us\n'+'\n'.join(f'country_event = {{ id = v65us.{n} is_triggered_only = yes title = v65us.{n}.t desc = v65us.{n}.d picture = GFX_report_event_generic_read_write option = {{ name = v65us.{n}.a }} }}' for n in [1,2]))
put(Path('common/decisions/categories/v65_intervention.txt'),'v65_us_mission = { icon = GFX_decision_generic_military allowed = { tag = SVN } visible = { has_global_flag = v65_us_active } }')
put(Path('common/decisions/v65_intervention.txt'),'''v65_us_mission = {
 v65_delay_us_withdrawal = { icon = generic_political_discourse cost = 120 days_re_enable = 180 available = { date > 1967.12.31 date < 1973.1.1 } complete_effect = { subtract_from_variable = { v65_us_withdraw_pressure = 15 } clamp_variable = { var = v65_us_withdraw_pressure min = 0 max = 100 } } ai_will_do = { factor = 1 } }
 v65_accept_us_withdrawal = { icon = generic_political_discourse cost = 0 available = { date > 1967.12.31 } complete_effect = { v65_withdraw_intervention = yes } ai_will_do = { factor = 0 } }
}''')
# Restore southern ownership and clear the obsolete neutral-zone history.
p=M/'history/states/10.txt';s=p.read_text().replace('owner = XTR','owner = SVN');p.write_text(s,encoding='utf-8')
p=M/'history/states/31.txt';s=p.read_text()
s=s.replace('361 = { naval_base = 2 }','361 = { naval_base = 3 coastal_bunker = 6 bunker = 4 }')
p.write_text(s,encoding='utf-8')
put(Path('common/on_actions/v65_island.txt'),'on_actions = { on_startup = { effect = { 31 = { add_dynamic_modifier = { modifier = v65_island_redoubt } } } } }')
for lang in ['simp_chinese','english']:put(Path(f'localisation/{lang}/zzzzzzzzzz_v65_intervention_l_{lang}.yml'),loc_text(L,lang))
print('Intervention: open 17th parallel, eight combat groups and four withdrawal-scaled support tiers')
