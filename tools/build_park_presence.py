"""A travelling officer is distinct from a territorial government's leader."""
from pathlib import Path
import json
from build_campaign import M,R,put
from long_foundation import loc_text

HOSTS={'PKS':'韩军本部','SVN':'西贡','DNM':'岘港','HLC':'西原','MKG':'湄公河','BHD':'东南军区','PHQ':'富国岛','KHM':'金边'}
effects='';decisions='v65_personal_connections = {\n';defined='defined_text = { name = v65_park_where\n'
L={'v65_park_where_unknown':'行程未通报','v65_park_itinerary':'朴的行程：[v65_park_where]',
   'v65_park_visit_ready':'由朴的私人网络安排出访',
   'v65_park_return':'返回韩军本部',
   'v65_park_visit_desc':'出访只改变人物行程，不移交领土、首都或部队。目标须保持和平并控制驻地。30天后可安排下一站；原有军区指挥关系继续有效。'}
for number,(tag,name) in enumerate(HOSTS.items(),1):
    guard=f'v65_personal_network_actor = yes {tag} = {{ exists = yes capital_scope = {{ is_fully_controlled_by = {tag} }} }} NOT = {{ has_global_flag = v65_park_visit_cooldown }}'
    if tag!='PKS':guard+=f' NOT = {{ has_war_with = {tag} }}'
    key='v65_park_visit_'+tag
    effects+=f'''{key} = {{ if = {{ limit = {{ {guard} }}
 SVN = {{ set_variable = {{ v65_park_host = {number} }} set_variable = {{ v65_park_visit_days = 30 }} }}
 set_global_flag = v65_park_visit_cooldown
 }} }}\n'''
    L[key]='前往'+name;L[key+'_desc']='$v65_park_visit_desc$'
    L['v65_park_at_'+tag]=name
    decisions+=f'''{key} = {{ icon = generic_political_discourse cost = 15
 visible = {{ v65_personal_network_actor = yes {tag} = {{ exists = yes }} }}
 available = {{ {guard} NOT = {{ SVN = {{ check_variable = {{ v65_park_host = {number} }} }} }} }}
 complete_effect = {{ {key} = yes }} ai_will_do = {{ factor = 0 }} }}\n'''
    defined+=f'text = {{ trigger = {{ SVN = {{ check_variable = {{ v65_park_host = {number} }} }} }} localization_key = v65_park_at_{tag} }}\n'
defined+='text = { localization_key = v65_park_where_unknown } }'
put(Path('common/scripted_effects/v65_presence.txt'),effects)
put(Path('common/decisions/v65_presence.txt'),decisions+'}')
put(Path('common/scripted_localisation/v65_presence.txt'),defined)
put(Path('events/v65_presence.txt'),'''add_namespace = v65presence
country_event = { id = v65presence.1 hidden = yes is_triggered_only = yes
 immediate = { clr_global_flag = v65_park_visit_cooldown } }
''')
put(Path('common/on_actions/v65_presence.txt'),'''on_actions = {
 on_startup = { effect = { SVN = { if = { limit = { NOT = { has_country_flag = v65_presence_initialized } }
 set_country_flag = v65_presence_initialized set_variable = { v65_park_host = 1 } } } } }
 on_daily = { effect = {
 if = { limit = { has_global_flag = v65_park_visit_cooldown }
  SVN = { subtract_from_variable = { v65_park_visit_days = 1 } }
  if = { limit = { SVN = { check_variable = { v65_park_visit_days < 1 } } } clr_global_flag = v65_park_visit_cooldown }
 }
 SVN = { if = { limit = { has_country_flag = v65_union_complete check_variable = { v65_park_host = 1 } }
 set_variable = { v65_park_host = 2 } } } } }
}''')
for lang in ['simp_chinese','english']:put(Path(f'localisation/{lang}/zzzzzzzz_v65_presence_l_{lang}.yml'),loc_text(L,lang))
(R/'park-presence-manifest.json').write_text(json.dumps(dict(hosts=HOSTS,territory_transfer=False,starting_commander='Chae Myeong-sin',park_role='corps_commander'),ensure_ascii=False,indent=2),encoding='utf-8')
print('Park itinerary: eight destinations, no territorial transfer')
