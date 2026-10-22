"""Park's private interests cross borders without annexing the partner's land."""
from pathlib import Path
from build_campaign import M,R,put
from long_foundation import loc_text

PARTNERS={'SVN':'西贡总统府','DNM':'岘港军区','HLC':'西原军区','MKG':'湄公河军区','BHD':'东南军区','PHQ':'富国岛特别区','KHM':'柬埔寨王国'}
L={
 'v65_personal_connections':'朴的私人通讯录',
 'v65_personal_connections_desc':'私产：[SVN.v65_private_wealth|0]/100　享受：[SVN.v65_private_comfort|0]/100\n这里按人情办事，不按国界涂色。关系25可租借军需站，50可分红，70可介入军区任命。每个关系50以上、仍与朴和平的外部伙伴每月提供1点私产；关系每月消退1点，战时断交额外消退5点。\n朴移驻或接管南越不会重建这本账。',
 'v65_personal_network_actor':'由朴系主持私人网络',
 'v65_network_supply':'共用仓库与私人车队','v65_network_supply_desc':'租来的仓库和运输关系暂时降低补给损耗。地主和司令各收一份，路线仍能开通。',
 'v65_private_staff':'有人替司令接电话','v65_private_staff_desc':'秘书、副官和招待处各有分工。司令休息时，送来的文件也有人签收。',
 'v65_private_holiday_decision':'把周末留给自己',
 'v65_private_holiday_decision_desc':'支出10私产，享受增加15，返还15政治点；每90天一次。招待处能挡住杂事，挡不住战线。',
 'v65network.1.t':'今天的电话由副官接',
 'v65network.1.d':'行李已经送到住处。副官捧着行程表追过来，还想把两场接见塞进下午。\n\n朴把接见划给了参谋。招待费不够就从自己的账上走，谁也别把这次休假写成视察。\n\n“急件怎么办？”\n“你先看看有多急。”',
 'v65network.1.a':'行李放下，电话拿远一点。',
 'v65network.2.t':'通讯录也要有人维护',
 'v65network.2.d':'同一条公路，军区收通行费，地方团收保护费，仓库还要一份装卸费。私人账本每月结一次，没人打算等战争结束再算。',
 'v65network.2.a':'把熟人的份额也算进去。',
}
triggers='v65_personal_network_actor = { OR = { tag = PKS has_idea = v65_park_shadow_ruler } }\n'
effects='''v65_refresh_personal_network = {
 clamp_variable = { var = v65_private_wealth min = 0 max = 100 }
 clamp_variable = { var = v65_private_comfort min = 0 max = 100 }
'''
for tag in PARTNERS:effects+=f' clamp_variable = {{ var = v65_network_{tag} min = 0 max = 100 }}\n'
effects+='''}
v65_private_holiday = { if = { limit = { v65_personal_network_actor = yes SVN = { check_variable = { v65_private_wealth > 9 } } }
 SVN = { subtract_from_variable = { v65_private_wealth = 10 } add_to_variable = { v65_private_comfort = 15 } v65_refresh_personal_network = yes }
 add_political_power = 15 add_timed_idea = { idea = v65_private_staff days = 45 }
} }
'''
decisions='v65_personal_connections = {\n'
events='add_namespace = v65network\n'
events+='country_event = { id = v65network.1 title = v65network.1.t desc = v65network.1.d picture = GFX_report_event_generic_read_write is_triggered_only = yes option = { name = v65network.1.a v65_private_holiday = yes } }\n'
dividend='v65_network_dividend = {\n'
month='SVN = { if = { limit = { has_country_flag = v65_private_book_open } v65_network_dividend = yes subtract_from_variable = { v65_private_comfort = 3 }\n'
for i,(tag,name) in enumerate(PARTNERS.items(),10):
    var=f'v65_network_{tag}'
    # A rebel command can remain Park's contact while fighting the central government.
    # Once Park takes the central government, a hostile command is excluded automatically.
    peace=f'{tag} = {{ exists = yes capital_scope = {{ is_fully_controlled_by = {tag} }} }} if = {{ limit = {{ PKS = {{ exists = yes }} }} {tag} = {{ NOT = {{ has_war_with = PKS }} }} }} else = {{ {tag} = {{ NOT = {{ has_war_with = SVN }} }} }}'
    triggers+=f'v65_park_partner_{tag} = {{ {peace} }}\n'
    source=f'v65_park_partner_{tag} = yes NOT = {{ tag = {tag} }}'
    accept=f'v65_accept_contact_{tag}'
    effects+=f'''{accept} = {{ if = {{ limit = {{ tag = {tag} has_global_flag = v65_pending_contact_{tag} v65_park_partner_{tag} = yes }}
 clr_global_flag = v65_pending_contact_{tag} add_political_power = 20
 SVN = {{ add_to_variable = {{ {var} = 20 }} v65_refresh_personal_network = yes }}
 if = {{ limit = {{ PKS = {{ exists = yes }} }} PKS = {{ country_event = {{ id = v65network.{i+100} days = 1 }} }} }}
 else = {{ SVN = {{ country_event = {{ id = v65network.{i+100} days = 1 }} }} }}
}} }}
v65_open_contact_{tag} = {{ if = {{ limit = {{ v65_personal_network_actor = yes {source} NOT = {{ has_global_flag = v65_pending_contact_{tag} }} }}
 set_global_flag = v65_pending_contact_{tag} {tag} = {{ country_event = {{ id = v65network.{i} days = 1 }} }}
 SVN = {{ country_event = {{ id = v65network.{i+200} days = 30 }} }}
}} }}
v65_network_depot_{tag} = {{ if = {{ limit = {{ v65_personal_network_actor = yes {source} SVN = {{ check_variable = {{ {var} > 24 }} check_variable = {{ v65_private_wealth > 7 }} }} }}
 SVN = {{ subtract_from_variable = {{ v65_private_wealth = 8 }} add_to_variable = {{ {var} = 3 }} v65_refresh_personal_network = yes }}
 add_timed_idea = {{ idea = v65_network_supply days = 90 }}
 {tag} = {{ add_timed_idea = {{ idea = v65_network_supply days = 90 }} subtract_from_variable = {{ v65_local_unrest = 1 }} v65_refresh_society = yes }}
}} }}
'''
    L.update({f'v65_contact_{tag}':f'托人递话：{name}',f'v65_contact_{tag}_desc':f'{name}关系：[SVN.{var}|0]/100。花35政治点递交合作提议；对方接受后关系增加20，对方得到20政治点。拒绝不会退还活动费。每90天一次。提议30天失效。',f'v65_depot_{tag}':f'在{name}合用仓库',f'v65_depot_{tag}_desc':'关系25、私产8以上：支出8私产及25政治点，双方获得90天补给消耗减免，伙伴的地方动荡降低1，关系增加3。不转移领土。',f'v65network.{i}.t':'有人替朴来递话',f'v65network.{i}.d':f'来人带了一封私信，谈的是{name}的仓库、运输和军官往来。信上没提改变隶属关系，也没要求把部队交出去。\n\n条件很简单：彼此留一条能办事的线，往后有利可图时互相照应。',f'v65network.{i}.a':'替我回信，先留一个联络处。',f'v65network.{i}.b':'让他找别人。',f'v65network.{i+100}.t':f'{name}回信了',f'v65network.{i+100}.d':'地址、姓名和联络时间都在纸上。接电话的人未必最有权，但至少知道谁能签字。余下的要靠来往把关系养起来。',f'v65network.{i+100}.a':'把号码抄进私人本子。'})
    events+=f'''country_event = {{ id = v65network.{i} title = v65network.{i}.t desc = v65network.{i}.d picture = GFX_report_event_generic_sign_treaty is_triggered_only = yes
 trigger = {{ has_global_flag = v65_pending_contact_{tag} v65_park_partner_{tag} = yes }}
 option = {{ name = v65network.{i}.a ai_chance = {{ factor = 80 }} {accept} = yes }}
 option = {{ name = v65network.{i}.b ai_chance = {{ factor = 20 }} clr_global_flag = v65_pending_contact_{tag} }} }}
country_event = {{ id = v65network.{i+100} title = v65network.{i+100}.t desc = v65network.{i+100}.d picture = GFX_report_event_generic_read_write is_triggered_only = yes option = {{ name = v65network.{i+100}.a }} }}
country_event = {{ id = v65network.{i+200} hidden = yes is_triggered_only = yes immediate = {{ clr_global_flag = v65_pending_contact_{tag} }} }}
'''
    decisions+=f'''v65_contact_{tag} = {{ icon = generic_political_discourse cost = 35 visible = {{ {source} }} available = {{ SVN = {{ check_variable = {{ {var} < 100 }} }} NOT = {{ has_global_flag = v65_pending_contact_{tag} }} }} days_re_enable = 90 complete_effect = {{ v65_open_contact_{tag} = yes }} ai_will_do = {{ factor = 0.3 }} }}
v65_depot_{tag} = {{ icon = generic_prepare_civil_war cost = 25 visible = {{ {source} }} available = {{ SVN = {{ check_variable = {{ {var} > 24 }} check_variable = {{ v65_private_wealth > 7 }} }} }} days_re_enable = 90 complete_effect = {{ v65_network_depot_{tag} = yes }} ai_will_do = {{ factor = 0.3 }} }}
'''
    dividend+=f'if = {{ limit = {{ v65_park_partner_{tag} = yes check_variable = {{ {var} > 49 }} '+('PKS = { exists = yes }' if tag=='SVN' else '')+f' }} add_to_variable = {{ v65_private_wealth = 1 }} }}\n'
    month+=f'if = {{ limit = {{ check_variable = {{ {var} > 0 }} }} subtract_from_variable = {{ {var} = 1 }} if = {{ limit = {{ NOT = {{ v65_park_partner_{tag} = yes }} }} subtract_from_variable = {{ {var} = 5 }} }} }}\n'
    if tag in ['DNM','HLC','MKG','BHD','PHQ']:
        for slug,delta in [('guarantee',20),('intrigue',-15)]:
            key=f'v65_network_{slug}_{tag}'
            L[key]=('替西贡担保：' if slug=='guarantee' else '给司令另留退路：')+name
            L[key+'_desc']=f'关系70以上、15私产及80政治点，改变该区对中央的忠诚{delta:+}。朴与该军区的私人关系增加5；承诺由朴的人脉承担，不会立即改变军区归属。'
            decisions+=f'''{key} = {{ icon = generic_political_discourse cost = 80 visible = {{ {source} {tag} = {{ v65_under_central_command = yes }} }} available = {{ SVN = {{ check_variable = {{ {var} > 69 }} check_variable = {{ v65_private_wealth > 14 }} }} }} days_re_enable = 120 complete_effect = {{ SVN = {{ subtract_from_variable = {{ v65_private_wealth = 15 }} add_to_variable = {{ {var} = 5 }} v65_refresh_personal_network = yes }} {tag} = {{ add_to_variable = {{ v65_regional_loyalty = {delta} }} clamp_variable = {{ var = v65_regional_loyalty min = 0 max = 100 }} }} }} ai_will_do = {{ factor = 0 }} }}\n'''
effects+=dividend+'v65_refresh_personal_network = yes }\n'
month+='v65_refresh_personal_network = yes } }'
decisions+='v65_private_holiday_decision = { icon = generic_political_discourse cost = 0 available = { SVN = { check_variable = { v65_private_wealth > 9 } } } days_re_enable = 90 complete_effect = { country_event = { id = v65network.1 days = 1 } } ai_will_do = { factor = 0.2 } }\n}'
put(Path('common/scripted_triggers/v65_personal_network.txt'),triggers)
put(Path('common/scripted_effects/v65_personal_network.txt'),effects)
put(Path('common/decisions/v65_personal_network.txt'),decisions)
put(Path('common/decisions/categories/v65_personal_network.txt'),'v65_personal_connections = { icon = GFX_decision_generic_military allowed = { always = yes } visible = { v65_personal_network_actor = yes } }')
put(Path('events/v65_personal_network.txt'),events)
put(Path('common/on_actions/v65_personal_network.txt'),'''on_actions = { on_startup = { effect = { SVN = { if = { limit = { NOT = { has_country_flag = v65_private_book_open } } set_country_flag = v65_private_book_open set_variable = { v65_private_wealth = 25 } set_variable = { v65_private_comfort = 10 } } } } } on_monthly = { effect = { '''+month+' } } }')
put(Path('common/ideas/v65_personal_network.txt'),'''ideas = { country = {
 v65_network_supply = { picture = generic_army_chief allowed = { always = no } modifier = { supply_consumption_factor = -0.1 } }
 v65_private_staff = { picture = generic_political_reform allowed = { always = no } modifier = { political_power_gain = 0.1 } }
} }''')
for lang in ['simp_chinese','english']:put(Path(f'localisation/{lang}/zzzzzzzzzzzz_v65_personal_network_l_{lang}.yml'),loc_text(L,lang))
print('Park network:',len(PARTNERS),'partners; proposals, shared depots, dividends and command interference')
