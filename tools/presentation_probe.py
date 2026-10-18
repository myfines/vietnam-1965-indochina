"""Native script assertions; UI rendering is explicitly not automated."""
from pathlib import Path
import re

def build(check,begin,end):
    state=(Path(__file__).resolve().parents[1]/'mod/history/states/18.txt').read_text(encoding='utf-8-sig')
    provinces=list(map(int,re.search(r'provinces = \{([^}]+)',state)[1].split()))
    cities={int(v) for v in re.findall(r'victory_points = \{\s*(\d+)',state)}
    pid=next((p for p in provinces if p not in cities and p not in {243,287,316}),provinces[0])
    s=f'on_actions = {{ on_startup = {{ effect = {{ log = "{begin}" }} }} on_daily = {{ effect = {{ '
    s+='if = { limit = { date > 1965.10.28 NOT = { has_global_flag = v65_presentation_probe } } set_global_flag = v65_presentation_probe '
    s+=check('18 = { check_variable = { v65_rear_level = 2 } has_dynamic_modifier = { modifier = v65_rear_pressure_2 } }','LOCAL_NETWORK_INITIALIZED')
    s+='PKS = { v65_free_korean_detachment = yes '
    s+=check('num_divisions > 4','KOREAN_REINFORCEMENT_REAL_UNIT')
    s+='v65_free_proxy = yes '
    s+=check('num_divisions > 5','PROXY_REAL_UNIT')
    s+='set_variable = { v65_contract_credit = 9 } v65_report_success = yes '
    s+=check('check_variable = { v65_contract_credit = 10 } has_country_flag = v65_last_claim_passed','CLAIM_PAYS_AND_CREDIT_CLAMPS')
    s+='v65_report_audit = yes '
    s+=check('has_country_flag = v65_audit_frozen NOT = { has_country_flag = v65_last_claim_passed }','AUDIT_FREEZES_CLAIMS')
    s+='set_variable = { v65_contract_credit = 4 } set_variable = { v65_personal_network = 6 } set_variable = { v65_ledger_claims = 2 } set_variable = { v65_park_influence = 6 } set_variable = { v65_korean_calls = 1 } } '
    s+='SVN = { complete_national_focus = v65_SVN_briefing v65_finalize_union = yes '
    s+=check('has_focus_tree = v65_park_government has_country_flag = v65_park_government_started','TAKEOVER_SWITCHES_PHASE')
    s+=check('check_variable = { v65_contract_credit = 4 } check_variable = { v65_personal_network = 6 } check_variable = { v65_korean_calls = 1 } check_variable = { v65_ledger_claims = 2 }','CONTRACT_NETWORK_SURVIVES_UNION')
    s+=check('has_country_flag = v65_audit_frozen','AUDIT_SURVIVES_UNION')
    s+=check('has_country_flag = v65_history_v65_SVN_briefing','PAST_FOCUS_HISTORY_RETAINED')
    s+='complete_national_focus = v65_pgov_root complete_national_focus = v65_pgov_command_roster complete_national_focus = v65_pgov_command_personal '
    s+=check('has_idea = v65_personal_staff','GOVERNING_FOCUS_HAS_PERSISTENT_EFFECT')
    s+='18 = { set_variable = { v65_rear_level = 3 } v65_refresh_rear_state = yes } '
    s+=check('18 = { has_dynamic_modifier = { modifier = v65_rear_pressure_3 } NOT = { has_dynamic_modifier = { modifier = v65_rear_pressure_2 } } }','LOCAL_NETWORK_REPLACES_OLD_TIER')
    s+='v65_rear_relief = yes '
    s+=check('18 = { check_variable = { v65_rear_level = 2 } has_dynamic_modifier = { modifier = v65_rear_pressure_2 } }','LOCAL_RELIEF_REDUCES_PRESSURE')
    s+='18 = { set_variable = { v65_rear_level = 3 } v65_refresh_rear_state = yes } } '
    s+=f'FNL = {{ v65_rear_rise_18 = yes '+check(f'controls_province = {pid} 18 = {{ check_variable = {{ v65_rear_level = 1 }} has_state_flag = v65_rear_cooldown }}','LOCAL_UPRISING_CREATES_REAR_FRONT')+' } } '
    s+=f'if = {{ limit = {{ date > 1965.11.05 }} log = "{end}" }} }} }} }}'
    return s
