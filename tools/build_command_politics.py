"""Selectable military jurisdictions, central prestige and Park's patronage network."""
from pathlib import Path
from build_campaign import put, M
from long_foundation import REGIONS, loc_text

put(Path('common/scripted_triggers/v65_command.txt'), '''v65_under_central_command = {
 OR = { is_subject_of = SVN has_country_flag = v65_central_command_contract }
 NOT = { has_country_flag = v65_rebel_command }
}''')

L = {
 'v65_command_politics': '中央、军区与私人势力',
 'v65_command_politics_desc': '中央威望：[?SVN.v65_central_prestige|0]/100\n本军区忠诚：[?v65_regional_loyalty|0]/100\n朴系人脉：[?PKS.v65_personal_network|0]/10\n威望低于30且军区忠诚低于25时，军区可以抗命；抗命后可逼宫或起兵。',
 'v65_fund_command': '补发军饷，确认指挥关系',
 'v65_fund_command_desc': '消耗75政治点。中央威望增加8，各附属军区忠诚增加8。每90天一次。',
 'v65_park_recruit_clients': '安插军需与军官联系人',
 'v65_park_recruit_clients_desc': '消耗50政治点。朴系人脉增加1，影响力增加1。上限10，每60天一次。',
 'v65_park_build_retinue': '通过关系扩充直属部队',
 'v65_park_build_retinue_desc': '需要2点人脉与完整控制的驻地。消耗75政治点，在当前首都组建一个直属步兵团；每90天一次。',
 'v65_park_request_command': '用部队与补给换取指挥权',
 'v65_park_request_command_desc': '需要3点人脉。消耗75政治点，影响力增加2，南越中央威望降低5。每120天一次。',
 'v65_park_takeover': '要求接管南越中央',
 'v65_park_takeover_desc': '需要至少6点人脉、5点影响力，南越中央威望低于40且仍控制首都。南越可以接受，也可以拒绝；拒绝后朴可另走已有的军事干预路线。',
 'v65_park_inside': '朴系掌握实际指挥权',
 'v65_park_inside_desc': '南越名义政府保留，朴系控制跨军区指挥与补给任命。军区忠诚仍须维持。',
 'v65_central_respected': '中央命令仍然有效',
 'v65_central_respected_desc': '中央威望不低于65。每日政治点增加0.10，计划速度增加5%。',
 'v65_central_discredited': '各军区自行其是',
 'v65_central_discredited_desc': '中央威望低于30。每日政治点减少0.15，计划速度降低10%；低忠诚军区可以抗命。',
 'v65command.1.t': '军区要求改组中央',
 'v65command.1.d': '军区拒绝调兵，要求总统府交出部分军饷与任命权。接受会保住现有指挥关系；拒绝后，军区可以退让或起兵。',
 'v65command.1.a': '承认既成事实，拨款续约。',
 'v65command.1.b': '拒绝，维持原命令。',
 'v65command.2.t': '中央拒绝让步',
 'v65command.2.d': '总统府要求立即恢复调度。司令部需要决定是否继续服从。',
 'v65command.2.a': '解除隶属，起兵反对中央。',
 'v65command.2.b': '暂时服从。',
 'v65command.3.t': '朴要求接管指挥系统',
 'v65command.3.d': '朴系已在军官、军需和地方部队中建立关系网。朴提出接管跨区调度，保留南越政府名义。',
 'v65command.3.a': '接受，合并远征集团。',
 'v65command.3.b': '拒绝。',
}

effects = '''v65_refresh_command = {
 clamp_variable = { var = v65_central_prestige min = 0 max = 100 }
 remove_ideas = { v65_central_respected v65_central_discredited }
 if = { limit = { check_variable = { v65_central_prestige > 64 } } add_ideas = v65_central_respected }
 else_if = { limit = { check_variable = { v65_central_prestige < 30 } } add_ideas = v65_central_discredited }
}
v65_park_build_retinue = {
 if = { limit = { tag = PKS check_variable = { v65_personal_network > 1 } capital_scope = { is_fully_controlled_by = PKS } }
  capital_scope = { create_unit = { division = "name = \\"Park Guard Regiment\\" division_template = \\"Theater Infantry\\" start_equipment_factor = 0.8 start_experience_factor = 0.3" owner = PKS } }
 }
}
v65_command_month = {
 if = { limit = { tag = SVN }
  if = { limit = { has_country_flag = v65_front_defeat } subtract_from_variable = { v65_central_prestige = 3 } }
  else_if = { limit = { controls_state = 25 } add_to_variable = { v65_central_prestige = 1 } }
  if = { limit = { NOT = { controls_state = 25 } } subtract_from_variable = { v65_central_prestige = 5 } }
  v65_refresh_command = yes
 }
}
'''
decisions = '''v65_command_politics = {
 v65_fund_command = { icon = generic_political_discourse cost = 75 visible = { tag = SVN } days_re_enable = 90
 complete_effect = { add_to_variable = { v65_central_prestige = 8 }
'''
for tag in REGIONS:
    decisions += f'if = {{ limit = {{ {tag} = {{ exists = yes is_subject_of = SVN }} }} {tag} = {{ add_to_variable = {{ v65_regional_loyalty = 8 }} clamp_variable = {{ var = v65_regional_loyalty min = 0 max = 100 }} }} }}\n'
decisions += 'v65_refresh_command = yes } ai_will_do = { factor = 1 } }\n'

for tag, (cn, _, capital, states, *_) in REGIONS.items():
    L['v65_commission_' + tag] = '设立' + cn
    L['v65_commission_' + tag + '_desc'] = '消耗50政治点，将预设辖区内完整控制的地区移交军区。该军区单独设立，不要求同时下放其他地区。'
    decisions += f'''v65_commission_{tag} = {{ icon = generic_political_discourse cost = 50 visible = {{ tag = SVN {tag} = {{ exists = no }} }}
 available = {{ owns_state = {capital} {capital} = {{ is_fully_controlled_by = SVN }} }}
 complete_effect = {{ v65_devolve_{tag} = yes add_ideas = v65_decentralized_command subtract_from_variable = {{ v65_central_prestige = 2 }} v65_refresh_command = yes }} ai_will_do = {{ factor = 0 }} }}
'''
    L['v65_select_district_' + tag] = '调整' + cn + '辖区'
    L['v65_select_district_' + tag + '_desc'] = '展开该军区的州划转列表，其他军区的划转列表收起。'
    selection = ' '.join('clr_country_flag = v65_selected_' + other for other in REGIONS)
    decisions += f'''v65_select_district_{tag} = {{ icon = generic_political_discourse cost = 0
 visible = {{ tag = SVN {tag} = {{ exists = yes v65_under_central_command = yes }} NOT = {{ has_country_flag = v65_selected_{tag} }} }}
 complete_effect = {{ {selection} set_country_flag = v65_selected_{tag} }} ai_will_do = {{ factor = 0 }} }}
'''
    # Expand jurisdiction one fully held mainland state at a time; no compulsory mass release.
    for sid in range(11, 32):
        if sid in [capital, 25]:
            continue
        key = f'v65_assign_{tag}_{sid}'
        L[key] = f'将$V65_STATE_{sid}$划归{cn}'
        L[key + '_desc'] = '消耗25政治点。移交完整控制的地区，军区忠诚增加3。交战或叛离的军区不能接收划区。'
        decisions += f'''{key} = {{ icon = generic_political_discourse cost = 25
 visible = {{ tag = SVN has_country_flag = v65_selected_{tag} owns_state = {sid} {tag} = {{ exists = yes is_subject_of = SVN }} }}
 available = {{ {sid} = {{ is_fully_controlled_by = SVN }} NOT = {{ has_war_with = {tag} }} }}
 complete_effect = {{ {sid} = {{ add_core_of = {tag} }} {tag} = {{ transfer_state = {sid} set_state_controller = {sid} add_to_variable = {{ v65_regional_loyalty = 3 }} }} }} ai_will_do = {{ factor = 0 }} }}
'''
    effects += f'''v65_dissent_{tag} = {{
 if = {{ limit = {{ tag = {tag} is_subject_of = SVN SVN = {{ exists = yes check_variable = {{ v65_central_prestige < 30 }} }} check_variable = {{ v65_regional_loyalty < 25 }} }} set_country_flag = v65_command_refused }}
}}
v65_rebel_{tag} = {{
 if = {{ limit = {{ tag = {tag} is_subject_of = SVN has_country_flag = v65_command_refused NOT = {{ has_war_with = SVN }} SVN = {{ exists = yes }} }}
  if = {{ limit = {{ is_subject_of = SVN }} SVN = {{ set_autonomy = {{ target = {tag} autonomy_state = autonomy_free }} }} }}
  SVN = {{ subtract_from_variable = {{ v65_central_prestige = 10 }} v65_refresh_command = yes }}
  clr_country_flag = v65_central_command_contract
  set_country_flag = v65_rebel_command country_event = {{ id = v65command.10 days = 3 }}
 }}
}}
'''
    for action, text, effect, cost in [
        ('refuse', '拒绝中央调令', f'v65_dissent_{tag} = yes', 25),
        ('petition', '要求中央改组', 'SVN = { country_event = { id = v65command.1 days = 1 } }', 50),
        ('rebel', '起兵反对中央', f'v65_rebel_{tag} = yes', 100),
    ]:
        key = f'v65_{action}_{tag}'
        L[key] = text
        L[key + '_desc'] = '需要中央威望低于30、军区忠诚低于25。先拒令，之后可逼宫或起兵。起兵将解除附属和同盟关系，与中央开战。'
        extra = 'NOT = { has_country_flag = v65_command_refused }' if action == 'refuse' else 'has_country_flag = v65_command_refused'
        decisions += f'''{key} = {{ icon = generic_prepare_civil_war cost = {cost} visible = {{ tag = {tag} is_subject_of = SVN }}
 available = {{ SVN = {{ exists = yes check_variable = {{ v65_central_prestige < 30 }} }} check_variable = {{ v65_regional_loyalty < 25 }} {extra} }}
 days_re_enable = 120 complete_effect = {{ {effect} }} ai_will_do = {{ factor = {1 if action != 'rebel' else 0.2} }} }}
'''

decisions += '''v65_park_recruit_clients = { icon = generic_political_discourse cost = 50 visible = { tag = PKS }
 available = { check_variable = { v65_personal_network < 10 } } days_re_enable = 60
 complete_effect = { add_to_variable = { v65_personal_network = 1 } add_to_variable = { v65_park_influence = 1 } } ai_will_do = { factor = 1 } }
 v65_park_build_retinue = { icon = generic_prepare_civil_war cost = 75 visible = { tag = PKS }
 available = { check_variable = { v65_personal_network > 1 } capital_scope = { is_fully_controlled_by = PKS } } days_re_enable = 90
 complete_effect = { v65_park_build_retinue = yes } ai_will_do = { factor = 0.5 } }
 v65_park_request_command = { icon = generic_political_discourse cost = 75 visible = { tag = PKS }
 available = { check_variable = { v65_personal_network > 2 } is_in_faction_with = SVN NOT = { has_war_with = SVN } SVN = { exists = yes } } days_re_enable = 120
 complete_effect = { add_to_variable = { v65_park_influence = 2 } SVN = { subtract_from_variable = { v65_central_prestige = 5 } v65_refresh_command = yes } } ai_will_do = { factor = 0.5 } }
 v65_park_takeover = { icon = generic_prepare_civil_war cost = 100 visible = { tag = PKS }
 available = { check_variable = { v65_personal_network > 5 } SVN = { check_variable = { v65_central_prestige < 40 } } v65_can_offer_union = yes }
 days_re_enable = 180 complete_effect = { set_country_flag = v65_union_pending SVN = { country_event = { id = v65command.3 days = 1 } } } ai_will_do = { factor = 1 } }
}
'''
events = '''add_namespace = v65command
country_event = { id = v65command.10 hidden = yes is_triggered_only = yes immediate = {
 if = { limit = { has_country_flag = v65_rebel_command }
  if = { limit = { has_war_with = NVN } white_peace = NVN }
  if = { limit = { has_war_with = FNL } white_peace = FNL }
  country_event = { id = v65command.11 days = 3 }
 }
} }
country_event = { id = v65command.11 hidden = yes is_triggered_only = yes immediate = {
 if = { limit = { has_country_flag = v65_rebel_command }
  SVN = { if = { limit = { is_in_faction_with = ROOT } remove_from_faction = ROOT } }
  country_event = { id = v65command.12 days = 3 }
 }
} }
country_event = { id = v65command.12 hidden = yes is_triggered_only = yes immediate = {
 if = { limit = { has_country_flag = v65_rebel_command exists = yes NOT = { is_subject_of = SVN } NOT = { is_in_faction_with = SVN } NOT = { has_war_with = SVN } SVN = { exists = yes } } declare_war_on = { target = SVN type = annex_everything } }
} }
country_event = { id = v65command.1 is_triggered_only = yes title = v65command.1.t desc = v65command.1.d picture = GFX_report_event_generic_read_write
 option = { name = v65command.1.a ai_chance = { factor = 60 } add_political_power = -75 subtract_from_variable = { v65_central_prestige = 5 } FROM = { add_to_variable = { v65_regional_loyalty = 25 } clr_country_flag = v65_command_refused } v65_refresh_command = yes }
 option = { name = v65command.1.b ai_chance = { factor = 40 } FROM = { country_event = { id = v65command.2 days = 3 } } }
}
country_event = { id = v65command.2 is_triggered_only = yes title = v65command.2.t desc = v65command.2.d picture = GFX_report_event_generic_read_write
 option = { name = v65command.2.a ai_chance = { factor = 50 } REBEL_EFFECTS }
 option = { name = v65command.2.b ai_chance = { factor = 50 } clr_country_flag = v65_command_refused add_to_variable = { v65_regional_loyalty = 15 } SVN = { add_to_variable = { v65_central_prestige = 5 } v65_refresh_command = yes } }
}
country_event = { id = v65command.3 is_triggered_only = yes title = v65command.3.t desc = v65command.3.d picture = GFX_report_event_generic_read_write
 immediate = { PKS = { clr_country_flag = v65_union_pending } }
 option = { name = v65command.3.a ai_chance = { factor = 55 } v65_finalize_union = yes if = { limit = { has_country_flag = v65_union_complete } add_ideas = v65_park_inside set_variable = { v65_central_prestige = 45 } v65_refresh_command = yes } }
 option = { name = v65command.3.b ai_chance = { factor = 45 } PKS = { clr_country_flag = v65_union_pending set_country_flag = v65_union_refused country_event = { id = v65routes.3 days = 90 } } }
}
'''.replace('REBEL_EFFECTS', ' '.join(f'v65_rebel_{tag} = yes' for tag in REGIONS))

monthly = 'SVN = { if = { limit = { exists = yes } v65_command_month = yes } }\n'
for tag in REGIONS:
    monthly += f'''{tag} = {{ if = {{ limit = {{ exists = yes is_subject_of = SVN }}
 if = {{ limit = {{ SVN = {{ check_variable = {{ v65_central_prestige < 40 }} }} }} subtract_from_variable = {{ v65_regional_loyalty = 5 }} }}
 else_if = {{ limit = {{ SVN = {{ check_variable = {{ v65_central_prestige > 64 }} }} }} add_to_variable = {{ v65_regional_loyalty = 2 }} }}
 clamp_variable = {{ var = v65_regional_loyalty min = 0 max = 100 }} v65_dissent_{tag} = yes }} }}\n'''
monthly = monthly.replace('is_subject_of = SVN', 'v65_under_central_command = yes')
# Contractual command permits military districts to leave the common war in stages.
# A puppet-to-free transition during a shared live front causes native theatre assertions.
for tag in REGIONS:
    effects = effects.replace(f'tag = {tag} is_subject_of = SVN', f'tag = {tag} v65_under_central_command = yes')
decisions = decisions.replace('is_subject_of = SVN', 'v65_under_central_command = yes')
put(Path('common/on_actions/v65_command.txt'), '''on_actions = { on_startup = { effect = {
 SVN = { if = { limit = { NOT = { has_country_flag = v65_command_initialized } } set_country_flag = v65_command_initialized set_variable = { v65_central_prestige = 55 } v65_refresh_command = yes } }
} } on_monthly = { effect = { ''' + monthly + '} } }')
put(Path('common/scripted_effects/v65_command.txt'), effects)
put(Path('common/decisions/v65_command.txt'), decisions)
put(Path('events/v65_command.txt'), events)
put(Path('common/decisions/categories/v65_command.txt'), 'v65_command_politics = { icon = GFX_decision_generic_military allowed = { OR = { tag = SVN tag = PKS '+ ' '.join('tag = '+tag for tag in REGIONS) +' } } visible = { always = yes } }')
put(Path('common/ideas/v65_command.txt'), '''ideas = { country = {
 v65_central_respected = { picture = generic_political_reform allowed = { always = no } modifier = { political_power_gain = 0.10 planning_speed = 0.05 } }
 v65_central_discredited = { picture = generic_political_reform allowed = { always = no } modifier = { political_power_gain = -0.15 planning_speed = -0.10 } }
 v65_park_inside = { picture = v65_park_shadow_ruler allowed = { always = no } modifier = { planning_speed = 0.05 } }
} }''')
for lang in ['simp_chinese', 'english']:
    put(Path(f'localisation/{lang}/zzzzzzz_v65_command_l_{lang}.yml'), loc_text(L, lang))
print('Central prestige, individual commands and Park patronage authored')
