"""Exercise actual transfer, command recall, faction debt and withdrawal effects."""
def build(check,begin,end):
    s=f'on_actions = {{ on_startup = {{ effect = {{ log = "{begin}" }} }} on_daily = {{ effect = {{ '
    s+='if = { limit = { date > 1965.10.28 NOT = { has_global_flag = v65_revision_probe } } set_global_flag = v65_revision_probe '
    s+=check('10 = { is_owned_by = SVN NOT = { has_state_flag = v65_supervised_dmz } }','NO_NEUTRAL_DMZ_AT_17TH_PARALLEL')
    s+='SVN = { '+check('has_idea = v65_us_firepower num_divisions > 16 has_template = "US Intervention Group"','US_FIREPOWER_AND_EIGHT_REAL_UNITS')+' v65_devolve_HLC = yes } '
    s+='SVN = { set_variable = { v65_us_withdraw_pressure = 30 } v65_refresh_us_support = yes '+check('has_idea = v65_us_firepower_75 NOT = { has_idea = v65_us_firepower }','WITHDRAWAL_30_SELECTS_75_PERCENT_TIER')
    s+='set_variable = { v65_us_withdraw_pressure = 60 } v65_refresh_us_support = yes '+check('has_idea = v65_us_firepower_50 NOT = { has_idea = v65_us_firepower_75 }','WITHDRAWAL_60_SELECTS_50_PERCENT_TIER')
    s+='set_variable = { v65_us_withdraw_pressure = 85 } v65_refresh_us_support = yes '+check('has_idea = v65_us_firepower_25 NOT = { has_idea = v65_us_firepower_50 }','WITHDRAWAL_85_SELECTS_25_PERCENT_TIER')
    s+='set_variable = { v65_us_withdraw_pressure = 0 } v65_refresh_us_support = yes v65_send_roc_detachment = yes '+check('has_idea = v65_roc_mission has_template = "ROC Vietnam Detachment" check_variable = { v65_roc_calls = 1 } PKS = { has_idea = v65_rok_liaison }','TAEGUK_AND_ROC_MISSIONS_WITH_REAL_REINFORCEMENT')+' } '
    s+='PKS = { set_country_flag = v65_island_plan_ready v65_move_park_31 = yes '
    s+=check('owns_state = 31 capital_scope = { state = 31 } has_country_flag = v65_move_cooldown','PARK_CAN_MOVE_TO_ALLIED_ISLAND')
    s+='SVN = { transfer_state = 15 } set_variable = { v65_park_influence = 6 } '
    s+=check('v65_can_offer_union = yes NOT = { owns_state = 15 }','UNION_NO_LONGER_REQUIRES_QUYNHON')
    s+='set_variable = { v65_paper_victories = 6 } set_variable = { v65_real_victories = 2 } set_variable = { v65_clique_daihai = 70 } v65_refresh_factions = yes '
    s+=check('check_variable = { v65_total_victories = 8 }','FAKE_AND_REAL_WAR_CREDIT_COMBINE')
    s+='} SVN = { v65_finalize_union = yes '
    s+=check('check_variable = { v65_clique_daihai = 70 } check_variable = { v65_paper_victories = 6 } check_variable = { v65_real_victories = 2 } has_country_flag = v65_island_plan_ready has_country_flag = v65_move_cooldown has_idea = v65_rok_liaison','PRIVATE_CLIQUES_SURVIVE_TAKEOVER')
    s+='set_variable = { v65_clique_request = 1 } set_variable = { v65_request_age = 2 } v65_factions_month = yes '
    s+=check('has_idea = v65_clique_contract_block','UNPAID_DAIHAI_BLOCKS_CONTRACTS')
    s+='v65_settle_clique = yes '+check('NOT = { has_idea = v65_clique_contract_block } check_variable = { v65_clique_request = 0 }','SETTLEMENT_REOPENS_CHANNEL')
    s+='set_variable = { v65_clique_request = 2 } set_variable = { v65_request_age = 2 } v65_factions_month = yes '
    s+=check('has_idea = v65_clique_staff_block','STAFF_CAN_BLOCK_COMMAND')
    s+='v65_settle_clique = yes set_variable = { v65_clique_request = 3 } set_variable = { v65_request_age = 2 } v65_factions_month = yes '
    s+=check('has_idea = v65_clique_proxy_block','PROXIES_CAN_WITHHOLD_PERSONNEL')
    s+='v65_settle_clique = yes } } '
    s+='if = { limit = { date > 1965.11.04 NOT = { has_global_flag = v65_recall_probe } } set_global_flag = v65_recall_probe SVN = { v65_recall_HLC_14 = yes '
    s+=check('owns_state = 14 HLC = { exists = yes owns_state = 16 }','PARTIAL_RECALL_KEEPS_DISTRICT_ALIVE')
    s+='v65_dissolve_HLC = yes '+check('owns_state = 16 HLC = { exists = no } has_character = v65_nguyen_khanh','FORCED_DISSOLUTION_RECALLS_LAND_AND_COMMANDER')
    s+='} SVN = { v65_withdraw_intervention = yes } '
    s+=check('has_global_flag = v65_us_withdrawn SVN = { NOT = { has_idea = v65_us_firepower } NOT = { has_template = "US Intervention Group" } has_template = "Theater Infantry" has_template = "ROC Vietnam Detachment" has_idea = v65_roc_mission }','US_WITHDRAWAL_PRESERVES_ROC_AND_REGULAR_UNITS')
    s+='NVN = { set_province_controller = 305 } SVN = { v65_evacuate_island = yes } } '
    s+='if = { limit = { date > 1965.11.12 NOT = { has_global_flag = v65_island_probe } } set_global_flag = v65_island_probe '
    s+=check('PHQ = { exists = yes owns_state = 31 controls_province = 361 num_divisions > 1 }','ISLAND_SURVIVES_MAINLAND_CAPITAL_LOSS')
    s+='} '
    s+=f'if = {{ limit = {{ date > 1965.11.13 }} log = "{end}" }} }} }} }}'
    return s
