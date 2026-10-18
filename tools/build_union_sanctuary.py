"""Negotiated shadow regency and Cambodia's neutral logistics rear."""
from build_campaign import put,M
from pathlib import Path

put(Path('common/scripted_triggers/v65_union_sanctuary.txt'),'''v65_can_offer_union = {
 tag = PKS exists = yes controls_state = 15
 check_variable = { v65_park_influence > 4 }
 NOT = { has_country_flag = v65_union_pending }
 NOT = { has_country_flag = v65_union_refused }
 NOT = { has_war_with = SVN }
 is_in_faction_with = SVN
 SVN = { exists = yes controls_state = 25 }
 NOT = { AND = { is_ai = no SVN = { is_ai = no } } }
}
v65_sanctuary_operational = {
 tag = KHM exists = yes NOT = { has_war_with = SVN } NOT = { has_war_with = NVN } NOT = { has_war_with = FNL }
 has_country_flag = v65_sanctuary_open
 controls_state = 35 controls_state = 42
 NVN = { exists = yes has_war_with = SVN }
 FNL = { exists = yes has_war_with = SVN }
}''')
put(Path('interface/v65_spirits.gfx'),'spriteTypes = { spriteType = { name = "GFX_idea_v65_park_shadow_ruler" texturefile = "gfx/leaders/v65/park_seicheng.dds" } }')
put(Path('common/ideas/v65_union_sanctuary.txt'),'''ideas = { country = {
 v65_park_shadow_ruler = { picture = v65_park_shadow_ruler allowed = { always = no }
  modifier = { political_power_gain = 0.20 army_org_factor = 0.05 production_factory_efficiency_gain_factor = 0.08 stability_factor = -0.05 }
 }
 v65_neutral_sanctuary = { picture = generic_army_chief allowed = { always = no }
  modifier = { political_power_gain = -0.10 production_speed_infrastructure_factor = 0.10 }
 }
 v65_faction_compromise = { picture = generic_political_reform allowed = { always = no }
  modifier = { political_power_gain = -0.15 stability_factor = 0.05 }
 }
} }''')
put(Path('common/scripted_effects/v65_union_sanctuary.txt'),'''v65_offer_union = {
 if = { limit = { v65_can_offer_union = yes }
  set_country_flag = v65_union_pending
  SVN = { country_event = { id = v65routes.1 days = 1 } }
 }
}
v65_finalize_union = {
 if = { limit = { PKS = { v65_can_offer_union = yes } SVN = { exists = yes controls_state = 25 } }
  # Transfer the human before annexation. All other southern systems keep SVN.
  SVN = { if = { limit = { PKS = { is_ai = no } } change_tag_from = PKS } }
  PKS = {
   if = { limit = { has_character = v65_park_seicheng } v65_park_seicheng = { set_nationality = SVN } }
   if = { limit = { has_character = v65_kim_jong_pil } v65_kim_jong_pil = { set_nationality = SVN } }
   if = { limit = { has_character = v65_kim_jae_gyu } v65_kim_jae_gyu = { set_nationality = SVN } }
   if = { limit = { has_character = v65_park_chung_hee } v65_park_chung_hee = { set_nationality = SVN } }
  }
  SVN = {
   annex_country = { target = PKS transfer_troops = yes }
   15 = { add_core_of = SVN }
   add_ideas = v65_park_shadow_ruler set_country_flag = v65_union_complete
   add_stability = 0.05
   if = { limit = { has_character = v65_nguyen_van_thieu }
    promote_character = { character = v65_nguyen_van_thieu ideology = despotism }
   }
   country_event = { id = v65routes.2 days = 1 }
   country_event = { id = v65routes.4 days = 45 }
  }
 }
}
v65_open_sanctuary = {
 if = { limit = { tag = KHM NOT = { has_war_with = SVN } NOT = { has_war_with = NVN } NOT = { has_war_with = FNL } controls_state = 35 controls_state = 42 }
  set_country_flag = v65_sanctuary_open add_ideas = v65_neutral_sanctuary
 }
}
v65_close_sanctuary = {
 clr_country_flag = v65_sanctuary_open remove_ideas = v65_neutral_sanctuary
}
v65_sanctuary_pulse = {
 if = { limit = { v65_sanctuary_operational = yes }
  NVN = { add_to_variable = { v65_trail_level = 1 } clamp_variable = { var = v65_trail_level min = 0 max = 5 } }
  FNL = { add_to_variable = { v65_infiltration = 1 } clamp_variable = { var = v65_infiltration min = 0 max = 3 }
   add_equipment_to_stockpile = { type = infantry_equipment_2 amount = 300 producer = NVN }
  }
  add_to_variable = { v65_border_tension = 1 } clamp_variable = { var = v65_border_tension min = 0 max = 3 }
  if = { limit = { NOT = { has_country_flag = v65_sanctuary_discovered } }
   set_country_flag = v65_sanctuary_discovered SVN = { country_event = { id = v65routes.5 days = 1 } }
  }
 }
}
v65_apply_border_pressure = {
 KHM = { if = { limit = { v65_sanctuary_operational = yes }
  add_to_variable = { v65_border_tension = 1 } clamp_variable = { var = v65_border_tension min = 0 max = 3 }
  country_event = { id = v65routes.6 days = 1 }
 } }
}''')
put(Path('common/on_actions/v65_routes.txt'),'''on_actions = {
 on_monthly = { effect = { KHM = { v65_sanctuary_pulse = yes } } }
 on_daily = { effect = { KHM = {
  if = { limit = { has_country_flag = v65_sanctuary_open OR = { has_war_with = SVN has_war_with = NVN has_war_with = FNL NOT = { controls_state = 35 } NOT = { controls_state = 42 } } } v65_close_sanctuary = yes }
 } } }
}''')
put(Path('common/decisions/categories/v65_routes.txt'),'''v65_union = { icon = GFX_decision_generic_military allowed = { OR = { tag = PKS tag = SVN } } visible = { always = yes } }
v65_cambodian_rear = { icon = GFX_decision_generic_military allowed = { OR = { tag = KHM tag = SVN tag = PKS tag = DNM } } visible = { always = yes } }''')
put(Path('common/decisions/v65_union_sanctuary.txt'),'''v65_union = {
 v65_request_union = { icon = generic_political_discourse cost = 100 visible = { tag = PKS } available = { v65_can_offer_union = yes } days_re_enable = 90 complete_effect = { v65_offer_union = yes } ai_will_do = { factor = 0.3 } }
}
v65_cambodian_rear = {
 v65_open_border_bases = { icon = generic_prepare_civil_war cost = 50 visible = { tag = KHM NOT = { has_country_flag = v65_sanctuary_open } } available = { NOT = { has_war_with = SVN } NOT = { has_war_with = NVN } NOT = { has_war_with = FNL } controls_state = 35 controls_state = 42 } complete_effect = { v65_open_sanctuary = yes } ai_will_do = { factor = 1 } }
 v65_seal_border_bases = { icon = generic_prepare_civil_war cost = 50 visible = { tag = KHM has_country_flag = v65_sanctuary_open } complete_effect = { v65_close_sanctuary = yes } ai_will_do = { factor = 0 } }
 v65_border_dossier = { icon = generic_political_discourse cost = 60 visible = { OR = { tag = SVN tag = PKS tag = DNM } KHM = { has_country_flag = v65_sanctuary_discovered } } available = { KHM = { v65_sanctuary_operational = yes } } days_re_enable = 60 complete_effect = { v65_apply_border_pressure = yes } ai_will_do = { factor = 0.5 } }
}''')
put(Path('events/v65_routes.txt'),'''add_namespace = v65routes
country_event = { id = v65routes.1 title = v65routes.1.t desc = v65routes.1.d picture = GFX_report_event_generic_sign_treaty is_triggered_only = yes
 immediate = { PKS = { clr_country_flag = v65_union_pending } }
 option = { name = v65routes.1.a ai_chance = { factor = 70 modifier = { factor = 2 check_variable = { v65_park_trust > 64 } } modifier = { factor = 0.5 check_variable = { v65_park_trust < 35 } } }
  trigger = { PKS = { exists = yes NOT = { has_war_with = SVN } } controls_state = 25 }
  v65_finalize_union = yes
 }
 option = { name = v65routes.1.b ai_chance = { factor = 30 }
  PKS = { set_country_flag = v65_union_refused country_event = { id = v65routes.3 days = 90 } }
  add_political_power = 35
 }
}
country_event = { id = v65routes.2 title = v65routes.2.t desc = v65routes.2.d picture = GFX_report_event_generic_read_write is_triggered_only = yes
 option = { name = v65routes.2.a add_political_power = 50 }
}
country_event = { id = v65routes.3 hidden = yes is_triggered_only = yes immediate = { clr_country_flag = v65_union_refused } }
country_event = { id = v65routes.4 title = v65routes.4.t desc = v65routes.4.d picture = GFX_report_event_generic_read_write is_triggered_only = yes
 trigger = { has_idea = v65_park_shadow_ruler }
 option = { name = v65routes.4.a add_political_power = -75 add_stability = 0.03 }
 option = { name = v65routes.4.b add_timed_idea = { idea = v65_faction_compromise days = 180 } }
}
country_event = { id = v65routes.5 title = v65routes.5.t desc = v65routes.5.d picture = GFX_report_event_generic_read_write is_triggered_only = yes
 option = { name = v65routes.5.a add_political_power = 30 }
}
country_event = { id = v65routes.6 title = v65routes.6.t desc = v65routes.6.d picture = GFX_report_event_generic_sign_treaty is_triggered_only = yes
 trigger = { v65_sanctuary_operational = yes }
 option = { name = v65routes.6.a ai_chance = { factor = 65 } add_stability = -0.03 add_political_power = -25 }
 option = { name = v65routes.6.b ai_chance = { factor = 35 modifier = { factor = 3 check_variable = { v65_border_tension > 2 } } }
  v65_close_sanctuary = yes add_political_power = 25
 }
}''')
L={
 'v65_union':'归仁与西贡：联合政府谈判','v65_cambodian_rear':'柬埔寨：中立幕布后的战争',
 'v65_park_shadow_ruler':'朴世诚：幕后太上皇','v65_park_shadow_ruler_desc':'总统与内阁仍在台前，朴世诚的军官任命、军需合同与顾问网络则控制着关键决定。统一指挥与采购提高组织度、生产效率和政治点收益；派系对幕后权力的不满降低稳定度。此联合政府结局为模组架空路线。',
 'v65_neutral_sanctuary':'中立旗帜下的秘密后方','v65_neutral_sanctuary_desc':'只要柬埔寨没有对越南各方参战且控制桔井与西哈努克港，每月为北方通道与南方动员各补充一级，并提供300支步枪。对越南参战或据点失守立即关闭基地；外交压力可能迫使金边封锁通道。',
 'v65_faction_compromise':'军头的保留条款','v65_faction_compromise_desc':'军区保留了部分任命权，换取对联合政府的支持。未来180天内政治整合放缓。',
 'v65_request_union':'提出联合政府议定书','v65_request_union_desc':'影响力至少5点，归仁与西贡首都均未失守，双方仍属同一联盟且没有交战，才可以谈判。西贡可拒绝并冻结谈判90天。接受后部队、领土和人物归入南越；朴世诚玩家自动接手南越，继续战争。两方均由玩家控制时不开放谈判。',
 'v65_open_border_bases':'默许北方边境基地','v65_seal_border_bases':'关闭秘密转运基地','v65_border_dossier':'向金边提交越境补给证据',
 'v65_border_dossier_desc':'向金边施压，使其在保留基地、承受政治损失与关闭通道之间选择。不会自动向柬埔寨宣战。',
 'v65_cambodian_rear_desc':'金边与红色高棉进行内战，同时对越南维持独立外交。秘密后方运转时，每月增加北方通道、南方组织能力及步枪储备；解放阵线再通过胡志明小道决议在南方腹地建立武装。边境紧张度：[KHM.v65_border_tension|0]/3。',
 'v65routes.1.t':'总统府收到联合政府议定书','v65routes.1.d':'归仁代表提出合并军饷、指挥和行政体系。总统保留职位，朴世诚则掌握军官任命、军需采购与顾问联络。接受可以结束联盟内部的重复机构，也意味着总统府必须容忍一个不在内阁名单上的权力中心。',
 'v65routes.1.a':'签署议定书，统一南方指挥。','v65routes.1.b':'总统府不接受这种监护。',
 'v65routes.2.t':'总统留在台前','v65routes.2.d':'归仁部队与军需机关已归入南越编制，阮文绍继续主持总统府。朴世诚没有接任国家元首，却在新的军政协调会中握有任命与合同的决定权。各军区暂时签字，没人保证他们会永远服从。',
 'v65routes.2.a':'真正的权力不必写在名片上。',
 'v65routes.4.t':'军区拒绝新的任命名单','v65routes.4.d':'联合政府成立后，第一批军官调任触动了地方派系。军区要求保留自己的晋升渠道。协调会必须拿出补偿，或允许一段时期的人事妥协，否则每一道命令都会变成新的交易。',
 'v65routes.4.a':'支付整编经费，维持统一任命。','v65routes.4.b':'用半年的保留条款换取合作。',
 'v65routes.5.t':'货单背后的丛林基地','v65routes.5.d':'被截获的运输单据指向桔井与腊塔纳基里。金边没有正式参战，但粮食、武器与人员正从它的边境抵达南方地下组织。我们可以继续截断运输，也可以提交证据，迫使金边回应。',
 'v65routes.5.a':'整理证据，准备外交交涉。',
 'v65routes.6.t':'中立声明遭到质疑','v65routes.6.d':'南方代表提交了一份边境基地清单，要求金边关闭秘密通道。维持默契会消耗政府威信；封锁基地则将失去北方的信任与筹码。边境紧张度越高，继续掩护的代价就越难承担。',
 'v65routes.6.a':'否认指控，默许基地继续运作。','v65routes.6.b':'暂时封锁转运通道。',
}
for lang in ['simp_chinese','english']:
 put(Path(f'localisation/{lang}/zzzzzz_v65_routes_l_{lang}.yml'),'l_'+lang+':\n'+'\n'.join(f' {k}:0 "{v}"' for k,v in L.items()))
print('Negotiated union, player transfer and neutral Cambodian sanctuary authored')
