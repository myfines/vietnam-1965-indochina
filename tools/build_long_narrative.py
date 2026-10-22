"""Five dated acts, delayed character scenes and the fourteen-year epilogue."""
from build_campaign import put,M,R,REWARDS
from long_foundation import ALL,PLAYABLE,REGIONS,loc_text
from narrative_scenes import SCENES
from chapter_scenes import SCENES as CHAPTER_SCENES
from pathlib import Path
import json,re

SCENES = SCENES + CHAPTER_SCENES
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
 callback_a='SVN = { add_to_variable = { v65_private_wealth = 2 } v65_refresh_personal_network = yes }' if ident>=5000 else 'add_to_variable = { v65_patronage = 2 } add_to_variable = { v65_war_fatigue = 1 }'
 callback_b='add_to_variable = { v65_contract_credit = 1 }' if ident>=5000 else 'add_to_variable = { v65_public_trust = 3 } subtract_from_variable = { v65_local_unrest = 1 }'
 events+=f'''country_event = {{ id = {root} title = {root}.t desc = {root}.d picture = GFX_report_event_generic_read_write is_triggered_only = yes
 option = {{ name = {root}.a ai_chance = {{ factor = 55 }} set_global_flag = v65_story_{ident}_a {ae} v65_refresh_society = yes {delayed()} }}
 option = {{ name = {root}.b ai_chance = {{ factor = {ai_b} }} set_global_flag = v65_story_{ident}_b {be} v65_refresh_society = yes {delayed()} }}
}}
country_event = {{ id = v65story.{relay} hidden = yes is_triggered_only = yes immediate = {{ {recipients(tags,sequel)} }} }}
country_event = {{ id = v65story.{sequel} immediate = {{ set_global_flag = v65_callback_{ident} }} title = v65story.{sequel}.t picture = GFX_report_event_generic_read_write is_triggered_only = yes
 desc = {{ trigger = {{ has_global_flag = v65_story_{ident}_a }} text = v65story.{sequel}.a }}
 desc = {{ trigger = {{ NOT = {{ has_global_flag = v65_story_{ident}_a }} }} text = v65story.{sequel}.b }}
 option = {{ name = v65story.{sequel}.next
  if = {{ limit = {{ has_global_flag = v65_story_{ident}_a }} {callback_a} }}
  else = {{ {callback_b} }} v65_refresh_society = yes
 }}
}}
'''
 available='OR = { '+' '.join(f'{t} = {{ exists = yes }}' for t in tags)+' }'
 schedule+=f'if = {{ limit = {{ date > {date} NOT = {{ has_global_flag = v65_scene_{ident}_sent }} {available} }} set_global_flag = v65_scene_{ident}_sent {recipients(tags,ident)} }}\n'

ACTS=[
 (1968,'撤军以后谁签字','美国人的撤军表送到了。有人先算缺了多少火力，有人先问空下来的仓库归谁。军费照领，运输照办；只是每张单子多了几个必须打招呼的名字。'),
 (1971,'一纸军令，几家生意','西贡要调兵，军区要欠饷，岛上要船。电话绕了一圈又回到原处。副官把几份条件抄到同一页：先说谁付钱，再谈谁听谁的。'),
 (1974,'撤退也得有个说法','地图上的箭头又往南挪了一截。船位、黄金、装备和军官家属都在排队；战报还没定稿，几位司令已经替自己的撤退选好了名字。'),
 (1977,'新番号，老熟人','县里的招牌换过几轮，收钱的人还是认得。新部队要编制，老军官要职位，商号说合同不能重签。司令部先把熟人的欠账列了出来。'),
 (1979,'十四年的老客户','新来的参谋想把旧账清掉，秘书搬来了十四年的合同。每一摞都有人签过字，每一个签字的人都说自己的那笔特殊。今天的电话比昨天还多。'),
]
for n,(year,title,body) in enumerate(ACTS,1):
 key=f'v65story.{800+n}';L.update({key+'.t':f'{year}：'+title,key+'.d':body+'\n\n案头的数字记录着此前的选择：民心、派系依赖、战争疲劳和军区关系都将带入这一幕。国策中的军事优先与社会契约互斥，新的阶段替换旧政策。',key+'.a':'继续写这一年的记录。'})
 events+=f'country_event = {{ id = {key} title = {key}.t desc = {key}.d picture = GFX_report_event_generic_read_write is_triggered_only = yes option = {{ name = {key}.a }} }}\n'
L.update({
 'v65_story_archive':'战时档案与人物关系',
 'v65_story_archive_desc':'朴与西贡的互信：[SVN.v65_park_trust|0]　首都政治关系：[SVN.v65_thieu_trust|0]　离岛信任：[SVN.v65_island_trust|0]\n每年的关键场景按日期出现。选择会留下全局剧情标记，并在45天后的信件或报告中回响。正式合并会保留西贡作为后续剧情的锚点。',
 'v65story.901.t':'第十四年的结算单',
 'v65story.901.d':'秘书把最后一年的账放上桌，又把前十三年的欠条压在底下。新来的参谋想按番号清账，刚查到第二页，就发现债主和领饷的人是同一批。\n\n“最后一卷叫什么？”\n“先别封卷，下个月的船还没到。”\n\n十四年叙事在这里结算。可以维持现有秩序，条件允许时推动停火，也可以继续战争；已有的人脉、民心与轮换缺额仍然有效。',
 'v65story.901.park':'总统的照片挂在门口，任命、合同和军区来电送到另一张桌子。朴不用为自己添一个头衔，秘书知道哪些文件要等他吃完饭再送。\n\n新参谋问这套手续是谁定的。老副官指了指柜里的合同：“先把这几笔续上，再问。”',
 'v65story.901.island':'船又到了。军官家属、机器零件和几箱没有写进货单的东西一起卸下，仓库里有人逐项签收。\n\n大陆上的番号换了几轮，岛上的商号还用原来的印章。今天先修船、发饷，至于明天挂哪面旗，等电话来了再说。',
 'v65story.901.a':'照旧开支，照旧签字。',
 'v65story.901.b':'把停火条件谈好，先恢复船期。',
 'v65story.901.c':'仗接着打，账也接着记。',
 'v65_memory_of_war':'十四年的关系户','v65_memory_of_war_desc':'熟人知道该找谁签字。旧合同和旧番号仍能让几家军区坐下来谈。',
 'v65_fragile_peace':'停火后的生意','v65_fragile_peace_desc':'船期可以重新排了，军队转向防御；各方继续商量欠饷、合同和驻地。',
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
