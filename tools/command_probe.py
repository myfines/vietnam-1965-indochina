"""Native-engine scenario for the military command extension."""
def build(check, begin, end):
    script = f'on_actions = {{ on_startup = {{ effect = {{ log = "{begin}" }} }} on_daily = {{ effect = {{ '
    script += 'if = { limit = { date > 1965.10.28 NOT = { has_global_flag = v65_command_probe1 } } set_global_flag = v65_command_probe1 SVN = { '
    script += check('check_variable = { v65_central_prestige = 55 }', 'CENTRAL_INITIALIZED')
    script += 'v65_devolve_HLC = yes } '
    script += check('HLC = { exists = yes v65_under_central_command = yes owns_state = 16 } MKG = { exists = no } BHD = { exists = no } PHQ = { exists = no }', 'ONE_DISTRICT_ONLY')
    script += 'PKS = { set_variable = { v65_personal_network = 6 } set_variable = { v65_park_influence = 6 } v65_park_build_retinue = yes '
    script += check('num_divisions > 4', 'PARK_PERSONAL_FORCE') + '} } '
    script += 'if = { limit = { date > 1965.11.02 NOT = { has_global_flag = v65_command_probe2 } } set_global_flag = v65_command_probe2 SVN = { set_variable = { v65_central_prestige = 20 } v65_refresh_command = yes '
    script += check('has_idea = v65_central_discredited', 'LOW_PRESTIGE_SPIRIT') + '} '
    script += 'HLC = { set_variable = { v65_regional_loyalty = 50 } v65_dissent_HLC = yes '
    script += check('NOT = { has_country_flag = v65_command_refused }', 'LOYAL_DISTRICT_OBEYS')
    script += 'set_variable = { v65_regional_loyalty = 20 } v65_dissent_HLC = yes '
    script += check('has_country_flag = v65_command_refused', 'DISLOYAL_DISTRICT_REFUSES')
    script += 'v65_rebel_HLC = yes '
    script += check('has_country_flag = v65_rebel_command NOT = { is_subject_of = SVN }', 'DISTRICT_BREAKS_FROM_CENTRAL') + '} '
    script += 'SVN = { set_variable = { v65_central_prestige = 65 } v65_refresh_command = yes '
    script += check('has_idea = v65_central_respected NOT = { has_idea = v65_central_discredited }', 'PRESTIGE_RECOVERS')
    script += '} } '
    script += 'if = { limit = { date > 1965.11.13 NOT = { has_global_flag = v65_command_probe3 } } set_global_flag = v65_command_probe3 HLC = { '
    script += check('has_war_with = SVN', 'DISTRICT_REBELLION_REAL_WAR') + '} } '
    script += 'if = { limit = { date > 1965.11.14 NOT = { has_global_flag = v65_command_probe_wars } } set_global_flag = v65_command_probe_wars SVN = { '
    script += check('has_war_with = NVN has_war_with = FNL', 'CENTRAL_EXTERNAL_WARS_PRESERVED') + '} } '
    script += 'if = { limit = { date > 1965.11.16 NOT = { has_global_flag = v65_command_probe4 } } set_global_flag = v65_command_probe4 SVN = { v65_finalize_union = yes '
    script += check('has_country_flag = v65_union_complete PKS = { exists = no } has_idea = v65_park_shadow_ruler', 'PARK_CONTROLS_SOUTH') + '} } '
    script += f'if = {{ limit = {{ date > 1965.11.17 }} log = "{end}" }} }} }} }}'
    return script
