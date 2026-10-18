"""Political causality and a multi-front war for the 1965 campaign."""
from build_campaign import put,loc,CN,EN,M,R
from pathlib import Path
import re

put(Path('common/scripted_triggers/v65_campaign.txt'),'''v65_front_has_collapsed = {
 OR = {
  10 = { is_controlled_by = NVN }
  11 = { is_controlled_by = NVN }
  AND = { 19 = { is_controlled_by = FNL } 20 = { is_controlled_by = FNL } }
 }
}''')
put(Path('common/ideas/v65_campaign.txt'),'''ideas = { country = {
 v65_prepared_defence = { picture = generic_army_chief allowed = { always = no } modifier = { army_defence_factor = 0.10 max_dig_in = 3 } }
 v65_intelligence_network = { picture = generic_political_reform allowed = { always = no } modifier = { political_power_gain = 0.1 } }
 v65_guerrilla_network = { picture = generic_army_chief allowed = { always = no } modifier = { supply_consumption_factor = -0.12 army_speed_factor = 0.05 } }
 v65_regional_network = { picture = generic_political_reform allowed = { always = no } modifier = { stability_factor = 0.05 production_factory_efficiency_gain_factor = 0.05 } }
 v65_dmz_standoff = { picture = generic_army_chief allowed = { always = no } modifier = { army_attack_factor = -0.15 army_defence_factor = 0.15 } }
 v65_defeat_shock = { picture = generic_political_reform allowed = { always = no } modifier = { stability_factor = -0.10 political_power_gain = -0.15 } }
} }''')
put(Path('common/on_actions/v65.txt'),'''on_actions = {
 on_startup = { effect = {
  if = { limit = { SVN = { exists = yes NOT = { has_country_flag = v65_intro_seen } } }
   SVN = {
    set_country_flag = v65_intro_seen
    create_faction = V65_SOUTHERN_COALITION add_to_faction = PKS add_to_faction = DNM
    add_ideas = { v65_dmz_standoff v65_prepared_defence }
    country_event = { id = v65.1 days = 1 }
   }
   NVN = { create_faction = V65_LIBERATION_FRONT add_to_faction = FNL add_ideas = { v65_dmz_standoff v65_prepared_defence }
    declare_war_on = { target = SVN type = annex_everything }
    declare_war_on = { target = PKS type = annex_everything }
    declare_war_on = { target = DNM type = annex_everything }
   }
   FNL = {
    declare_war_on = { target = SVN type = annex_everything }
    declare_war_on = { target = PKS type = annex_everything }
    declare_war_on = { target = DNM type = annex_everything }
    add_ideas = v65_guerrilla_network
    set_province_controller = 243 set_province_controller = 287 set_province_controller = 316
    18 = { create_unit = { division = "name = \\"Highlands Cell\\" division_template = \\"Theater Infantry\\" start_equipment_factor = 0.65 location = 243" owner = FNL } }
    23 = { create_unit = { division = "name = \\"Tay Ninh Cell\\" division_template = \\"Theater Infantry\\" start_equipment_factor = 0.65 location = 287" owner = FNL } }
    27 = { create_unit = { division = "name = \\"Mekong Cell\\" division_template = \\"Theater Infantry\\" start_equipment_factor = 0.65 location = 316" owner = FNL } }
   }
   PKS = { add_ideas = v65_park_patron }
  }
 } }
}'''.replace('\\"','\"'))
# Quoted create_unit strings must retain the embedded escaped quotes.
p=M/'common/on_actions/v65.txt';s=p.read_text(encoding='utf-8-sig');
for name in ['Highlands Cell','Tay Ninh Cell','Mekong Cell','Theater Infantry']:
 s=s.replace('"'+name+'"','\\"'+name+'\\"')
p.write_text(s,encoding='utf-8')

p=M/'common/scripted_effects/v65_politics.txt';s=(R/'tools/politics_base.txt').read_text(encoding='utf-8-sig')
# Keep the proven loyalty/civil-war implementation, replace the old raid model.
s=s[:s.index('v65_launch_infiltration =')]
s=s.replace('set_country_flag = v65_coup_victory', 'set_country_flag = v65_coup_victory remove_ideas = v65_defeat_shock v65_duong_van_minh = { add_country_leader_role = { promote_leader = yes country_leader = { ideology = despotism expire = "1990.1.1" } } }')
s=s.replace('set_variable = { v65_infiltration = 0 }','set_variable = { v65_infiltration = 0 }')
s=s.replace('} } }\nv65_enact', '} } }\nv65_enact')
# The actual coup effect also enforces defeat; bypassing the decision is harmless.
start=s.index('v65_resolve_coup =');s=s[:start]+s[start:].replace('v65_resolve_coup = {','v65_resolve_coup = { if = { limit = { has_country_flag = v65_front_defeat }',1)
s+='\n}\n'
s+='''v65_check_front_defeat = {
 if = { limit = { has_war_with = NVN v65_front_has_collapsed = yes NOT = { has_country_flag = v65_front_defeat } }
  set_country_flag = v65_front_defeat set_country_flag = v65_crisis_active add_ideas = v65_defeat_shock
  country_event = { id = v65politics.1 days = 1 }
  PKS = { country_event = { id = v65campaign.1 days = 2 } }
  DNM = { country_event = { id = v65campaign.2 days = 2 } }
 }
}
v65_park_intervention = {
 if = { limit = { tag = PKS SVN = { has_country_flag = v65_front_defeat exists = yes } }
  leave_faction = yes set_country_flag = v65_park_march
  add_ideas = v65_guard_network
  declare_war_on = { target = SVN type = annex_everything }
  SVN = { country_event = { id = v65campaign.3 days = 1 } }
 }
}
v65_launch_infiltration = { FNL = {
 if = { limit = { has_war_with = SVN check_variable = { v65_infiltration > 0 } NVN = { check_variable = { v65_trail_level > 0 } } NOT = { has_country_flag = v65_raid_cooldown } }
  random_list = {
'''
for sid,pid in [(18,244),(20,269),(23,288),(24,300),(27,324)]:
 s+=f'   1 = {{ modifier = {{ factor = 0 NOT = {{ SVN = {{ controls_province = {pid} }} }} }} v65_raid_{sid} = yes }}\n'
s+='  }\n }\n} }\n'
for sid,pid in [(18,244),(20,269),(23,288),(24,300),(27,324)]:
 s+=f'''v65_raid_{sid} = {{ if = {{ limit = {{ tag = FNL has_war_with = SVN SVN = {{ controls_province = {pid} }} }}
 set_province_controller = {pid}
 {sid} = {{ create_unit = {{ division = "name = \\"Liberation Mobile Group\\" division_template = \\"Theater Infantry\\" start_experience_factor = 0.35 start_equipment_factor = 0.65 location = {pid}" owner = FNL count = 1 }} }}
 subtract_from_variable = {{ v65_infiltration = 1 }} NVN = {{ subtract_from_variable = {{ v65_trail_level = 1 }} }}
 set_country_flag = v65_raid_cooldown set_country_flag = v65_raid_fired
 country_event = {{ id = v65politics.8 days = 35 }} SVN = {{ country_event = {{ id = v65politics.6 days = 1 }} }}
}} }}\n'''
put(Path('common/scripted_effects/v65_politics.txt'),s)

decay='\n'.join(f'{i} = {{ if = {{ limit = {{ is_owned_by = SVN }} if = {{ limit = {{ SVN = {{ has_idea = v65_martial_law }} }} subtract_from_variable = {{ v65_loyalty = 2 }} }} else = {{ subtract_from_variable = {{ v65_loyalty = 5 }} }} clamp_variable = {{ var = v65_loyalty min = 0 max = 100 }} }} }}' for i in [23,24,26,27])
put(Path('common/on_actions/v65_politics.txt'),'''on_actions = {
 on_startup = { effect = { SVN = { v65_politics_init = yes } FNL = { if = { limit = { NOT = { has_country_flag = v65_organization_ready } } set_country_flag = v65_organization_ready set_variable = { v65_infiltration = 1 } } } PKS = { if = { limit = { NOT = { has_country_flag = v65_organization_ready } } set_country_flag = v65_organization_ready set_variable = { v65_park_influence = 0 } } } } }
 on_daily = { effect = { SVN = { v65_check_front_defeat = yes } } }
 on_weekly = { effect = {
  SVN = { if = { limit = { has_country_flag = v65_crisis_active NOT = { has_country_flag = v65_coup_resolved } }
'''+decay+''' } }
  FNL = { if = { limit = { is_ai = yes check_variable = { v65_infiltration > 0 } NVN = { check_variable = { v65_trail_level > 0 } } NOT = { has_country_flag = v65_raid_cooldown } } v65_launch_infiltration = yes } }
 } }
 on_monthly = { effect = {
  NVN = { if = { limit = { has_war_with = SVN } add_to_variable = { v65_trail_level = 1 } clamp_variable = { var = v65_trail_level min = 0 max = 5 } } }
  FNL = { if = { limit = { has_war_with = SVN NVN = { check_variable = { v65_trail_level > 0 } } } add_to_variable = { v65_infiltration = 1 } clamp_variable = { var = v65_infiltration min = 0 max = 3 } } }
 } }
}''')
p=M/'common/decisions/v65_politics.txt';s=p.read_text(encoding='utf-8-sig');s=s.replace('available = { controls_state = 25 }','available = { controls_state = 25 has_country_flag = v65_front_defeat }');p.write_text(s,encoding='utf-8')
put(Path('common/decisions/v65_trail.txt'),'''v65_trail = {
 v65_expand_trail = { icon = generic_prepare_civil_war cost = 60 visible = { tag = NVN } available = { check_variable = { v65_trail_level < 5 } } days_re_enable = 30 complete_effect = { add_to_variable = { v65_trail_level = 1 } add_ideas = v65_trail_network } ai_will_do = { factor = 1 } }
 v65_infiltrate = { icon = generic_prepare_civil_war cost = 50 visible = { OR = { tag = NVN tag = FNL } } available = { has_war_with = SVN FNL = { check_variable = { v65_infiltration > 0 } NOT = { has_country_flag = v65_raid_cooldown } } NVN = { check_variable = { v65_trail_level > 0 } } OR = { SVN = { controls_province = 244 } SVN = { controls_province = 269 } SVN = { controls_province = 288 } SVN = { controls_province = 300 } SVN = { controls_province = 324 } } } days_re_enable = 35 complete_effect = { v65_launch_infiltration = yes } ai_will_do = { factor = 1 } }
 v65_interdict = { icon = generic_prepare_civil_war cost = 65 visible = { OR = { tag = SVN tag = PKS tag = DNM } } available = { has_war_with = FNL NVN = { check_variable = { v65_trail_level > 0 } } } days_re_enable = 30 complete_effect = { NVN = { subtract_from_variable = { v65_trail_level = 1 } clamp_variable = { var = v65_trail_level min = 0 max = 5 } } FNL = { subtract_from_variable = { v65_infiltration = 1 } clamp_variable = { var = v65_infiltration min = 0 max = 3 } } } ai_will_do = { factor = 0.5 } }
}''')
put(Path('common/decisions/categories/v65_politics.txt'),'''v65_politics = { icon = GFX_decision_generic_military allowed = { tag = SVN } visible = { always = yes } }
v65_park = { icon = GFX_decision_generic_military allowed = { tag = PKS } visible = { always = yes } }
v65_trail = { icon = GFX_decision_generic_military allowed = { OR = { tag = SVN tag = NVN tag = FNL tag = PKS tag = DNM } } visible = { always = yes } }''')
put(Path('events/v65_campaign.txt'),'''add_namespace = v65campaign
country_event = { id = v65campaign.1 title = v65campaign.1.t desc = v65campaign.1.d picture = GFX_report_event_generic_read_write is_triggered_only = yes
 option = { name = v65campaign.1.a add_to_variable = { v65_park_influence = 1 } }
}
country_event = { id = v65campaign.2 title = v65campaign.2.t desc = v65campaign.2.d picture = GFX_report_event_generic_read_write is_triggered_only = yes
 option = { name = v65campaign.2.a add_stability = 0.03 }
 option = { name = v65campaign.2.b add_political_power = 50 add_stability = -0.03 }
}
country_event = { id = v65campaign.3 title = v65campaign.3.t desc = v65campaign.3.d picture = GFX_report_event_generic_read_write is_triggered_only = yes
 option = { name = v65campaign.3.a add_political_power = 50 }
}
''')
L={
'V65_SOUTHERN_COALITION':'南方防务协调会','V65_LIBERATION_FRONT':'民族解放联合阵线',
'v65_prepared_defence':'纵深防御准备','v65_intelligence_network':'常设情报联络网','v65_guerrilla_network':'南方游击网络','v65_regional_network':'归仁军政网络','v65_dmz_standoff':'十七度线对峙','v65_defeat_shock':'前线溃败的政治冲击',
'v65_requires_front_defeat':'前线败局已经动摇政府：广治或顺化失守，或南方芽庄与大叻同时被解放阵线控制。',
'v65campaign.1.t':'败报传到归仁','v65campaign.1.d':'西贡正在追究前线失利的责任。驻军开始寻找可靠的盟友，而朴世诚收到的联络也不再只是运输和补给。要维持联盟，还是把危机变成自己的机会？','v65campaign.1.a':'先确认哪些部队还听从命令。',
'v65campaign.2.t':'西贡的命令彼此矛盾','v65campaign.2.d':'前线失利后，不同派系向岘港发来了不同的命令。军区必须先保证防区不出现真空，再决定如何回应首都。','v65campaign.2.a':'先稳住前线与港口。','v65campaign.2.b':'要求中央重新确认军费与权限。',
'v65campaign.3.t':'归仁部队宣布进军','v65campaign.3.d':'朴世诚以恢复秩序为由，宣布不再接受西贡现有指挥体系。沿海联盟的裂缝已经变成新的战线；首都驻军的态度将决定政府还能否继续运转。','v65campaign.3.a':'保住首都的通信与驻军。',
'v65politics.1.t':'败报之后：谁来负责？','v65politics.1.d':'前线防线失守，责任之争涌入总统府。军官开始互相指责，广播台、总参谋部和周边驻军的服从也不再理所当然。花费政治点争取首都周边驻军；支持不足而强行摊牌，将引发内战。',
'v65politics.6.d':'南方地下组织利用秘密运输线建立了新的武装据点。这是一支真实出现于后方的解放阵线部队；北线调兵无法自动解决乡村与交通线的威胁。',
'v65_trail_desc':'北方通道等级：[NVN.v65_trail_level|0]。南方可动员次数：[FNL.v65_infiltration|0]。每月恢复通道和组织能力；解放阵线可在南方腹地建立据点，北越玩家也可代为组织。',
'v65_infiltrate_desc':'消耗南方组织能力与北方通道储备，在仍由西贡控制的目标省份建立一支真实的解放阵线部队。目标从邦美蜀、大叻、西宁、边和与美萩的后方地块中选择。',
'v65_coup_desc':'必须先发生前线溃败。争取西宁、边和、头顿、美萩驻军后再行动：三处支持足够则和平夺权，一至两处可能引发内战，没有支持则政变失败。',
}
for lang in ['simp_chinese','english']:
 # These specific overlays intentionally replace the 0.3 introductory strings.
 put(Path(f'localisation/{lang}/zzzzz_v65_mechanics_l_{lang}.yml'),'l_'+lang+':\n'+'\n'.join(f' {k}:0 "{v}"' for k,v in L.items()))

# Remove ARVN units accidentally placed on newly autonomous territory. FNL's
# initial isolated cells are spawned only after their provinces change control.
owners={}
for p in (M/'history/states').glob('*.txt'):
 s=p.read_text(encoding='utf-8-sig');owner=re.search(r'owner = (\w+)',s)[1]
 for n in re.search(r'provinces = \{([^}]+)',s)[1].split():owners[int(n)]=owner
for tag in ['SVN','FNL']:
 p=M/f'history/units/{tag}_1965.txt';s=p.read_text(encoding='utf-8-sig')
 s=re.sub(r'division = \{[^{}]+\}',lambda m:m[0] if owners[int(re.search(r'location = (\d+)',m[0])[1])]==tag else '',s)
 p.write_text('\n'.join(line.rstrip() for line in s.splitlines()).rstrip()+'\n',encoding='utf-8')
print('Multi-front setup, defeat-triggered coup and Park intervention authored')
