"""Five dated acts, delayed character scenes and the fourteen-year epilogue."""
from build_campaign import put,M,R,REWARDS
from long_foundation import ALL,PLAYABLE,REGIONS,loc_text
from narrative_scenes import SCENES
from pathlib import Path
import json,re

L={};events='add_namespace = v65story\n';schedule='on_actions = { on_daily = { effect = {\n'
def recipients(tags,event_id):
 # Prefer the human in the relevant storyline; union always preserves SVN.
 out='';first=True
 for human in [True,False]:
  for tag in tags:
   out+=('if' if first else 'else_if')+f' = {{ limit = {{ {tag} = {{ exists = yes'+(' is_ai = no' if human else '')+f' }} }} {tag} = {{ country_event = {{ id = v65story.{event_id} days = 1 }} }} }}\n';first=False
 return out
for ident,date,tags,title,body,a,ae,af,b,be,bf in SCENES:
 root=f'v65story.{ident}';sequel=ident+1000;relay=ident+2000
 L.update({root+'.t':title,root+'.d':body,root+'.a':a,root+'.b':b,f'v65story.{sequel}.t':'后来的一封信：'+title,f'v65story.{sequel}.a':af,f'v65story.{sequel}.b':bf,f'v65story.{sequel}.next':'把它收进这一年的档案。'})
 anchor='SVN' if any(t in ['SVN','PKS','PHQ','MKG','HLC'] for t in tags) else tags[0]
 # A surviving alternative anchor is used if a Cambodian government disappears.
 def delayed():return f'{anchor} = {{ country_event = {{ id = v65story.{relay} days = 45 }} }}'
 ai_b=0 if ident==302 else 45
 events+=f'''country_event = {{ id = {root} title = {root}.t desc = {root}.d picture = GFX_report_event_generic_read_write is_triggered_only = yes
 option = {{ name = {root}.a ai_chance = {{ factor = 55 }} set_global_flag = v65_story_{ident}_a {ae} v65_refresh_society = yes {delayed()} }}
 option = {{ name = {root}.b ai_chance = {{ factor = {ai_b} }} set_global_flag = v65_story_{ident}_b {be} v65_refresh_society = yes {delayed()} }}
}}
country_event = {{ id = v65story.{relay} hidden = yes is_triggered_only = yes immediate = {{ {recipients(tags,sequel)} }} }}
country_event = {{ id = v65story.{sequel} immediate = {{ set_global_flag = v65_callback_{ident} }} title = v65story.{sequel}.t picture = GFX_report_event_generic_read_write is_triggered_only = yes
 desc = {{ trigger = {{ has_global_flag = v65_story_{ident}_a }} text = v65story.{sequel}.a }}
 desc = {{ trigger = {{ NOT = {{ has_global_flag = v65_story_{ident}_a }} }} text = v65story.{sequel}.b }}
 option = {{ name = v65story.{sequel}.next
  if = {{ limit = {{ has_global_flag = v65_story_{ident}_a }} add_to_variable = {{ v65_patronage = 2 }} add_to_variable = {{ v65_war_fatigue = 1 }} }}
  else = {{ add_to_variable = {{ v65_public_trust = 3 }} subtract_from_variable = {{ v65_local_unrest = 1 }} }} v65_refresh_society = yes
 }}
}}
'''
 available='OR = { '+' '.join(f'{t} = {{ exists = yes }}' for t in tags)+' }'
 schedule+=f'if = {{ limit = {{ date > {date} NOT = {{ has_global_flag = v65_scene_{ident}_sent }} {available} }} set_global_flag = v65_scene_{ident}_sent {recipients(tags,ident)} }}\n'

ACTS=[
 (1968,'军援离开之后','撤军表使部队开始清点自己真正掌握的东西：仓库、军饷、村庄和能继续工作的维修队。对外援的依赖正在变成对军区和合同的依赖。'),
 (1971,'一张地图，几套命令','机动军、岛上后方与地方军区都希望获得更多资源。共同的敌人仍在，但谁来签发任命、谁来支付军饷，已经决定了命令能够走多远。'),
 (1974,'保存什么，放弃什么','西原与首都的危机让各派重新计算承诺。保存精锐、保护平民、保住政府与保护私人网络，越来越难同时做到。'),
 (1977,'战争进入地方社会','正规战线没有消除夜间的枪声。地方行政、难民安置与军官利益构成了另一张地图。继续征集容易，重建合作则需要兑现过去的承诺。'),
 (1979,'十四年以后','有些军官还在等待下一次攻势，有些家庭只希望知道明年的学校是否继续开门。十四年留下的机构、人情和伤口，必须由活下来的人接着管理。'),
]
for n,(year,title,body) in enumerate(ACTS,1):
 key=f'v65story.{800+n}';L.update({key+'.t':f'{year}：'+title,key+'.d':body+'\n\n案头的数字记录着此前的选择：民心、派系依赖、战争疲劳和军区关系都将带入这一幕。国策中的军事优先与社会契约互斥，新的阶段替换旧政策。',key+'.a':'继续写这一年的记录。'})
 events+=f'country_event = {{ id = {key} title = {key}.t desc = {key}.d picture = GFX_report_event_generic_read_write is_triggered_only = yes option = {{ name = {key}.a }} }}\n'
L.update({
 'v65_story_archive':'战时档案与人物关系',
 'v65_story_archive_desc':'朴与西贡的互信：[SVN.v65_park_trust|0]　首都政治关系：[SVN.v65_thieu_trust|0]　离岛信任：[SVN.v65_island_trust|0]\n每年的关键场景按日期出现。选择会留下全局剧情标记，并在45天后的信件或报告中回响。正式合并会保留西贡作为后续剧情的锚点。',
 'v65story.901.t':'十四年之后，留下来的是什么',
 'v65story.901.d':'档案柜的最上层装着最早的证件与调令，下面几层是合同、撤退计划、安置名单和没有兑现的承诺。\n\n秘书问，最后一卷应该叫什么。没有人愿意把它简单地叫作胜利，或者失败。\n\n民心、派系网络与长期疲劳仍将影响今后的生活。这是十四年叙事的尾声；玩家可以保留现有秩序、在条件允许时推动停火，也可以继续战争。',
 'v65story.901.park':'总统仍在台前。协调会的电话、任命名单与合同则经过另一张桌子。朴世诚没有需要公开宣布的头衔，却必须继续兑现对军区的保证。\n\n十四年把年轻军官变成了一个制度。人们记得他的方式，取决于制度给他们留下了什么。',
 'v65story.901.island':'大陆的消息仍然乘船抵达。岛上已经有了新的学校、新的军营，也有了不认识大陆故乡的孩子。\n\n离岛政权可以继续准备返回，也可以先决定怎样让留在这里的人生活下去。',
 'v65story.901.a':'承认我们维持下来的秩序，继续治理。',
 'v65story.901.b':'以民意和疲劳为依据，结束目前的战争。',
 'v65story.901.c':'战争还没有结束。',
 'v65_memory_of_war':'十四年的共同记忆','v65_memory_of_war_desc':'共同经历提供了一点合作的基础，却不会抹去地方社会与军官网络之间的分歧。',
 'v65_fragile_peace':'脆弱而真实的停火','v65_fragile_peace_desc':'停火使社会可以喘息。军队转向防御，未解决的争执仍需以制度与谈判处理。',
})
events+='''country_event = { id = v65story.901 title = v65story.901.t picture = GFX_report_event_generic_read_write is_triggered_only = yes
 desc = { trigger = { has_idea = v65_park_shadow_ruler } text = v65story.901.park }
 desc = { trigger = { NOT = { has_idea = v65_park_shadow_ruler } capital_scope = { state = 31 } } text = v65story.901.island }
 desc = { trigger = { NOT = { has_idea = v65_park_shadow_ruler } NOT = { capital_scope = { state = 31 } } } text = v65story.901.d }
 option = { name = v65story.901.a add_ideas = v65_memory_of_war set_country_flag = v65_epilogue_accepted }
 option = { name = v65story.901.b trigger = { check_variable = { v65_public_trust > 59 } check_variable = { v65_war_fatigue > 39 } }
  if = { limit = { has_war_with = NVN } white_peace = NVN }
  if = { limit = { has_war_with = FNL } white_peace = FNL }
  if = { limit = { has_war_with = SVN } white_peace = SVN }
  if = { limit = { has_war_with = KHM } white_peace = KHM }
  if = { limit = { has_war_with = RKH } white_peace = RKH }
  add_ideas = v65_fragile_peace set_country_flag = v65_epilogue_accepted subtract_from_variable = { v65_war_fatigue = 15 } v65_refresh_society = yes
 }
 option = { name = v65story.901.c add_war_support = 0.03 set_country_flag = v65_epilogue_accepted }
}
'''
for tag in ALL:
 schedule+=f'{tag} = {{ if = {{ limit = {{ exists = yes is_ai = no date > 1979.10.27 NOT = {{ has_country_flag = v65_epilogue_seen }} }} set_country_flag = v65_epilogue_seen country_event = {{ id = v65story.901 days = 1 }} }} }}\n'
schedule+='} } }'
put(Path('common/on_actions/v65_narrative.txt'),schedule)
put(Path('events/v65_narrative.txt'),events)
ideas_path=M/'common/ideas/v65_long_campaign.txt';text=ideas_path.read_text(encoding='utf-8').rsplit('} }',1)[0]
text+='v65_memory_of_war = { picture = generic_political_reform allowed = { always = no } modifier = { stability_factor = 0.04 political_power_gain = 0.08 } }\n'
text+='v65_fragile_peace = { picture = generic_political_reform allowed = { always = no } modifier = { stability_factor = 0.10 army_attack_factor = -0.05 } }\n} }'
ideas_path.write_text(text,encoding='utf-8')

def focus(ident,name,desc,icon,x,y,reward,parent=None,cost=5,available='',exclusive=''):
 L[ident]=name;L[ident+'_desc']=desc
 return f'focus = {{ id = {ident} icon = GFX_v65_focus_{icon} x = {x} y = {y} cost = {cost} '+(f'prerequisite = {{ {parent} }} ' if parent else '')+f'{available} {exclusive} completion_reward = {{ {reward} }} ai_will_do = {{ factor = 1 }} }}\n'
RKH_BRANCHES=[
 ('根据地的道路','村庄运输队','分散粮食仓','修理缴获武器','雨季前的储备','根据地后勤契约'),
 ('组织与军队','连队骨干训练','核查征集名册','地方干部联络','精锐与补充队','保持指挥与轮换'),
 ('边境与外部援助','建立北方联络','中转仓的条件','核对越境货单','减少单一依赖','自己掌握通道'),
 ('村庄与革命','恢复基层生产','处理地方申诉','保留可用行政','学校与救护站','兑现粮食承诺'),
]
root='v65_RKH_briefing';tree='focus_tree = { id = v65_RKH_tree country = { factor = 0 modifier = { add = 100 tag = RKH } } default = no\n'
tree+=focus(root,'丛林中的另一种国家','革命根据地必须同时面对金边的军队、村庄的生活与越境援助的条件。军事扩张并不能替代治理。','tree',12,0,'add_political_power = 50',cost=2)
for col,labels in enumerate(RKH_BRANCHES):
 parent=root
 for row,label in enumerate(labels):
  ident=f'v65_RKH_base_{col}_{row}';kind=['logistics','training','signals','staff'][col]
  reward=f'v65_upgrade_{kind} = yes' if row%2==0 else 'add_to_variable = { v65_public_trust = 4 } v65_refresh_society = yes'
  tree+=focus(ident,label,f'{label}需要根据地的人员与物资。把军事需求与村庄实际承受能力对照，才能避免短期动员耗尽未来的支持。','tree' if col==3 else 'truck' if col==0 else 'helmet' if col==1 else 'radio',col*8,2+row*2,reward,'focus = '+parent)
  parent=ident
put(Path('common/national_focus/v65_RKH.txt'),tree+'}')
REGION_THEMES={
 'HLC':[['山地道路','熟悉村庄的向导','分散转运仓','雨季运输预案'],['整顿高地驻军','尊重地方语言与习惯','核查警务报告','军政联络处'],['保存部队的条件','核对中央军援','与邻区共享情报','重新谈判战区责任']],
 'MKG':[['河道巡逻队','稻米市场的秩序','分散船运仓','恢复渡口与码头'],['三角洲的地方军','征粮与保护的边界','夜间道路联络','训练本地预备队'],['给西贡的真实报告','军费换来的承诺','保留地方行政','三角洲共同防务']],
 'BHD':[['首都外的通信网','工坊与补给站','保护交通节点','恢复地方采购'],['核查警察名册','清查关卡收入','县城之外的巡逻','保留可靠的基层'],['中央与驻军的合同','分担首都防卫','统一军需结算','东南战区的政治价格']],
 'PHQ':[['扩建岛上港口','难民登记与安置','军属学校与救护','维持海上补给'],['岛防与训练营','精锐的轮换制度','核查大陆情报','本岛预备力量'],['后方也有自己的利益','援助大陆的限度','保存地方行政','一份能够兑现的离岛保证']],
}
for tag,branches in REGION_THEMES.items():
 cn=REGIONS[tag][0];root=f'v65_{tag}_briefing';tree=f'focus_tree = {{ id = v65_{tag}_tree country = {{ factor = 0 modifier = {{ add = 100 tag = {tag} }} }} default = no\n'
 tree+=focus(root,cn+'的第一本账',f'{cn}得到军政自主权，也接过地方叛乱、采购与安置责任。中央援助可以改善关系，不能替代司令部自己的决定。','flag',8,0,'add_political_power = 50',cost=2)
 for col,labels in enumerate(branches):
  parent=root
  for row,label in enumerate(labels):
   ident=f'v65_{tag}_local_{col}_{row}';reward=[REWARDS['supply'],REWARDS['training'],REWARDS['civil'],REWARDS['intel']][row]
   tree+=focus(ident,label,f'{cn}：{label}。地方政府需要把保护承诺、军费与实际执行对上，中央的支援只能解决其中一部分。','truck' if col==0 else 'helmet' if col==1 else 'scroll',col*8,2+row*2,reward,'focus = '+parent)
   parent=ident
 put(Path(f'common/national_focus/v65_{tag}.txt'),tree+'}')

long_count=0
for tag in ALL:
 p=M/f'common/national_focus/v65_{tag}.txt';tree=p.read_text(encoding='utf-8').rstrip()[:-1]
 previous=[f'v65_{tag}_briefing']
 for phase,(year,title,body) in enumerate(ACTS,1):
  ident=f'v65_{tag}_act_{year}';sec=ident+'_security';civil=ident+'_civilian';y=16+(phase-1)*8
  parent=' '.join('focus = '+x for x in previous)
  tree+=focus(ident,title,body+'\n\n本阶段先清点预算与组织，再选择军事优先或社会契约。方案互斥，完成任一方案后才能进入下一阶段。','scroll',4,y,f'add_political_power = 50 country_event = {{ id = v65story.{800+phase} days = 1 }}',parent,10,f'available = {{ date > {year}.1.1 }}')
  remove=' '.join(f'v65_policy_{kind}_{n}' for kind in ['security','civilian'] for n in range(1,6))
  a=f'remove_ideas = {{ {remove} }} add_ideas = v65_policy_security_{phase} v65_upgrade_staff = yes v65_upgrade_training = yes subtract_from_variable = {{ v65_public_trust = 4 }} add_to_variable = {{ v65_patronage = 5 }} add_equipment_to_stockpile = {{ type = infantry_equipment_2 amount = 600 producer = ROOT }} v65_refresh_society = yes'
  b=f'remove_ideas = {{ {remove} }} add_ideas = v65_policy_civilian_{phase} v65_upgrade_logistics = yes v65_upgrade_signals = yes add_to_variable = {{ v65_public_trust = 8 }} subtract_from_variable = {{ v65_patronage = 4 }} subtract_from_variable = {{ v65_war_fatigue = 4 }} random_owned_controlled_state = {{ add_building_construction = {{ type = industrial_complex level = 1 instant_build = yes }} }} v65_refresh_society = yes'
  tree+=focus(sec,f'{year}：把战区放在首位',f'{title}之后，司令部要求优先补充军队。强化指挥、训练和战区政策，会提高部队表现，也扩大派系依赖并消耗民心。','helmet',0,y+2,a,'focus = '+ident,28,exclusive=f'mutually_exclusive = {{ focus = {civil} }}')
  tree+=focus(civil,f'{year}：与地方重新立约',f'{title}之后，地方社会要求恢复生产与可兑现的保护。增加民用产能、后勤和情报能力，降低疲劳；较慢的动员也意味着放弃部分进攻效率。','landmark',8,y+2,b,'focus = '+ident,28,exclusive=f'mutually_exclusive = {{ focus = {sec} }}')
  previous=[sec,civil];long_count+=3
 p.write_text(tree+'}\n',encoding='utf-8')

archive='v65_story_archive = {\n'
for phase,(year,title,_) in enumerate(ACTS,1):
 key=f'v65_archive_{year}';L[key]=f'重读{year}卷：{title}'
 archive+=f'{key} = {{ icon = generic_political_discourse cost = 0 available = {{ date > {year}.1.1 }} days_re_enable = 7 complete_effect = {{ country_event = {{ id = v65story.{800+phase} days = 1 }} }} ai_will_do = {{ factor = 0 }} }}\n'
put(Path('common/decisions/v65_archive.txt'),archive+'}')
put(Path('common/decisions/categories/v65_archive.txt'),'v65_story_archive = { icon = GFX_decision_generic_military allowed = { OR = { '+' '.join('tag = '+t for t in ALL)+' } } visible = { always = yes } }')
for lang in ['simp_chinese','english']:
 put(Path(f'localisation/{lang}/zzzzzz_v65_narrative_l_{lang}.yml'),loc_text(L,lang))
for lang,name in [('simp_chinese','高棉共和国'),('english','Khmer Republic')]:
 values={}
 for suffix in ['','_DEF','_ADJ']+[f'_{i}{s}' for i in ['neutrality','democratic','communism','fascism'] for s in ['','_DEF','_ADJ']]:values['V65_KHMER_REPUBLIC'+suffix]=name
 put(Path(f'localisation/replace/v65_cosmetic_names_l_{lang}.yml'),loc_text(values,lang))
# Add the narrative institutions to initialization without resetting loaded saves.
p=M/'common/on_actions/v65_society.txt';text=p.read_text(encoding='utf-8');text=text.replace('on_startup = { effect = {','on_startup = { effect = { SVN = { if = { limit = { NOT = { has_country_flag = v65_relationships_initialized } } set_country_flag = v65_relationships_initialized set_variable = { v65_park_trust = 50 } set_variable = { v65_thieu_trust = 50 } set_variable = { v65_island_trust = 50 } } }',1);p.write_text(text,encoding='utf-8')
total=sum(len(re.findall(r'\bfocus\s*=\s*\{',p.read_text(encoding='utf-8'))) for p in (M/'common/national_focus').glob('v65_*.txt'))
manifest={'version':'0.6.0','years':[1965,1968,1971,1974,1977,1979],'story_events':len(re.findall(r'^country_event = \{ id =',events,re.M)),'original_scene_chains':len(SCENES),'long_term_focuses':long_count,'total_focuses':total,'playable_at_start':PLAYABLE,'optional_regions':list(REGIONS),'intelligence':'narrative decisions; no agency requirement','adaptation':'Original dialogue and alternate routes informed by private novel notes; no novel text distributed'}
(R/'narrative-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Long campaign:',total,'focuses;',long_count,'dated focuses;',manifest['story_events'],'story/relay events;',len(SCENES),'delayed narrative chains')

p=R/'campaign-manifest.json';j=json.loads(p.read_text(encoding='utf-8'));j['expansion']=manifest;j['factions']['RKH']={'name':'红色高棉','capital':36};p.write_text(json.dumps(j,indent=2),encoding='utf-8')
