"""ROK Taeguk troops and ROC military liaison in the fictional Vietnam theater."""
from pathlib import Path
from build_campaign import M,put
from long_foundation import loc_text

L={
 'v65_allied_missions':'太极旗与驻越国军',
 'v65_allied_missions_desc':'韩军由朴系人脉、军需信用及参谋本部渠道调动；台湾国军以顾问、通信与驻越分遣队介入。两者独立于美军撤军。台湾、韩国本土不加入战区地图。',
 'v65_rok_liaison':'太极旗：驻越韩军联络处',
 'v65_rok_liaison_desc':'朴系保留韩军联络与增援渠道。现有韩军付费增援仍消耗军需信用，并受参谋本部派系争夺影响。',
 'v65_roc_mission':'台湾国军驻越顾问团',
 'v65_roc_mission_desc':'通信、训练和小规模分遣队共同支援南越。计划速度+10%、训练时间-5%。任务部队使用国军专属编制，美军撤离不会将其删除。',
 'v65_request_roc':'向台湾申请国军分遣队',
 'v65_request_roc_desc':'80政治点，每180天一次，最多3次。需要完整控制首都及顾问团渠道；在首都增派一支国军分遣队。',
 'v65allies.1.t':'另一张军援清单',
 'v65allies.1.d':'韩国联络处和台湾顾问团各送来一份名单。人员、通信和训练有现成安排；军饷与补给分开结算。美方的撤军表不负责替他们签字。',
 'v65allies.1.a':'分别建账。',
}
effects='''v65_begin_allied_missions = {
 if = { limit = { NOT = { has_global_flag = v65_allies_initialized } } set_global_flag = v65_allies_initialized
  PKS = { add_ideas = v65_rok_liaison capital_scope = { create_unit = { division = "name = \\"ROK Taeguk Expeditionary Group\\" division_template = \\"Theater Infantry\\" start_equipment_factor = 1 start_experience_factor = 0.6" owner = PREV } } }
  SVN = { add_ideas = v65_roc_mission 25 = { create_unit = { division = "name = \\"ROC Vietnam Detachment\\" division_template = \\"ROC Vietnam Detachment\\" start_equipment_factor = 1 start_experience_factor = 0.5" owner = SVN count = 2 } } country_event = { id = v65allies.1 days = 7 } }
 }
}
v65_send_roc_detachment = { if = { limit = { has_idea = v65_roc_mission capital_scope = { is_fully_controlled_by = PREV } } capital_scope = { create_unit = { division = "name = \\"ROC Vietnam Detachment\\" division_template = \\"ROC Vietnam Detachment\\" start_equipment_factor = 0.9 start_experience_factor = 0.4" owner = PREV } } add_to_variable = { v65_roc_calls = 1 } } }
'''
p=M/'history/units/SVN_1965.txt'
template=next(line for line in p.read_text().splitlines() if line.startswith('division_template') and '"Theater Infantry"' in line)
p.write_text(template.replace('"Theater Infantry"','"ROC Vietnam Detachment" is_locked = yes')+'\n'+p.read_text(),encoding='utf-8')
put(Path('common/scripted_effects/v65_allied_missions.txt'),effects)
put(Path('common/on_actions/v65_allied_missions.txt'),'on_actions = { on_startup = { effect = { SVN = { v65_begin_allied_missions = yes } } } }')
put(Path('common/ideas/v65_allied_missions.txt'),'ideas = { country = { v65_rok_liaison = { picture = generic_army_chief allowed = { always = no } modifier = { command_power_gain_mult = 0.1 } } v65_roc_mission = { picture = generic_army_chief allowed = { always = no } modifier = { planning_speed = 0.1 training_time_factor = -0.05 } } } }')
put(Path('common/decisions/categories/v65_allied_missions.txt'),'v65_allied_missions = { icon = GFX_decision_generic_military allowed = { OR = { tag = SVN tag = PKS } } visible = { always = yes } }')
put(Path('common/decisions/v65_allied_missions.txt'),'v65_allied_missions = { v65_request_roc = { icon = generic_prepare_civil_war cost = 80 days_re_enable = 180 visible = { tag = SVN } available = { has_idea = v65_roc_mission check_variable = { v65_roc_calls < 3 } capital_scope = { is_fully_controlled_by = ROOT } } complete_effect = { v65_send_roc_detachment = yes } ai_will_do = { factor = 0.5 } } }')
put(Path('events/v65_allied_missions.txt'),'add_namespace = v65allies\ncountry_event = { id = v65allies.1 is_triggered_only = yes title = v65allies.1.t desc = v65allies.1.d picture = GFX_report_event_generic_read_write option = { name = v65allies.1.a } }')
p=M/'common/scripted_effects/v65_union_sanctuary.txt'
p.write_text(p.read_text().replace('annex_country = {','if = { limit = { PKS = { has_idea = v65_rok_liaison } } add_ideas = v65_rok_liaison } annex_country = {',1),encoding='utf-8')
for lang in ['simp_chinese','english']:put(Path(f'localisation/{lang}/zzzzzzzzzzz_v65_allies_l_{lang}.yml'),loc_text(L,lang))
print('Allied missions: Taeguk force, ROC advisors, two ROC detachments and a reinforcement channel')
