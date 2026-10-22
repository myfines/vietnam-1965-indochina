"""Chapter 254: a northern withdrawal and a southern delaying operation."""
from pathlib import Path
import json
from build_campaign import R,put
from long_foundation import loc_text

passages={p['id']:p for p in json.loads((R/'data/novel-source-passages.json').read_text(encoding='utf-8'))['passages']}
L={
 'v65_north_plans':'北方战局与南方牵制',
 'v65_north_reassess':'重议十七度线战局',
 'v65_north_reassess_desc':'北越与西贡交战、$V65_STATE_9$失守时开放；本局一次。选择整理正面防御或补充小道运输，随后由南方决定是否配合牵制。',
 'v65_south_delay':'提出南方牵制方案',
 'v65_south_delay_desc':'$V65_STATE_9$失守、解放阵线仍与西贡交战时，可独立提出牵制方案；与北方来函共用一次机会。',
 'v65north.1.t':'就这么收兵有点难看',
 'v65north.1.d':passages['ch254_nvn_withdrawal_debate']['quote'],
 'v65north.1.a':'先整理正面防御。',
 'v65north.1.b':'给南方牵制争取运输。',
 'v65north.2.t':'用游击队拖延南越的进军',
 'v65north.2.d':passages['ch254_nvn_rear_guerilla_delay']['quote'],
 'v65north.2.a':'让游击队黏住南越部队。',
 'v65north.2.b':'先整顿现有部队。',
}
put(Path('common/decisions/categories/v65_north_story.txt'),'''v65_north_plans = { icon = GFX_decision_category_generic_military allowed = { OR = { tag = NVN tag = FNL } } visible = { always = yes } }''')
put(Path('common/decisions/v65_north_story.txt'),'''v65_north_plans = {
 v65_north_reassess = { icon = generic_prepare_civil_war cost = 15
 visible = { tag = NVN NOT = { has_global_flag = v65_north_story_started } }
 available = { has_war_with = SVN NOT = { controls_state = 9 } }
 complete_effect = { country_event = { id = v65north.1 } } ai_will_do = { factor = 2 } }
 v65_south_delay = { icon = generic_prepare_civil_war cost = 15
 visible = { tag = FNL NOT = { has_global_flag = v65_south_delay_resolved } }
 available = { has_war_with = SVN NVN = { exists = yes has_war_with = SVN NOT = { controls_state = 9 } } }
 complete_effect = { country_event = { id = v65north.2 } } ai_will_do = { factor = 2 } }
}''')
put(Path('events/v65_north_story.txt'),'''add_namespace = v65north
country_event = { id = v65north.1 title = v65north.1.t desc = v65north.1.d
 picture = GFX_report_event_generic_read_write is_triggered_only = yes
 trigger = { tag = NVN NOT = { has_global_flag = v65_north_story_started } }
 immediate = { set_global_flag = v65_north_story_started }
 option = { name = v65north.1.a army_experience = 10 add_timed_idea = { idea = v65_prepared_defence days = 60 }
  if = { limit = { FNL = { exists = yes has_war_with = SVN } } FNL = { country_event = { id = v65north.2 days = 3 } } } }
 option = { name = v65north.1.b add_to_variable = { v65_trail_level = 1 } clamp_variable = { var = v65_trail_level min = 0 max = 6 } add_political_power = 15
  if = { limit = { FNL = { exists = yes has_war_with = SVN } } FNL = { country_event = { id = v65north.2 days = 3 } } } }
}
country_event = { id = v65north.2 title = v65north.2.t desc = v65north.2.d
 picture = GFX_report_event_generic_read_write is_triggered_only = yes
 trigger = { tag = FNL NOT = { has_global_flag = v65_south_delay_resolved } }
 immediate = { set_global_flag = v65_south_delay_resolved }
 option = { name = v65north.2.a add_to_variable = { v65_infiltration = 1 } clamp_variable = { var = v65_infiltration min = 0 max = 3 } }
 option = { name = v65north.2.b army_experience = 8 }
}''')
for lang in ['simp_chinese','english']:put(Path(f'localisation/{lang}/zzzzzzzz_v65_north_story_l_{lang}.yml'),loc_text(L,lang))
print('Northern and NLF chapter-254 story: two sourced events with separate player choices')
