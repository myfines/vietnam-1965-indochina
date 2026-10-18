"""Geographic defeat stages inspired by the novel, triggered by real control."""
from build_campaign import put
from pathlib import Path
put(Path('common/scripted_triggers/v65_war_stages.txt'),'''v65_highland_has_fallen = { OR = { 18 = { is_controlled_by = NVN } 18 = { is_controlled_by = FNL } 16 = { is_controlled_by = NVN } 16 = { is_controlled_by = FNL } } }
v65_saigon_has_fallen = { NOT = { controls_province = 305 } OR = { controls_state = 28 controls_state = 31 } }
''')
put(Path('common/ideas/v65_war_stages.txt'),'''ideas = { country = {
 v65_highland_disruption = { picture = generic_army_chief allowed = { always = no } modifier = { army_org_factor = -0.05 supply_consumption_factor = 0.05 } }
 v65_southern_holdouts = { picture = generic_army_chief allowed = { always = no } modifier = { surrender_limit = 0.15 army_defence_factor = 0.05 } }
} }''')
put(Path('common/scripted_effects/v65_war_stages.txt'),'''v65_check_war_stages = {
 if = { limit = { tag = SVN exists = yes has_war_with = NVN }
  if = { limit = { NOT = { has_country_flag = v65_highlands_lost } v65_highland_has_fallen = yes }
   set_country_flag = v65_highlands_lost set_country_flag = v65_front_defeat set_country_flag = v65_crisis_active
   add_timed_idea = { idea = v65_highland_disruption days = 90 }
   country_event = { id = v65stages.1 days = 1 }
   PKS = { if = { limit = { exists = yes } country_event = { id = v65stages.2 days = 1 } } }
  }
  if = { limit = { NOT = { has_country_flag = v65_saigon_lost } v65_saigon_has_fallen = yes }
   set_country_flag = v65_saigon_lost add_ideas = v65_southern_holdouts
   if = { limit = { controls_state = 28 } set_capital = { state = 28 } }
   else = { set_capital = { state = 31 } }
   country_event = { id = v65stages.3 days = 1 }
  }
 }
}''')
put(Path('common/on_actions/v65_war_stages.txt'),'''on_actions = { on_daily = { effect = { SVN = { v65_check_war_stages = yes } } } }''')
put(Path('events/v65_war_stages.txt'),'''add_namespace = v65stages
country_event = { id = v65stages.1 title = v65stages.1.t desc = v65stages.1.d picture = GFX_report_event_generic_read_write is_triggered_only = yes
 option = { name = v65stages.1.a add_political_power = -50 add_war_support = 0.05 army_experience = 15 }
 option = { name = v65stages.1.b add_stability = -0.05 add_ideas = v65_prepared_defence }
}
country_event = { id = v65stages.2 title = v65stages.2.t desc = v65stages.2.d picture = GFX_report_event_generic_read_write is_triggered_only = yes
 option = { name = v65stages.2.a add_to_variable = { v65_park_influence = 1 } add_political_power = -35 SVN = { add_equipment_to_stockpile = { type = infantry_equipment_2 amount = 600 producer = PKS } } }
 option = { name = v65stages.2.b add_political_power = 35 add_stability = -0.03 }
}
country_event = { id = v65stages.3 title = v65stages.3.t desc = v65stages.3.d picture = GFX_report_event_generic_read_write is_triggered_only = yes
 option = { name = v65stages.3.a add_war_support = 0.05 }
 option = { name = v65stages.3.b trigger = { 31 = { is_owned_by = ROOT is_controlled_by = ROOT } } add_political_power = -50 31 = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } } }
}''')
L={
 'v65_highland_disruption':'西原交通线断裂','v65_highland_disruption_desc':'西原重镇失守后的90天内，撤退与补给中断降低部队组织度，并增加补给消耗。',
 'v65_southern_holdouts':'三角洲与离岛的继续抵抗','v65_southern_holdouts_desc':'首都失守不等于所有地方部队都已放下武器。三角洲或富国岛仍可维持政府机构，提供额外投降抵抗与防御。',
 'v65stages.1.t':'西原的道路正在断裂','v65stages.1.d':'波来古或邦美蜀失守，内陆道路上的撤退队伍挤成长龙。北部战术区、沿海军区和西贡接到的命令互相矛盾。总统府必须决定，是付出政治代价重组指挥，还是接受收缩防区的现实。西原的败局也已经打开首都的政治危机。',
 'v65stages.1.a':'重组指挥，准备继续作战。','v65stages.1.b':'收缩防区，保存主力。',
 'v65stages.2.t':'来自西原的求援电话','v65stages.2.d':'西原军官请求归仁提供武器和协调指挥。他们愿意接受顾问，却不愿交出自己的部队。援助能够扩大朴世诚的影响，也会使他背上下一场败仗的责任。',
 'v65stages.2.a':'提供六百支步枪，派联络官。','v65stages.2.b':'保住归仁，不接手别人的败局。',
 'v65stages.3.t':'西贡失守，战争尚未结束','v65stages.3.d':'总统府的通信已经中断，幸存机关正向仍在控制中的三角洲或富国岛转移。大陆军区与离岛驻军有着不同的打算；只要后方还有土地和部队，政府便继续抵抗。控制首都的人尚未控制整个南方。',
 'v65stages.3.a':'以现存军区继续抵抗。','v65stages.3.b':'拨款建设富国岛后方。',
}
for lang in ['simp_chinese','english']:
 put(Path(f'localisation/{lang}/zzzzzz_v65_stages_l_{lang}.yml'),'l_'+lang+':\n'+'\n'.join(f' {k}:0 "{v}"' for k,v in L.items()))
print('Highland breakthrough and southern holdout events authored')
