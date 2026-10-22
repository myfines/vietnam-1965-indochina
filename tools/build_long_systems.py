"""Durable institutions, civilian trust, fatigue and local security decisions."""
from build_campaign import put,M
from build_long_world import city,provinces
from long_foundation import REGIONS,ALL,loc_text
from pathlib import Path

L={
 'v65_prepared_defence_desc':'工兵、交通壕与预设火力为守军争取准备时间。防御收益需要有部队守住道路与补给节点，不能替代实际驻防。',
 'v65_intelligence_network_desc':'地方联络员、无线电与核实战报的人员组成通信网络。相关国策进一步建设剧情情报能力，截报决议用于降低地方叛乱压力。',
 'v65_guerrilla_network_desc':'解放阵线依靠村庄、隐蔽仓库与联络线维持分散作战。胡志明小道决议能够在南方政府或自治军区后方建立真实的武装据点。',
 'v65_regional_network_desc':'各地司令通过军饷、人事与军需互相联系。地方关系能够支持作战，也使中央命令必须经过更多协商。',
 'v65_dmz_standoff_desc':'十七度线附近的阵地、工事和补给布局有利于长期防御。正面进攻代价较高，双方仍能通过集中兵力取得突破。',
 'v65_defeat_shock_desc':'前线失利动摇政府威信与军官信心。首都周边驻军开始重新计算支持对象，政治决议可以争取他们，败局也可能引出政变。',
 'v65_martial_law_desc':'政府宣布全国戒严，非军事区除外。军警加强控制以维持政治支持，但强制命令无法代替地方合作或改变前线败局。',
 'v65_guard_network_desc':'首都警卫与驻军联络构成政治支点。它有助于维持命令链，政变结果仍取决于西宁、边和、头顿与美萩驻军的支持。',
 'v65_trail_network_desc':'隐蔽道路、仓库与转运站连接北方物资和南方游击组织。通道等级与组织准备决定敌后行动能力，南方可使用截断通道决议削弱它。',
 'v65_civil_admin_desc':'地方行政负责采购、请愿、征募和战争中的日常秩序。持续兑现保护与补偿承诺，可以减轻军警和村庄之间的矛盾。',
 'v65_story_governance':'案头的战争：人物、情报与地方社会',
 'v65_story_governance_desc':'民心：[?v65_public_trust|0]　派系依赖：[?v65_patronage|0]　战争疲劳：[?v65_war_fatigue|0]\n本地叛乱压力：[?v65_local_unrest|0]/10　剧情情报能力：[?v65_intelligence|0]/5\n军区对中央忠诚：[?v65_regional_loyalty|0]。人物关系（西贡）：朴世诚[?SVN.v65_park_trust|0]、阮文绍[?SVN.v65_thieu_trust|0]、岛上议会[?SVN.v65_island_trust|0]。机构等级最高五级；民心和疲劳会形成国家精神。情报由剧情决议处理，无需原版特工系统。',
 'v65_decentralized_command':'军区自治体制','v65_local_command':'本地军政司令部','v65_reintegrated_command':'重新签署的战区协定','v65_jungle_revolution':'丛林革命根据地',
 'v65_social_mandate':'愿意合作的地方社会','v65_social_mandate_desc':'民心高于64、派系依赖低于61时，地方协助让征税、征募和行政更有效。',
 'v65_civilian_resentment':'白天服从，夜里沉默','v65_civilian_resentment_desc':'民心低于35。村庄不再提供可靠情报，行政与军队的命令也难以得到合作。',
 'v65_weariness':'疲惫的军营','v65_exhaustion':'没有结束日期的战争',
 'v65_rotation':'轮休与补充训练','v65_rotation_desc':'暂时放缓进攻，为部队轮休和基层训练留出空间。',
 'v65_decentralized_command_desc':'中央把地方军政交给自治战区。跨区计划速度下降10%，每日政治点减少0.15；地方部队自行维持治安，援助和重新整合需要另行谈判。',
 'v65_local_command_desc':'本地军政司令部熟悉辖区道路与村庄。防御提高8%，补给消耗降低5%；军区仍须用自己的政治点控制叛乱压力，不能依赖首都自动消灭游击队。',
 'v65_reintegrated_command_desc':'忠诚军区与中央重新签订指挥协定。计划速度提高8%，每日政治点增加0.10；部队和司令随整合保留，中央重新承担地方战争。',
 'v65_jungle_revolution_desc':'红色高棉依托东北丛林建立革命根据地。防御提高15%，补给消耗降低15%；与金边的内战、村庄合作和对外依赖决定这一后方能维持多久。',
 'v65_weariness_desc':'战争疲劳超过54。进攻降低5%，每日政治点减少0.10。轮休、请愿和社会治理路线能够缓解长期消耗；疲劳超过79将进一步恶化。',
 'v65_exhaustion_desc':'战争疲劳超过79。进攻降低12%，稳定度下降6%，每日政治点减少0.20。轮休与兑现地方承诺能缓解疲劳，继续动员则必须承担这些代价。',
 'v65_local_patrol':'命令驻军扩大夜间清剿','v65_local_patrol_desc':'降低3点本地压力，但民心下降4、派系依赖与疲劳上升。军警可以迅速恢复道路控制，也会留下新的怨恨。',
 'v65_village_compact':'与村长重新签订保护协议','v65_village_compact_desc':'降低2点本地压力，民心上升6。需要兑现采购与保护承诺，政治成本较高。',
 'v65_expand_network':'建立新的线人与联络站','v65_expand_network_desc':'剧情情报能力提升一级，最多五级。情报用于核对战报、保护行动与甄别村庄消息。',
 'v65_read_intercepts':'核对截获电报与线人报告','v65_read_intercepts_desc':'消耗一次情报储备，降低2点本地压力，并在90天内保护当地联络。情报行动不使用原版特工槽位。',
 'v65_rest_veterans':'安排老兵轮休与营级整训','v65_rest_veterans_desc':'战争疲劳降低8，战争支持度下降3%，30天内部队侧重恢复而非进攻。',
 'v65_petitions':'听取地方请愿与军属申诉','v65_petitions_desc':'提高5点民心，降低3点派系依赖和1点本地压力。每半年可举行一次。',
 'v65government.3.t':'县城以外的地图又变了颜色','v65government.3.d':'夜间巡逻队送回的报告比白天的行政公报晚了六个小时。地图上的一处联络站已经升起了另一面旗。\n\n“他们不是从北线过来的。”参谋指着粮食征购路线，“人和枪一直在这里。”\n\n这次武装爆发由本军区处置。单靠首都的命令不能让村庄重新提供情报。',
 'v65government.3.a':'本地部队负责恢复道路。',
}
TRACKS={
 'staff':('参谋与命令链',lambda n:f'planning_speed = {n*.04:.2f} political_power_gain = {n*.03:.2f}'),
 'training':('基层训练与轮换骨干',lambda n:f'army_org_factor = {n*.012:.3f} experience_gain_army_unit_factor = {n*.04:.2f}'),
 'signals':('联络、甄别与通信处',lambda n:f'recon_factor = {n*.05:.2f} encryption_factor = {n*.02:.2f}'),
 'logistics':('战区后勤机构',lambda n:f'supply_consumption_factor = {-n*.02:.2f} production_factory_efficiency_gain_factor = {n*.01:.2f}'),
 'contracts':('军需合同与私人网络',lambda n:f'production_factory_efficiency_gain_factor = {n*.025:.3f} stability_factor = {-n*.01:.2f}'),
}
ideas='ideas = { country = {\n';effects=''
for key,(name,mods) in TRACKS.items():
 remove=' '.join(f'v65_{key}_{n}' for n in range(1,6))
 effects+=f'v65_upgrade_{key} = {{ add_to_variable = {{ v65_{key}_level = 1 }} clamp_variable = {{ var = v65_{key}_level min = 0 max = 5 }} remove_ideas = {{ {remove} }}\n'
 for n in range(1,6):
  idea=f'v65_{key}_{n}';ideas+=f'{idea} = {{ picture = generic_army_chief allowed = {{ always = no }} modifier = {{ {mods(n)} }} }}\n'
  effects+=f' if = {{ limit = {{ check_variable = {{ v65_{key}_level = {n} }} }} add_ideas = {idea} }}\n'
  L[idea]=f'{name} · {n}级';L[idea+'_desc']=f'{name}的第{n}级机构。相关国策将机构逐级提升，旧等级会被替换，最高五级。它的长期收益也需要地方社会和持续资源支持。'
 effects+='}\n'
EXTRA={
 'v65_decentralized_command':'political_power_gain = -0.15 planning_speed = -0.10',
 'v65_local_command':'army_defence_factor = 0.08 supply_consumption_factor = -0.05',
 'v65_reintegrated_command':'planning_speed = 0.08 political_power_gain = 0.10',
 'v65_jungle_revolution':'army_defence_factor = 0.15 supply_consumption_factor = -0.15',
 'v65_social_mandate':'stability_factor = 0.08 political_power_gain = 0.15',
 'v65_civilian_resentment':'stability_factor = -0.08 army_org_factor = -0.03',
 'v65_weariness':'army_attack_factor = -0.05 political_power_gain = -0.10',
 'v65_exhaustion':'army_attack_factor = -0.12 stability_factor = -0.06 political_power_gain = -0.20',
 'v65_rotation':'army_attack_factor = -0.04 army_org_factor = 0.03',
}
for key,mods in EXTRA.items():
 ideas+=f'{key} = {{ picture = generic_army_chief allowed = {{ always = no }} modifier = {{ {mods} }} }}\n'
 if key+'_desc' not in L:L[key+'_desc']='这一制度持续影响部队与政治运转。相关决议、民心与战争进程可以改变它的效果。'
for phase in range(1,6):
 for path in ['security','civilian']:
  key=f'v65_policy_{path}_{phase}'
  mods=f'army_defence_factor = {phase*.015:.3f} army_org_factor = {phase*.01:.2f} stability_factor = {-phase*.015:.3f}' if path=='security' else f'stability_factor = {phase*.02:.2f} political_power_gain = {phase*.04:.2f} production_factory_efficiency_gain_factor = {phase*.02:.2f} army_attack_factor = {-phase*.01:.2f}'
  ideas+=f'{key} = {{ picture = generic_political_reform allowed = {{ always = no }} modifier = {{ {mods} }} }}\n'
  L[key]=('战区优先的政治安排' if path=='security' else '行政与社会的长期契约')+f' · 第{phase}阶段'
  L[key+'_desc']='这一阶段的长期政策替换先前阶段的安排。军事动员与地方社会各有收益和代价，不能同时采用两种互斥方案。'
put(Path('common/ideas/v65_long_campaign.txt'),ideas+'} }')
effects+='''v65_refresh_society = {
 clamp_variable = { var = v65_public_trust min = 0 max = 100 }
 clamp_variable = { var = v65_patronage min = 0 max = 100 }
 clamp_variable = { var = v65_war_fatigue min = 0 max = 100 }
 clamp_variable = { var = v65_local_unrest min = 0 max = 10 }
 clamp_variable = { var = v65_intelligence min = 0 max = 5 }
 if = { limit = { check_variable = { v65_public_trust > 64 } check_variable = { v65_patronage < 61 } } add_ideas = v65_social_mandate remove_ideas = v65_civilian_resentment }
 else_if = { limit = { check_variable = { v65_public_trust < 35 } } add_ideas = v65_civilian_resentment remove_ideas = v65_social_mandate }
 else = { remove_ideas = { v65_social_mandate v65_civilian_resentment } }
 if = { limit = { check_variable = { v65_war_fatigue > 79 } } add_ideas = v65_exhaustion remove_ideas = v65_weariness }
 else_if = { limit = { check_variable = { v65_war_fatigue > 54 } } add_ideas = v65_weariness remove_ideas = v65_exhaustion }
 else = { remove_ideas = { v65_exhaustion v65_weariness } }
}
v65_local_security_pulse = {
 if = { limit = { has_war_with = FNL }
  add_to_variable = { v65_local_unrest = 1 }
  if = { limit = { check_variable = { v65_public_trust > 64 } } subtract_from_variable = { v65_local_unrest = 1 } }
  if = { limit = { check_variable = { v65_public_trust < 35 } } add_to_variable = { v65_local_unrest = 1 } }
  if = { limit = { has_country_flag = v65_intel_cover } subtract_from_variable = { v65_local_unrest = 1 } }
  if = { limit = { is_ai = yes has_political_power > 45 check_variable = { v65_local_unrest > 4 } }
   add_political_power = -35 subtract_from_variable = { v65_local_unrest = 2 } add_to_variable = { v65_public_trust = 2 }
  }
  if = { limit = { check_variable = { v65_local_unrest > 7 } } v65_regional_outbreak = yes }
 }
 v65_refresh_society = yes
}
v65_regional_outbreak = {
'''
targets={**{t:next((s for s in reversed(v[3]) if s!=v[2]),v[2]) for t,v in REGIONS.items()},'DNM':12,'PKS':15}
for tag,sid in targets.items():
 if sid == 31:continue  # Island unrest is politics; never teleport an FNL army across the sea.
 pid=next((p for p in provinces(sid) if p!=city(sid)),city(sid))
 effects+=f''' if = {{ limit = {{ tag = {tag} controls_province = {pid} FNL = {{ has_war_with = {tag} }} }}
  FNL = {{ set_province_controller = {pid}
   {sid} = {{ create_unit = {{ division = "name = \\"Local Liberation Detachment\\" division_template = \\"Theater Infantry\\" start_equipment_factor = 0.6 location = {pid}" owner = FNL }} }}
  }} subtract_from_variable = {{ v65_local_unrest = 4 }} country_event = {{ id = v65government.3 days = 1 }}
 }}\n'''
effects+='}\n'
put(Path('common/scripted_effects/v65_society.txt'),effects)
init='\n'.join(f'{tag} = {{ if = {{ limit = {{ exists = yes NOT = {{ has_country_flag = v65_story_initialized }} }} set_country_flag = v65_story_initialized set_variable = {{ v65_public_trust = 50 }} set_variable = {{ v65_patronage = 20 }} set_variable = {{ v65_intelligence = 1 }} set_variable = {{ v65_local_unrest = 2 }} }} }}' for tag in ALL)
monthly='\n'.join(f'{tag} = {{ if = {{ limit = {{ exists = yes }} if = {{ limit = {{ has_war = yes }} add_to_variable = {{ v65_war_fatigue = 0.35 }} }} else = {{ subtract_from_variable = {{ v65_war_fatigue = 0.5 }} }} v65_refresh_society = yes }} }}' for tag in ALL)
monthly+='\n'+'\n'.join(f'{tag} = {{ if = {{ limit = {{ exists = yes }} v65_local_security_pulse = yes }} }}' for tag in targets)
put(Path('common/on_actions/v65_society.txt'),'on_actions = { on_startup = { effect = { '+init+' } } on_monthly = { effect = { '+monthly+' } } }')
cat='OR = { '+' '.join('tag = '+tag for tag in ALL)+' }'
put(Path('common/decisions/categories/v65_governance.txt'),f'v65_story_governance = {{ icon = GFX_decision_generic_military allowed = {{ {cat} }} visible = {{ always = yes }} }}')
put(Path('common/decisions/v65_governance.txt'),'''v65_story_governance = {
 v65_local_patrol = { icon = generic_prepare_civil_war cost = 45 available = { has_war = yes check_variable = { v65_local_unrest > 0 } } days_re_enable = 60 complete_effect = { subtract_from_variable = { v65_local_unrest = 3 } subtract_from_variable = { v65_public_trust = 4 } add_to_variable = { v65_patronage = 2 } add_to_variable = { v65_war_fatigue = 1 } v65_refresh_society = yes } ai_will_do = { factor = 0 } }
 v65_village_compact = { icon = generic_political_discourse cost = 60 available = { check_variable = { v65_local_unrest > 0 } } days_re_enable = 90 complete_effect = { subtract_from_variable = { v65_local_unrest = 2 } add_to_variable = { v65_public_trust = 6 } v65_refresh_society = yes } ai_will_do = { factor = 0.5 } }
 v65_expand_network = { icon = generic_political_discourse cost = 75 available = { check_variable = { v65_intelligence < 5 } } days_re_enable = 120 complete_effect = { add_to_variable = { v65_intelligence = 1 } v65_upgrade_signals = yes v65_refresh_society = yes } ai_will_do = { factor = 0.5 } }
 v65_read_intercepts = { icon = generic_political_discourse cost = 40 available = { check_variable = { v65_intelligence > 0 } NOT = { has_country_flag = v65_intel_cover } } days_re_enable = 90 complete_effect = { subtract_from_variable = { v65_intelligence = 1 } subtract_from_variable = { v65_local_unrest = 2 } set_country_flag = v65_intel_cover country_event = { id = v65government.9 days = 90 } v65_refresh_society = yes } ai_will_do = { factor = 0.5 } }
 v65_rest_veterans = { icon = generic_prepare_civil_war cost = 65 available = { check_variable = { v65_war_fatigue > 7 } } days_re_enable = 120 complete_effect = { subtract_from_variable = { v65_war_fatigue = 8 } add_war_support = -0.03 add_timed_idea = { idea = v65_rotation days = 30 } v65_refresh_society = yes } ai_will_do = { factor = 1 } }
 v65_petitions = { icon = generic_political_discourse cost = 45 available = { check_variable = { v65_public_trust < 95 } } days_re_enable = 180 complete_effect = { add_to_variable = { v65_public_trust = 5 } subtract_from_variable = { v65_patronage = 3 } subtract_from_variable = { v65_local_unrest = 1 } v65_refresh_society = yes } ai_will_do = { factor = 0.5 } }
}''')
put(Path('events/v65_governance.txt'),'''add_namespace = v65government
country_event = { id = v65government.3 title = v65government.3.t desc = v65government.3.d picture = GFX_report_event_generic_read_write is_triggered_only = yes option = { name = v65government.3.a add_war_support = -0.02 } }
country_event = { id = v65government.9 hidden = yes is_triggered_only = yes immediate = { clr_country_flag = v65_intel_cover } }
''')
# References to a rear province must follow its regional controller after devolution.
effects_path=M/'common/scripted_effects/v65_politics.txt';text=effects_path.read_text(encoding='utf-8')
for pid in [244,269,288,300,324]:
 old=f'SVN = {{ controls_province = {pid} }}'
 new='OR = { '+' '.join(f'{t} = {{ controls_province = {pid} }}' for t in ['SVN',*REGIONS])+' }'
 text=text.replace(old,new)
import pdx
war='OR = { '+' '.join('has_war_with = '+tag for tag in ['SVN','PKS','DNM',*REGIONS])+' }'
blocks=pdx.parse(text)
blocks=[(k,op,pdx.parse(pdx.dump(v).replace('has_war_with = SVN',war))) if k=='v65_launch_infiltration' or k.startswith('v65_raid_') else (k,op,v) for k,op,v in blocks]
effects_path.write_text(pdx.dump(blocks),encoding='utf-8')
p=M/'common/on_actions/v65_politics.txt';text=p.read_text(encoding='utf-8').replace('has_war_with = SVN',war);p.write_text(text,encoding='utf-8')
p=M/'common/decisions/v65_trail.txt';text=p.read_text(encoding='utf-8')
for pid in [244,269,288,300,324]:
 text=text.replace(f'SVN = {{ controls_province = {pid} }}','OR = { '+' '.join(f'{t} = {{ controls_province = {pid} }}' for t in ['SVN',*REGIONS])+' }')
text=text.replace('tag = SVN tag = PKS tag = DNM','tag = SVN tag = PKS tag = DNM '+' '.join('tag = '+t for t in REGIONS))
text=text.replace('has_war_with = SVN',war)
p.write_text(text,encoding='utf-8')
for lang in ['simp_chinese','english']:
 put(Path(f'localisation/{lang}/zzzzzz_v65_society_l_{lang}.yml'),loc_text(L,lang))
print('Five-tier institutions, persistent society, local security and narrative intelligence authored')
