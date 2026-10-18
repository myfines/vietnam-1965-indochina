"""Command recall, mobile headquarters and competition over invented war credit."""
from pathlib import Path
import sys
from build_campaign import M,R,put
from long_foundation import REGIONS,loc_text
sys.path.insert(0,str(R/'vendor'));import pdx

L={
 'v65_private_war':'朴系：驻地、账面与派系',
 'v65_private_war_desc':'驻地随当前首都变化。移动司令部会接收一州和当地指挥权，不会搬走原驻地的所有部队。\n纸面战功 [?v65_paper_victories|0]　实际战功 [?v65_real_victories|0]\n日海 [?v65_clique_daihai|0]　参谋本部 [?v65_clique_staff|0]　南方代理 [?v65_clique_proxy|0]\n派系要求：[v65_faction_request]。各派争的是合同、任命和报功署名。',
 'v65_no_request':'暂无到期要求','v65_daihai_request':'日海要求运输合同','v65_staff_request':'参谋本部要求报功名额','v65_proxy_request':'南方军官要求军饷份额',
 'v65_paper_claim':'把友军战果写进本部捷报',
 'v65_paper_claim_desc':'35政治点。纸面战功+2，日海势力+5，南方代理势力-5。调用现有军需申报机制；核查失败会冻结申报。每60天一次。',
 'v65_settle_clique':'签下本期派系分账',
 'v65_settle_clique_desc':'60政治点。满足当前派系要求并支付其具体报酬，清除本期要求。每季度会有新的争夺；忽略到期要求会使相应渠道停止工作。',
 'v65_raid_budgets':'把南方友军编进本部供应表',
 'v65_raid_budgets_desc':'50政治点，代理派系+10，南越中央威望-5，获得400支步枪与3000人力。每120天一次。',
 'v65_park_coercion':'执行封锁与连坐清剿计划',
 'v65_park_coercion_desc':'80政治点。已控制州网络降低两级，本地叛乱压力-4；民心-12，控制地区的征用与封锁损失合计5000可用人力。形成90天强制治安状态。这是冷酷的军事选择，不增加主角的心理负担数值。',
 'v65_park_coercion_spirit':'封锁与连坐清剿',
 'v65_park_coercion_spirit_desc':'通过驻军、征用与集体惩罚压低活动空间；政治点收入下降，守备效率提高。民心损失不会因清剿期结束而返还。',
 'v65_democratic_general':'“民主神将”',
 'v65_democratic_general_desc':'报纸、上级和军需合同共同承认的常胜名号。获得至少8点战功，其中至少2点来自实际控制敌方州或压低地方网络；其余可以来自战报。每日政治点+0.15、军需信用上限仍为10。',
 'v65_democratic_title':'让报纸采用“民主神将”的称呼',
 'v65_democratic_title_desc':'需要战功总计8、实际战功至少2。消耗50政治点，获得持续声望精神。',
 'v65_clique_contract_block':'日海扣住合同','v65_clique_contract_block_desc':'运输合同分配未满足日海的要求。采购效率与政治点收入下降，结清本期分账后解除。',
 'v65_clique_staff_block':'参谋本部压住任命','v65_clique_staff_block_desc':'报功署名和晋升名额没有谈妥。每日指挥点和计划速度下降。',
 'v65_clique_proxy_block':'南方军官扣饷扣人','v65_clique_proxy_block_desc':'代理军官拒绝继续交出人力和军需。组织度与政治点收入下降。',
 'v65rev.1.t':'给朴世诚的表彰令',
 'v65rev.1.d':'西贡发来表彰，首尔准备转载。战报已经盖章，军需处也收到了副本。朴让参谋再印一份，送去谈下一批补给。',
 'v65rev.1.a':'勋章上墙，战报进账。',
 'v65rev.2.t':'纱良也有一份战功',
 'v65rev.2.d':'纱良交来的战报与友军那份用了同一张缴获照片。参谋问署谁的名字；朴看的是追加补给那一栏。',
 'v65rev.2.a':'先算本部的，给他一个署名。','v65rev.2.b':'这次让他拿，欠账记下。',
}
effects=''
decisions='v65_command_politics = {\n'
for tag,(cn,_,capital,*_) in REGIONS.items():
    # Force is paid for in political authority, not blocked by a loyalty threshold.
    key='v65_dissolve_'+tag;L[key]='强制撤销'+cn
    L[key+'_desc']='100政治点。收回全部所有权、库存与部队，接收军区人物。无需忠诚门槛；中央威望-10，其余听令军区忠诚-10。已公开叛乱或与中央交战的军区须通过战争收回。'
    valid=f'tag = SVN {tag} = {{ exists = yes v65_under_central_command = yes }} NOT = {{ has_war_with = {tag} }}'
    effects+=f'v65_dissolve_{tag} = {{ if = {{ limit = {{ {valid} }} {tag} = {{ send_equipment_fraction = {{ target = SVN value = 1 }} every_owned_state = {{ add_core_of = SVN }} every_character = {{ set_nationality = SVN }} }} annex_country = {{ target = {tag} transfer_troops = yes }} subtract_from_variable = {{ v65_central_prestige = 10 }} '
    for other in REGIONS:
        effects+=f'{other} = {{ if = {{ limit = {{ exists = yes v65_under_central_command = yes }} subtract_from_variable = {{ v65_regional_loyalty = 10 }} clamp_variable = {{ var = v65_regional_loyalty min = 0 max = 100 }} }} }} '
    effects+='v65_refresh_command = yes } }\n'
    decisions+=f'{key} = {{ icon = generic_prepare_civil_war cost = 100 visible = {{ {valid} }} complete_effect = {{ {key} = yes }} ai_will_do = {{ factor = 0 }} }}\n'
    for sid in range(11,32):
        if sid==capital:continue
        key=f'v65_recall_{tag}_{sid}';L[key]=f'从{cn}收回$V65_STATE_{sid}$';L[key+'_desc']='25政治点。收回完整控制的非首府州；军区忠诚-8。首府须通过撤销整个军区收回，避免留下没有驻地的军区。'
        held=f'{sid} = {{ is_fully_controlled_by = {tag} }} {tag} = {{ NOT = {{ capital_scope = {{ state = {sid} }} }} }}'
        effects+=f'{key} = {{ if = {{ limit = {{ {valid} {tag} = {{ owns_state = {sid} }} {held} }} {sid} = {{ add_core_of = SVN }} transfer_state = {sid} {tag} = {{ subtract_from_variable = {{ v65_regional_loyalty = 8 }} clamp_variable = {{ var = v65_regional_loyalty min = 0 max = 100 }} }} }} }}\n'
        decisions+=f'{key} = {{ icon = generic_political_discourse cost = 25 visible = {{ {valid} has_country_flag = v65_selected_{tag} {tag} = {{ owns_state = {sid} }} }} available = {{ {held} }} complete_effect = {{ {key} = yes }} ai_will_do = {{ factor = 0 }} }}\n'
decisions+='}\nv65_private_war = {\n'
for sid in [11,12,15,16,19,22,25,28,31]:
    key=f'v65_move_park_{sid}';L[key]='移驻$V65_STATE_'+str(sid)+'$'
    L[key+'_desc']='50政治点，每90天一次。目标须由本部或未叛乱的南方盟军完整控制；若属于盟军，该州移交本部。原有领土保留，直属部队须自行调动。岛上驻地需先完成富国岛计划或取得该岛。'
    donors=['SVN','DNM',*REGIONS]
    consent='OR = { owns_state = '+str(sid)+' '+' '.join(f'AND = {{ {t} = {{ owns_state = {sid} NOT = {{ has_country_flag = v65_rebel_command }} }} is_in_faction_with = {t} NOT = {{ has_war_with = {t} }} }}' for t in donors)+' }'
    available=f'{consent} {sid} = {{ OR = {{ is_fully_controlled_by = PKS '+' '.join('is_fully_controlled_by = '+t for t in donors)+' } }'
    if sid==31:available+=' OR = { owns_state = 31 has_country_flag = v65_island_plan_ready }'
    if sid==25:available+=' tag = SVN'
    actor='OR = { tag = PKS AND = { tag = SVN has_country_flag = v65_union_complete } }'
    effects+=f'{key} = {{ if = {{ limit = {{ {actor} {available} NOT = {{ has_country_flag = v65_move_cooldown }} }} {sid} = {{ add_core_of = PREV }} transfer_state = {sid} set_capital = {{ state = {sid} }} set_country_flag = v65_move_cooldown country_event = {{ id = v65rev.9 days = 90 }} }} }}\n'
    decisions+=f'{key} = {{ icon = generic_political_discourse cost = 50 visible = {{ {actor} NOT = {{ capital_scope = {{ state = {sid} }} }} }} available = {{ {available} NOT = {{ has_country_flag = v65_move_cooldown }} }} complete_effect = {{ {key} = yes }} ai_will_do = {{ factor = 0 }} }}\n'
for slug,cost,condition,effect in [
 ('paper_claim',35,'NOT = { has_country_flag = v65_audit_frozen }','v65_claim_supplies = yes add_to_variable = { v65_paper_victories = 2 } add_to_variable = { v65_clique_daihai = 5 } subtract_from_variable = { v65_clique_proxy = 5 }'),
 ('raid_budgets',50,'SVN = { exists = yes }','add_to_variable = { v65_clique_proxy = 10 } add_equipment_to_stockpile = { type = infantry_equipment_2 amount = 400 producer = ROOT } add_manpower = 3000 SVN = { subtract_from_variable = { v65_central_prestige = 5 } v65_refresh_command = yes }'),
 ('park_coercion',80,'any_owned_state = { is_fully_controlled_by = ROOT check_variable = { v65_rear_level > 0 } }','every_owned_state = { limit = { is_fully_controlled_by = ROOT check_variable = { v65_rear_level > 0 } } subtract_from_variable = { v65_rear_level = 2 } v65_refresh_rear_state = yes } subtract_from_variable = { v65_local_unrest = 4 } subtract_from_variable = { v65_public_trust = 12 } add_manpower = -5000 add_timed_idea = { idea = v65_park_coercion_spirit days = 90 } add_to_variable = { v65_real_victories = 1 }'),
 ('democratic_title',50,'check_variable = { v65_total_victories > 7 } check_variable = { v65_real_victories > 1 } NOT = { has_idea = v65_democratic_general }','add_ideas = v65_democratic_general'),
 ('settle_clique',60,'check_variable = { v65_clique_request > 0 }','v65_settle_clique = yes'),
]:
    decisions+=f'v65_{slug} = {{ icon = generic_political_discourse cost = {cost} available = {{ {condition} }} days_re_enable = {120 if slug=="raid_budgets" else 90 if slug=="park_coercion" else 60} complete_effect = {{ {effect} v65_refresh_factions = yes v65_refresh_society = yes }} ai_will_do = {{ factor = 0.5 }} }}\n'
decisions+='}'
effects+='''v65_refresh_factions = {
 clamp_variable = { var = v65_clique_daihai min = 0 max = 100 } clamp_variable = { var = v65_clique_staff min = 0 max = 100 } clamp_variable = { var = v65_clique_proxy min = 0 max = 100 }
 set_variable = { v65_total_victories = v65_paper_victories } add_to_variable = { v65_total_victories = v65_real_victories }
}
v65_settle_clique = {
 if = { limit = { check_variable = { v65_clique_request = 1 } } add_to_variable = { v65_clique_daihai = 10 } add_to_variable = { v65_contract_credit = 2 } v65_credit = yes }
 else_if = { limit = { check_variable = { v65_clique_request = 2 } } add_to_variable = { v65_clique_staff = 10 } add_to_variable = { v65_paper_victories = 1 } }
 else_if = { limit = { check_variable = { v65_clique_request = 3 } } add_to_variable = { v65_clique_proxy = 10 } add_manpower = 1500 }
 set_variable = { v65_clique_request = 0 } remove_ideas = { v65_clique_contract_block v65_clique_staff_block v65_clique_proxy_block }
}
v65_factions_month = {
 if = { limit = { check_variable = { v65_clique_request > 0 } } add_to_variable = { v65_request_age = 1 }
  if = { limit = { check_variable = { v65_request_age > 1 } }
   if = { limit = { check_variable = { v65_clique_request = 1 } } add_ideas = v65_clique_contract_block }
   else_if = { limit = { check_variable = { v65_clique_request = 2 } } add_ideas = v65_clique_staff_block }
   else = { add_ideas = v65_clique_proxy_block }
  }
 }
 else = { add_to_variable = { v65_clique_quarter = 1 }
  if = { limit = { check_variable = { v65_clique_quarter > 2 } } set_variable = { v65_clique_quarter = 0 } set_variable = { v65_request_age = 0 }
   random_list = { 1 = { set_variable = { v65_clique_request = 1 } } 1 = { set_variable = { v65_clique_request = 2 } } 1 = { set_variable = { v65_clique_request = 3 } } }
  }
 }
 every_controlled_state = { limit = { OR = { is_owned_by = NVN is_owned_by = FNL } NOT = { has_state_flag = v65_park_real_credit } } set_state_flag = v65_park_real_credit PREV = { add_to_variable = { v65_real_victories = 1 } } }
 v65_refresh_factions = yes
}
'''
put(Path('common/scripted_effects/v65_revision.txt'),effects)
put(Path('common/decisions/v65_revision.txt'),decisions)
put(Path('common/decisions/categories/v65_revision.txt'),'v65_private_war = { icon = GFX_decision_generic_military allowed = { OR = { tag = PKS AND = { tag = SVN has_country_flag = v65_union_complete } } } visible = { always = yes } }')
put(Path('common/scripted_localisation/v65_factions.txt'),'defined_text = { name = v65_faction_request '+' '.join(f'text = {{ trigger = {{ check_variable = {{ v65_clique_request = {n} }} }} localization_key = v65_{key}_request }}' for n,key in [(1,'daihai'),(2,'staff'),(3,'proxy')])+' text = { localization_key = v65_no_request } }')
put(Path('events/v65_revision.txt'),'''add_namespace = v65rev
country_event = { id = v65rev.9 hidden = yes is_triggered_only = yes immediate = { clr_country_flag = v65_move_cooldown } }
country_event = { id = v65rev.1 title = v65rev.1.t desc = v65rev.1.d picture = GFX_report_event_generic_read_write is_triggered_only = yes option = { name = v65rev.1.a add_political_power = 50 PKS = { add_to_variable = { v65_paper_victories = 1 } } } }
country_event = { id = v65rev.2 title = v65rev.2.t desc = v65rev.2.d picture = GFX_report_event_generic_read_write is_triggered_only = yes option = { name = v65rev.2.a add_to_variable = { v65_paper_victories = 2 } add_to_variable = { v65_clique_staff = 5 } v65_report_success = yes } option = { name = v65rev.2.b add_to_variable = { v65_clique_proxy = 10 } add_to_variable = { v65_personal_network = 1 } } }
''')
init='set_variable = { v65_clique_daihai = 45 } set_variable = { v65_clique_staff = 65 } set_variable = { v65_clique_proxy = 35 }'
put(Path('common/on_actions/v65_revision.txt'),'on_actions = { on_startup = { effect = { PKS = { '+init+' } } } on_monthly = { effect = { PKS = { if = { limit = { exists = yes } v65_factions_month = yes } } SVN = { if = { limit = { has_country_flag = v65_union_complete } v65_factions_month = yes } } } } on_daily = { effect = { if = { limit = { date > 1966.1.15 NOT = { has_global_flag = v65_shaliang_sent } } set_global_flag = v65_shaliang_sent PKS = { if = { limit = { exists = yes } country_event = { id = v65rev.2 days = 1 } } } SVN = { if = { limit = { has_country_flag = v65_union_complete } country_event = { id = v65rev.2 days = 1 } } } } } } }')
ideas={'v65_park_coercion_spirit':'political_power_gain = -0.1 resistance_target = -0.1','v65_democratic_general':'political_power_gain = 0.15 planning_speed = 0.05','v65_clique_contract_block':'production_factory_efficiency_gain_factor = -0.1 political_power_gain = -0.1','v65_clique_staff_block':'planning_speed = -0.15 command_power_gain_mult = -0.1','v65_clique_proxy_block':'army_org_factor = -0.08 political_power_gain = -0.1'}
put(Path('common/ideas/v65_revision.txt'),'ideas = { country = { '+' '.join(k+' = { picture = generic_political_reform allowed = { always = no } modifier = { '+v+' } }' for k,v in ideas.items())+' } }')
# Mobility removes the permanent Quy Nhon gate from diplomacy.
p=M/'common/scripted_triggers/v65_union_sanctuary.txt';p.write_text(p.read_text().replace('controls_state = 15','capital_scope = { is_fully_controlled_by = PREV }'),encoding='utf-8')
# Replace only the opening notice; subsequent political crises keep their conditions.
p=M/'common/on_actions/v65.txt';p.write_text(p.read_text().replace('id = v65.1 days = 1','id = v65rev.1 days = 1'),encoding='utf-8')
# Keep all private resources when the old tag is absorbed.
p=M/'common/scripted_effects/v65_union_sanctuary.txt';blocks=pdx.read(p)
def inherit(nodes):
    for i,(key,op,value) in enumerate(list(nodes)):
        if key=='annex_country' and any(k=='target' and v=='PKS' for k,_,v in value):
            names=['v65_paper_victories','v65_real_victories','v65_clique_daihai','v65_clique_staff','v65_clique_proxy','v65_clique_request','v65_request_age','v65_clique_quarter']
            persistent=' '.join(f'if = {{ limit = {{ PKS = {{ has_idea = {idea} }} }} add_ideas = {idea} }}' for idea in ['v65_democratic_general','v65_clique_contract_block','v65_clique_staff_block','v65_clique_proxy_block'])
            flags='if = { limit = { PKS = { has_country_flag = v65_island_plan_ready } } set_country_flag = v65_island_plan_ready } if = { limit = { PKS = { has_country_flag = v65_move_cooldown } } set_country_flag = v65_move_cooldown country_event = { id = v65rev.9 days = 90 } }'
            nodes[i:i]=pdx.parse(' '.join(f'set_variable = {{ {v} = PKS.{v} }}' for v in names)+' '+persistent+' '+flags)
        elif isinstance(value,list):inherit(value)
inherit(blocks);p.write_text(pdx.dump(blocks),encoding='utf-8')
# Five existing lines become the actual resource channels; no extra year filler.
rewrites={
 'command':('参谋本部的自己人','上级要战功与名额，本部要调兵和军需。先把能签字的人列出来。','add_to_variable = { v65_clique_staff = 10 }'),
 'quynhon':('驻地跟着合同走','归仁是一个起点，不是永久根据地。联络官把可移驻地点和物资清单交给本部。','add_to_variable = { v65_personal_network = 1 }'),
 'reputation':('胜利先走公文','真假战果都要经过参谋、报社和军需处。同一场胜利可以有几套名字。','add_to_variable = { v65_paper_victories = 1 }'),
 'war_reports':('缴获照片再用一次','照片换个题注，战果就能再报一遍。签字人也要分到名额。','add_to_variable = { v65_paper_victories = 2 }'),
 'patron':('给参谋本部留名额','上级拿走一个署名，本部多拿一批物资。','add_to_variable = { v65_clique_staff = 10 }'),
 'palace':('按继承人的规格送材料','更高层需要一位能不断交出捷报的年轻军官，朴需要他们继续相信。','add_to_variable = { v65_paper_victories = 2 }'),
 'villages':('南方伪军的账也归本部','给番号、给公文，把人力和征收渠道接进本部供应表。','add_to_variable = { v65_clique_proxy = 10 }'),
 'inspection':('让核查的人也有收益','把分账做稳，比找一个清白的账房更有用。','add_to_variable = { v65_clique_daihai = 5 }'),
 'business':('日海财团的驻越账本','运输合同把越南军需与韩国国内的人情账接起来。','add_to_variable = { v65_clique_daihai = 10 }'),
 'company':('国内分红，前线报功','日海收款，上级收材料，本部收补给。','add_to_variable = { v65_contract_credit = 2 }'),
 'power':('把友军变成本部的关系户','南方将领需要军饷和保住番号；朴需要他们的人和地。','add_to_variable = { v65_clique_proxy = 10 }'),
 'remain':('留下的是人脉和合同','谁当名义首长可以再谈，签军饷和军需的权限不能丢。','add_to_variable = { v65_personal_network = 1 }'),
}
p=M/'common/national_focus/v65_PKS.txt';blocks=pdx.read(p);tree=blocks[0][2]
for kind,_,body in tree:
    if kind!='focus':continue
    ident=next(v for k,_,v in body if k=='id');slug=ident.removeprefix('v65_PKS_')
    if slug in rewrites:
        name,desc,reward=rewrites[slug];L[ident]=name;L[ident+'_desc']=desc
        next(v for k,_,v in body if k=='completion_reward').extend(pdx.parse(reward+' v65_refresh_factions = yes v65_credit = yes'))
island=[('plan','富国岛计划','先留一处独立港口，合同和人员才有第二个去处。','set_country_flag = v65_island_plan_ready','port'),('lease','租下岛上驻地','把特别区与本部的港口安排写进移驻清单。','add_to_variable = { v65_personal_network = 1 }','treaty'),('warehouse','把余粮与零件运上岛','库存先上岛，大陆的作战与分账继续。','v65_upgrade_logistics = yes','warehouse'),('contracts','给日海留港口份额','岛上基地也要进入韩国国内的账本。','add_to_variable = { v65_clique_daihai = 10 }','contracts'),('cadres','代理团轮驻离岛','南方军官交出人员，本部负责番号和补给。','v65_free_proxy = yes','proxy'),('staff','离岛也能签发军令','参谋与通信系统必须能随本部转移。','v65_upgrade_signals = yes','radio'),('base','给任何结局留一个基地','不是退出生意，只是换一个更难被端走的办公室。','add_to_variable = { v65_contract_credit = 3 } v65_credit = yes','security')]
for i,(slug,name,desc,reward,art) in enumerate(island):
    ident='v65_PKS_island_'+slug;L[ident]=name;L[ident+'_desc']=desc
    predecessor='v65_PKS_briefing' if i==0 else 'v65_PKS_island_'+island[i-1][0]
    tree.extend(pdx.parse(f'focus = {{ id = {ident} icon = GFX_v65_detail_{art} x = 48 y = {2+i*2} cost = 5 prerequisite = {{ focus = {predecessor} }} completion_reward = {{ {reward} }} }}'))
p.write_text(pdx.dump(blocks),encoding='utf-8')
# A faction dispute closes its specific paid channel, beyond the temporary modifiers.
p=M/'common/decisions/v65_contracts.txt';blocks=pdx.read(p)
for _,_,category in blocks:
    for ident,_,decision in category:
        block={'v65_open_credit':'v65_clique_contract_block','v65_claim_supplies':'v65_clique_contract_block','v65_call_koreans':'v65_clique_staff_block','v65_raise_proxy':'v65_clique_proxy_block'}.get(ident)
        if block:
            condition=next((v for k,_,v in decision if k=='available'),None)
            if condition is not None:condition.extend(pdx.parse('NOT = { has_idea = '+block+' }'))
p.write_text(pdx.dump(blocks),encoding='utf-8')
# Present account-keeping as competing profit strategies, rather than a morality test.
L.update({'v65story.101.b':'限定每层抽成，免得下面把人赶跑。','v65story.102.t':'同一张缴获照片','v65story.102.d':'缴获照片已经报过一次，换一个题注还能再用。上级要数字，军需处要签名；实际补员另有一张表。','v65story.102.a':'战果往上写，先把追加军需领了。','v65story.102.b':'给参谋留实底，免得下次多派任务。','v65story.103.b':'拆开合同，几家一起欠本部的人情。'})
# Personal pressure is administrative competition, never the protagonist's conscience.
for lang in ['simp_chinese','english']:
    L.update({'v65_weariness':'轮换与缺额','v65_weariness_desc':'持续作战造成的缺编和轮换成本，不代表朴的内疚或心理压力。','v65_exhaustion':'补充系统透支','v65_exhaustion_desc':'持续征用使兵员和补给渠道跟不上消耗。这个数值描述组织状态。'})
    put(Path(f'localisation/{lang}/zzzzzzzzzz_v65_revision_l_{lang}.yml'),loc_text(L,lang))
print('Revision: compulsory dissolution, state recall, mobile Park and competing patronage cliques')
