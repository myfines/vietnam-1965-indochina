"""Exercise actual transfer, command recall, faction debt and withdrawal effects."""
def build(check,begin,end):
    s=f'on_actions = {{ on_startup = {{ effect = {{ log = "{begin}" }} }} on_daily = {{ effect = {{ '
    s+='if = { limit = { date > 1965.10.28 NOT = { has_global_flag = v65_revision_probe } } set_global_flag = v65_revision_probe '
    s+=check('10 = { is_owned_by = XTR has_state_flag = v65_supervised_dmz } XTR = { NOT = { has_war_with = NVN } NOT = { has_war_with = SVN } }','NEUTRAL_DMZ_SEPARATES_BELLIGERENTS')
    s+='SVN = { '+check('has_idea = v65_us_firepower num_divisions > 16 has_template = "US Intervention Group"','US_FIREPOWER_AND_EIGHT_REAL_UNITS')+' v65_devolve_HLC = yes } '
    s+='PKS = { set_country_flag = v65_island_plan_ready v65_move_park_31 = yes '
    s+=check('owns_state = 31 capital_scope = { state = 31 } has_country_flag = v65_move_cooldown','PARK_CAN_MOVE_TO_ALLIED_ISLAND')
    s+='SVN = { transfer_state = 15 } set_variable = { v65_park_influence = 6 } '
    s+=check('v65_can_offer_union = yes NOT = { owns_state = 15 }','UNION_NO_LONGER_REQUIRES_QUYNHON')
    s+='set_variable = { v65_paper_victories = 6 } set_variable = { v65_real_victories = 2 } set_variable = { v65_clique_daihai = 70 } v65_refresh_factions = yes '
    s+=check('check_variable = { v65_total_victories = 8 }','FAKE_AND_REAL_WAR_CREDIT_COMBINE')
    s+='} SVN = { v65_finalize_union = yes '
    s+=check('check_variable = { v65_clique_daihai = 70 } check_variable = { v65_paper_victories = 6 } check_variable = { v65_real_victories = 2 } has_country_flag = v65_island_plan_ready has_country_flag = v65_move_cooldown','PRIVATE_CLIQUES_SURVIVE_TAKEOVER')
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
    s+=check('10 = { is_owned_by = SVN } has_global_flag = v65_us_withdrawn SVN = { NOT = { has_idea = v65_us_firepower } NOT = { has_template = "US Intervention Group" } has_template = "Theater Infantry" }','WITHDRAWAL_REOPENS_DMZ_AND_ENDS_BUFF')
    s+='NVN = { set_province_controller = 305 } SVN = { v65_evacuate_island = yes } } '
    s+='if = { limit = { date > 1965.11.12 NOT = { has_global_flag = v65_island_probe } } set_global_flag = v65_island_probe '
    s+=check('PHQ = { exists = yes owns_state = 31 controls_province = 361 num_divisions > 1 }','ISLAND_SURVIVES_MAINLAND_CAPITAL_LOSS')
    s+='} '
    s+=f'if = {{ limit = {{ date > 1965.11.13 }} log = "{end}" }} }} }} }}'
    return s
