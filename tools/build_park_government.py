"""A separate governing phase, with a persistent contractor/army resource loop."""
from pathlib import Path
import sys
from build_campaign import M,R,put
from long_foundation import REGIONS,loc_text
sys.path.insert(0,str(R/'vendor'));import pdx

L={
 'v65_park_government':'朴系主持的南越中央',
 'v65_park_government_desc':'总统府保留名义，军饷、任命和跨区调度由朴系协调。',
 'v65_pgov_root':'接过西贡的电话',
 'v65_pgov_root_desc':'接管已经完成。先确认谁负责拨款，谁有权调兵。',
 'v65_contract_operations':'驻越合同与军需渠道',
 'v65_contract_operations_desc':'军需信用：[?v65_contract_credit|0]/10　核查次数：[?v65_ledger_claims|0]\n军需信用用于韩军增援与代理部队。战报核查失败会冻结申报90天。',
 'v65_claim_supplies':'用战果申请追加军需',
 'v65_claim_supplies_desc':'35政治点，每60天一次。申报少于3次时70%通过，获得600步枪及2点军需信用；之后通过率降为45%。核查失败损失40政治点并冻结申报90天。',
 'v65_call_koreans':'申请韩军增援分遣队',
 'v65_call_koreans_desc':'消耗100政治点和2点军需信用，在完整控制的当前首都部署一个韩军步兵团。每180天一次，最多三次。',
 'v65_raise_proxy':'征募越南代理部队',
 'v65_raise_proxy_desc':'消耗60政治点和1点军需信用，在当前首都部署一个缺乏训练和装备的代理团。每90天一次。',
 'v65_open_credit':'向军需联系人购买信用',
 'v65_open_credit_desc':'消耗60政治点换取2点军需信用，每90天一次。',
 'v65_audit_pass':'追加军需获批','v65_audit_pass_desc':'申报通过，下一批运输增加武器与军需额度。',
 'v65_audit_hold':'军需申报被冻结','v65_audit_hold_desc':'账目需要复核，90天内不能继续申请追加军需。',
 'v65gov.1.t':'中央换了一套班子',
 'v65gov.1.d':'总统仍在，军需和跨区调令改由朴系经手。各军区等着看新的任命与拨款。',
 'v65gov.1.a':'先处理军饷和指挥权。',
}
# Each lane offers a real institutional fork, then rejoins. No dated filler nodes.
BRANCHES=[
 ('command',0,'军区任命',[
  ('roster','核对司令与实际驻军','把军区名册、驻地和领饷数对上。','v65_upgrade_staff = yes add_political_power = 25','staff'),
  ('personal','由朴系参谋接管调令','跨区调动交给直属参谋。地方司令保留自己的部队。','add_ideas = v65_personal_staff add_to_variable = { v65_central_prestige = 8 }','command'),
  ('council','召开军区协调会','让各区签下调兵和拨款的份额。','add_ideas = v65_command_council v65_loyalty_grant = yes','treaty'),
  ('inspect','派出直属督察组','驻军报告直接送往协调处。','v65_upgrade_signals = yes add_to_variable = { v65_central_prestige = 6 }','inspect'),
  ('compact','承认军区内部任命','中央只保留跨区调度权，换取司令配合。','v65_loyalty_grant = yes add_to_variable = { v65_public_trust = 4 }','autonomy'),
  ('reserve','确定中央预备队','固定预备队的军饷与调动手续。','v65_upgrade_training = yes add_manpower = 4000','reserve'),
  ('orders','恢复跨区作战命令','有了名单、经费和联络，命令才能执行。','v65_upgrade_staff = yes add_to_variable = { v65_central_prestige = 10 }','orders'),
 ]),
 ('finance',10,'军饷与日海',[
  ('accounts','接收旧政府的军需账','库存和欠账都要继续处理。','add_to_variable = { v65_contract_credit = 2 } v65_upgrade_logistics = yes','ledger'),
  ('budget','固定各区军饷份额','中央承担定期拨款，限制临时截留。','add_ideas = v65_regular_payroll v65_loyalty_grant = yes','payroll'),
  ('contracts','让日海承包运输','通过私人合同维持运输和采购。','add_ideas = v65_daihai_contracts add_to_variable = { v65_contract_credit = 3 }','contracts'),
  ('reconcile','以实编人数发饷','拨款与在册部队核对，保留可查的记录。','add_to_variable = { v65_public_trust = 6 } add_to_variable = { v65_central_prestige = 6 }','recruit'),
  ('report','扩大特需申报渠道','让军需联系人承接更多采购。','v65_upgrade_contracts = yes add_to_variable = { v65_contract_credit = 3 }','supply'),
  ('repair','设立维修与零件库','把现有装备留在部队手里继续使用。','v65_upgrade_logistics = yes add_equipment_to_stockpile = { type = motorized_equipment_1 amount = 120 producer = ROOT }','repair'),
  ('settle','结清一次跨区欠饷','先把最影响调兵的欠账补齐。','v65_loyalty_grant = yes add_to_variable = { v65_central_prestige = 8 }','funds'),
 ]),
 ('korea',20,'韩军与海外渠道',[
  ('liaison','保留驻越联络组','将韩国本土、驻越部队与协调处的联络固定下来。','add_to_variable = { v65_contract_credit = 2 } add_to_variable = { v65_personal_network = 1 }','radio'),
  ('cadre','申请韩军骨干留驻','争取一支有实战经验的分遣队。','v65_free_korean_detachment = yes','korea'),
  ('training','扩大越南军官培训','用教官换取本地部队的长期依附。','v65_upgrade_training = yes add_to_variable = { v65_personal_network = 2 }','academy'),
  ('airlift','为分遣队保留空运额度','补给和轮换优先保障骨干部队。','v65_upgrade_logistics = yes add_to_variable = { v65_contract_credit = 2 }','airlift'),
  ('advisers','派顾问进入军区司令部','把培训关系延伸到实际调度。','v65_upgrade_staff = yes v65_loyalty_grant = yes','adviser'),
  ('rotation','安排驻军轮换','用轮换名额维持海外部队的留驻意愿。','subtract_from_variable = { v65_war_fatigue = 8 } v65_upgrade_training = yes','rotation'),
  ('channel','建立固定增援渠道','把临时关系变成持续的补充来源。','add_ideas = v65_overseas_channel add_to_variable = { v65_contract_credit = 3 }','reinforce'),
 ]),
 ('rear',30,'地方部队与后方',[
  ('map','重新登记后方联络线','把县城、公路与游击网络分别标出来。','add_to_variable = { v65_intelligence = 1 } v65_upgrade_signals = yes','map'),
  ('proxy','征发地方代理部队','扩大地方武装，先把人数补出来。','v65_free_proxy = yes add_to_variable = { v65_patronage = 3 }','proxy'),
  ('village','与地方头面人物签约','把向导、运输和村庄联络列进协议。','add_to_variable = { v65_public_trust = 7 } v65_rear_relief = yes','village'),
  ('garrison','把代理团纳入驻军表','指定驻地与军饷渠道，减少临时借兵。','v65_upgrade_training = yes add_manpower = 5000','garrison'),
  ('routes','优先打通运输道路','控制道路周边的联络站。','v65_rear_relief = yes v65_upgrade_logistics = yes','roads'),
  ('intel','让军区自行核对情报','当地报告与中央截获记录交叉核实。','add_to_variable = { v65_intelligence = 2 } v65_upgrade_signals = yes','intelligence'),
  ('rear_order','恢复后方驻军协定','中央提供支援，军区承担具体治安。','v65_loyalty_grant = yes v65_rear_relief = yes','security'),
 ]),
 ('settlement',40,'撤军后的安排',[
  ('warehouses','清点移交仓库','把接收装备登记进库存。','add_equipment_to_stockpile = { type = infantry_equipment_2 amount = 1000 producer = ROOT }','warehouse'),
  ('island','保留离岛后勤','把岛上基地作为维修和训练后方。','add_ideas = v65_island_logistics v65_upgrade_logistics = yes','port'),
  ('mainland','优先维持大陆战区','把可用物资分给仍在作战的军区。','v65_loyalty_grant = yes add_to_variable = { v65_central_prestige = 8 }','mainland'),
  ('evacuation','拟定基地与人员转运表','明确撤离顺序和可带走的物资。','subtract_from_variable = { v65_war_fatigue = 6 } add_to_variable = { v65_contract_credit = 2 }','evacuation'),
  ('districts','重签各区补给份额','中央和军区按实际驻军重分库存。','v65_loyalty_grant = yes v65_upgrade_contracts = yes','allocation'),
  ('mandate','确认中央最后保留的权限','明确任命、调兵与对外援助的签字人。','add_to_variable = { v65_central_prestige = 10 } v65_upgrade_staff = yes','mandate'),
  ('regency','让所有人继续拿得到军饷','名义政府和实际指挥体系维持合作。','add_ideas = v65_settled_regency v65_loyalty_grant = yes','regency'),
 ]),
]
tree='focus_tree = { id = v65_park_government default = no reset_on_civilwar = no country = { factor = 0 } continuous_focus_position = { x = 20 y = 1800 }\n'
tree+='focus = { id = v65_pgov_root icon = GFX_v65_detail_command x = 20 y = 0 cost = 3 completion_reward = { add_political_power = 50 } }\n'
art_assignments={'v65_pgov_root':'command'}
for lane,x,title,items in BRANCHES:
 ids=['v65_pgov_'+lane+'_'+item[0] for item in items]
 for i,(slug,name,desc,reward,icon) in enumerate(items):
  ident=ids[i];L[ident]=name;L[ident+'_desc']=desc
  xp=x+([-2,2,-2,2][i-1] if i in [1,2,3,4] else 0)
  yp=[3,6,6,9,9,12,15][i]
  before='v65_pgov_root' if i==0 else ids[0] if i in [1,2] else ids[i-2] if i in [3,4] else ' '.join(ids[3:5]) if i==5 else ids[5]
  prerequisites='prerequisite = { '+' '.join('focus = '+v for v in before.split())+' }'
  exclusion=f'mutually_exclusive = {{ focus = {ids[3-i]} }}' if i in [1,2] else ''
  tree+=f'focus = {{ id = {ident} icon = GFX_v65_detail_{icon} x = {xp} y = {yp} cost = 5 {prerequisites} {exclusion} search_filters = {{ FOCUS_FILTER_POLITICAL FOCUS_FILTER_ARMY }} completion_reward = {{ {reward} clamp_variable = {{ var = v65_contract_credit min = 0 max = 10 }} v65_refresh_command = yes v65_refresh_society = yes }} ai_will_do = {{ factor = 1 }} }}\n'
  art_assignments[ident]=icon
put(Path('common/national_focus/v65_PARK_GOVERNMENT.txt'),tree+'}')
loyalty=' '.join(f'if = {{ limit = {{ {t} = {{ exists = yes v65_under_central_command = yes }} }} {t} = {{ add_to_variable = {{ v65_regional_loyalty = 5 }} clamp_variable = {{ var = v65_regional_loyalty min = 0 max = 100 }} }} }}' for t in REGIONS)
effects='''v65_begin_park_government = {
 if = { limit = { tag = SVN has_country_flag = v65_union_complete NOT = { has_country_flag = v65_park_government_started } }
  set_country_flag = v65_park_government_started v65_record_government_history = yes load_focus_tree = { tree = v65_park_government keep_completed = yes }
  country_event = { id = v65gov.1 days = 2 }
 }
}
v65_loyalty_grant = { LOYALTY }
v65_free_korean_detachment = {
 if = { limit = { capital_scope = { is_fully_controlled_by = PREV } }
  capital_scope = { create_unit = { division = "name = \\"ROK Liaison Regiment\\" division_template = \\"Theater Infantry\\" start_equipment_factor = 1 start_experience_factor = 0.6" owner = PREV } }
 }
}
v65_free_proxy = {
 if = { limit = { capital_scope = { is_fully_controlled_by = PREV } }
  capital_scope = { create_unit = { division = "name = \\"Local Auxiliary Regiment\\" division_template = \\"Theater Infantry\\" start_equipment_factor = 0.3 start_experience_factor = 0" owner = PREV } }
 }
}
v65_credit = { clamp_variable = { var = v65_contract_credit min = 0 max = 10 } }
v65_report_success = { add_equipment_to_stockpile = { type = infantry_equipment_2 amount = 600 producer = ROOT } add_to_variable = { v65_contract_credit = 2 } v65_credit = yes set_country_flag = v65_last_claim_passed }
v65_report_audit = { add_political_power = -40 set_country_flag = v65_audit_frozen country_event = { id = v65gov.9 days = 90 } clr_country_flag = v65_last_claim_passed }
v65_claim_supplies = {
 if = { limit = { NOT = { has_country_flag = v65_audit_frozen } }
  if = { limit = { check_variable = { v65_ledger_claims < 3 } } random_list = { 70 = { v65_report_success = yes } 30 = { v65_report_audit = yes } } }
  else = { random_list = { 45 = { v65_report_success = yes } 55 = { v65_report_audit = yes } } }
  add_to_variable = { v65_ledger_claims = 1 }
 }
}
'''.replace('LOYALTY',loyalty)
history_ids=[v for k,op,tree in pdx.read(M/'common/national_focus/v65_SVN.txt') for kind,oper,body in tree if kind=='focus' for key,_,v in body if key=='id']
effects+='v65_record_government_history = { '+' '.join(f'if = {{ limit = {{ has_completed_focus = {ident} }} set_country_flag = v65_history_{ident} }}' for ident in history_ids)+' }\n'
put(Path('common/scripted_effects/v65_park_government.txt'),effects)
ideas={
 'v65_personal_staff':('直属参谋掌握调令','planning_speed = 0.10 political_power_gain = 0.05','跨区命令由朴系参谋办理，中央威望与地方忠诚仍分别计算。'),
 'v65_command_council':('军区联席会议','planning_speed = 0.03 stability_factor = 0.04','各区按协定调兵和分担预算，司令保留内部任命权。'),
 'v65_regular_payroll':('固定军饷拨款','army_org_factor = 0.04 political_power_gain = -0.10','中央承担持续军费，部队组织度提高4%，每日政治点减少0.10。'),
 'v65_daihai_contracts':('日海军需承包','production_factory_efficiency_gain_factor = 0.08 stability_factor = -0.03','私人运输与采购提高生产效率增长，地方分账仍会产生摩擦。'),
 'v65_overseas_channel':('驻越增援渠道','army_org_factor = 0.03 supply_consumption_factor = -0.05','海外骨干与轮换渠道维持作战组织和补给效率。'),
 'v65_island_logistics':('离岛维修与训练后方','supply_consumption_factor = -0.05 production_factory_efficiency_gain_factor = 0.05','岛上承担仓储、维修和补训，减少前线补给消耗。'),
 'v65_settled_regency':('协调处主持中央','political_power_gain = 0.15 planning_speed = 0.05','朴系主持实际调度，名义政府与军区继续按协议分担军费。'),
}
put(Path('common/ideas/v65_park_government.txt'),'ideas = { country = { '+'\n'.join(f'{key} = {{ picture = generic_army_chief allowed = {{ always = no }} modifier = {{ {mods} }} }}' for key,(_,mods,_) in ideas.items())+' } }')
for key,(name,_,desc) in ideas.items():L[key]=name;L[key+'_desc']=desc
allowed='OR = { tag = PKS AND = { tag = SVN has_country_flag = v65_union_complete } }'
put(Path('common/decisions/categories/v65_contracts.txt'),f'v65_contract_operations = {{ icon = GFX_decision_generic_military allowed = {{ {allowed} }} visible = {{ always = yes }} }}')
put(Path('common/decisions/v65_contracts.txt'),'''v65_contract_operations = {
 v65_open_credit = { icon = generic_political_discourse cost = 60 days_re_enable = 90 available = { check_variable = { v65_contract_credit < 9 } } complete_effect = { add_to_variable = { v65_contract_credit = 2 } v65_credit = yes } ai_will_do = { factor = 0.5 } }
 v65_claim_supplies = { icon = generic_political_discourse cost = 35 days_re_enable = 60 available = { NOT = { has_country_flag = v65_audit_frozen } } complete_effect = { v65_claim_supplies = yes } ai_will_do = { factor = 0.5 } }
 v65_call_koreans = { icon = generic_prepare_civil_war cost = 100 days_re_enable = 180 available = { check_variable = { v65_contract_credit > 1 } check_variable = { v65_korean_calls < 3 } capital_scope = { is_fully_controlled_by = ROOT } } complete_effect = { subtract_from_variable = { v65_contract_credit = 2 } add_to_variable = { v65_korean_calls = 1 } v65_free_korean_detachment = yes } ai_will_do = { factor = 0.5 } }
 v65_raise_proxy = { icon = generic_prepare_civil_war cost = 60 days_re_enable = 90 available = { check_variable = { v65_contract_credit > 0 } capital_scope = { is_fully_controlled_by = ROOT } } complete_effect = { subtract_from_variable = { v65_contract_credit = 1 } v65_free_proxy = yes } ai_will_do = { factor = 0.5 } }
}''')
put(Path('events/v65_park_government.txt'),'add_namespace = v65gov\ncountry_event = { id = v65gov.1 is_triggered_only = yes title = v65gov.1.t desc = v65gov.1.d picture = GFX_report_event_generic_read_write option = { name = v65gov.1.a } }\ncountry_event = { id = v65gov.9 hidden = yes is_triggered_only = yes immediate = { clr_country_flag = v65_audit_frozen } }')
# Preserve contractor resources before the old country disappears; invoke the phase after annexation.
p=M/'common/scripted_effects/v65_union_sanctuary.txt';blocks=pdx.read(p)
for k,_,body in blocks:
 if k!='v65_finalize_union':continue
 for a,_,branch in body:
  if a!='if':continue
  for b,_,country in branch:
   if b!='PKS':continue
   country[:0]=pdx.parse('send_equipment_fraction = { target = SVN value = 1 } SVN = { '+' '.join(f'set_variable = {{ {v} = PKS.{v} }}' for v in ['v65_personal_network','v65_contract_credit','v65_ledger_claims','v65_korean_calls'])+' if = { limit = { PKS = { has_country_flag = v65_audit_frozen } } set_country_flag = v65_audit_frozen country_event = { id = v65gov.9 days = 90 } } }')
  for b,_,country in branch:
   if b=='SVN' and any(z[0]=='annex_country' for z in country):country+=pdx.parse('v65_begin_park_government = yes')
p.write_text(pdx.dump(blocks),encoding='utf-8')
# UI state and economic channels survive an already-completed union in a compatible save.
put(Path('common/on_actions/v65_park_government.txt'),'on_actions = { on_daily = { effect = { SVN = { v65_begin_park_government = yes } } } }')
for lang in ['simp_chinese','english']:put(Path(f'localisation/{lang}/zzzzzzzz_v65_government_l_{lang}.yml'),loc_text(L,lang))
import json
(R/'park-government-manifest.json').write_text(json.dumps({'tree':'v65_park_government','focuses':36,'art':art_assignments},indent=2),encoding='utf-8')
print('Park governing phase: 36 focuses, Korean reinforcement, proxy regiments and audited supply claims')
