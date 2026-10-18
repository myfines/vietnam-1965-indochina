"""A neutral supervised DMZ, allied intervention and a staged withdrawal."""
from pathlib import Path
from build_campaign import M,put
from long_foundation import REGIONS,loc_text

L={
 'v65_us_mission':'美军干涉与撤军安排',
 'v65_us_mission_desc':'美军撤军压力：[?SVN.v65_us_withdraw_pressure|0]/100。1968年起每月增加3，达到100或进入1973年撤走。\n广治划为中立监督区：南北双方都不能通过中立区开战推进。撤军时归还南越，正面战线重新开放。',
 'v65_us_firepower':'美军干涉：空中与火力支援',
 'v65_us_firepower_desc':'美军驻越战斗群以盟军单位编制表示，驻防顺化、西贡与富国岛。配套火力提高盟军防御、组织与补给能力。广治由中立监督机构隔开南北，不允许部队直接北上。此效果随撤军结束。',
 'v65_island_redoubt':'富国岛海上基地',
 'v65_island_redoubt_desc':'岛屿没有陆地通道。港口、岸防与留守部队构成离岛基地；西贡失守时提前启用独立指挥，避免随大陆投降直接移交。仍可遭受实际海上登陆。',
 'v65_delay_us_withdrawal':'用新一轮捷报争取延后撤军',
 'v65_delay_us_withdrawal_desc':'120政治点，撤军压力-15，每180天一次。只能在1968—1972年办理；不能无限延后1973年的最终撤军。',
 'v65_accept_us_withdrawal':'接受提前撤军与装备交接',
 'v65_accept_us_withdrawal_desc':'1968年后可选择提前结束支援。广治恢复南越所有权，正面重新开放，获得1200支步枪和150辆卡车。',
 'v65us.1.t':'干涉部队的作战边界',
 'v65us.1.d':'美方接下了火力与驻防任务，但不批准部队越过监督区。北边暂时不会一路压到西贡，南边的游击队仍要另找办法。',
 'v65us.1.a':'把这条界线画清楚。',
 'v65us.2.t':'撤军，交表',
 'v65us.2.d':'美方撤去额外火力保障，留下移交清单。广治监督区解除，南北正面重新接上。仓库里有什么，接收人签字。',
 'v65us.2.a':'先把库存领走。',
 'V65_STATE_10':'十七度线监督区',
}
effects='''v65_begin_intervention = {
 if = { limit = { NOT = { has_global_flag = v65_us_initialized } } set_global_flag = v65_us_initialized set_global_flag = v65_us_active
  XTR = { transfer_state = 10 } 10 = { set_demilitarized_zone = yes set_state_flag = v65_supervised_dmz }
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
  every_country = { remove_ideas = v65_us_firepower delete_unit_template_and_units = { division_template = "US Intervention Group" disband = no } }
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
effects=effects.replace('division_template = \\"Theater Infantry\\"','division_template = \\"US Intervention Group\\"')
p=M/'history/units/SVN_1965.txt'
template=p.read_text(encoding='utf-8').split('\n',1)[0].replace('"Theater Infantry"','"US Intervention Group" is_locked = yes')
p.write_text(template+'\n'+p.read_text(encoding='utf-8'),encoding='utf-8')
put(Path('common/scripted_effects/v65_intervention.txt'),effects)
allies=['SVN','PKS','DNM',*REGIONS]
support=' '.join(f'{t} = {{ if = {{ limit = {{ exists = yes NOT = {{ has_country_flag = v65_rebel_command }} '+('' if t=='SVN' else 'is_in_faction_with = SVN NOT = { has_war_with = SVN }')+' } add_ideas = v65_us_firepower } else = { remove_ideas = v65_us_firepower } }' for t in allies)
put(Path('common/on_actions/v65_intervention.txt'),'''on_actions = { on_startup = { effect = { SVN = { v65_begin_intervention = yes } } }
 on_daily = { effect = { if = { limit = { has_global_flag = v65_us_active } SUPPORT }
 SVN = { if = { limit = { exists = yes } v65_evacuate_island = yes } }
 if = { limit = { has_global_flag = v65_us_active OR = { date > 1972.12.31 SVN = { check_variable = { v65_us_withdraw_pressure > 99 } } } } SVN = { v65_withdraw_intervention = yes } }
 } }
 on_monthly = { effect = { if = { limit = { has_global_flag = v65_us_active date > 1967.12.31 } SVN = { add_to_variable = { v65_us_withdraw_pressure = 3 } clamp_variable = { var = v65_us_withdraw_pressure min = 0 max = 100 } } } } }
}'''.replace('SUPPORT',support))
put(Path('common/ideas/v65_intervention.txt'),'ideas = { country = { v65_us_firepower = { picture = generic_army_chief allowed = { always = no } modifier = { army_defence_factor = 1 army_org_factor = 0.5 supply_consumption_factor = -0.3 army_attack_factor = 0.35 } } } }')
put(Path('common/dynamic_modifiers/v65_island.txt'),'v65_island_redoubt = { icon = 1 enable = { always = yes } local_supplies = 2 }')
put(Path('events/v65_intervention.txt'),'add_namespace = v65us\n'+'\n'.join(f'country_event = {{ id = v65us.{n} is_triggered_only = yes title = v65us.{n}.t desc = v65us.{n}.d picture = GFX_report_event_generic_read_write option = {{ name = v65us.{n}.a }} }}' for n in [1,2]))
put(Path('common/decisions/categories/v65_intervention.txt'),'v65_us_mission = { icon = GFX_decision_generic_military allowed = { tag = SVN } visible = { has_global_flag = v65_us_active } }')
put(Path('common/decisions/v65_intervention.txt'),'''v65_us_mission = {
 v65_delay_us_withdrawal = { icon = generic_political_discourse cost = 120 days_re_enable = 180 available = { date > 1967.12.31 date < 1973.1.1 } complete_effect = { subtract_from_variable = { v65_us_withdraw_pressure = 15 } clamp_variable = { var = v65_us_withdraw_pressure min = 0 max = 100 } } ai_will_do = { factor = 1 } }
 v65_accept_us_withdrawal = { icon = generic_political_discourse cost = 0 available = { date > 1967.12.31 } complete_effect = { v65_withdraw_intervention = yes } ai_will_do = { factor = 0 } }
}''')
# Native history holds the neutral region from the first frame, before startup actions.
p=M/'history/states/10.txt';s=p.read_text().replace('owner = SVN','owner = XTR');p.write_text(s,encoding='utf-8')
p=M/'history/states/31.txt';s=p.read_text()
s=s.replace('361 = { naval_base = 2 }','361 = { naval_base = 3 coastal_bunker = 6 bunker = 4 }')
p.write_text(s,encoding='utf-8')
put(Path('common/on_actions/v65_island.txt'),'on_actions = { on_startup = { effect = { 31 = { add_dynamic_modifier = { modifier = v65_island_redoubt } } } } }')
for lang in ['simp_chinese','english']:put(Path(f'localisation/{lang}/zzzzzzzzzz_v65_intervention_l_{lang}.yml'),loc_text(L,lang))
print('Intervention: neutral 17th parallel, eight allied combat groups, staged withdrawal and island refuge')
