"""Exercise production consent and peace effects in a real internal war."""
def build(check,begin,end):
    s=f'on_actions = {{ on_startup = {{ effect = {{ log = "{begin}" }} }} on_daily = {{ effect = {{ '
    s+='if = { limit = { date > 1965.10.28 NOT = { has_global_flag = v65_guest_probe_setup } } set_global_flag = v65_guest_probe_setup SVN = { v65_devolve_MKG = yes v65_devolve_PHQ = yes } NVN = { country_event = { id = v65north.1 } } } '
    s+='if = { limit = { date > 1965.11.01 NOT = { has_global_flag = v65_guest_probe_war } } set_global_flag = v65_guest_probe_war SVN = { set_variable = { v65_central_prestige = 20 } } MKG = { set_variable = { v65_regional_loyalty = 20 } v65_dissent_MKG = yes v65_rebel_MKG = yes } } '
    s+='if = { limit = { date > 1965.11.11 NOT = { has_global_flag = v65_guest_probe_external } } set_global_flag = v65_guest_probe_external MKG = { declare_war_on = { target = FNL type = annex_everything } } } '
    s+='if = { limit = { date > 1965.11.12 NOT = { has_global_flag = v65_guest_probe_checked } } set_global_flag = v65_guest_probe_checked '
    s+=check('MKG = { has_war_with = SVN has_war_with = FNL } PHQ = { controls_province = 361 }','MEDIATION_REAL_INTERNAL_AND_EXTERNAL_WARS')
    s+='MKG = { v65_guest_finish = yes '+check('has_war_with = SVN NOT = { has_country_flag = v65_guest_mediated }','NO_PEACE_WITHOUT_PROPOSAL')+' } '
    s+='set_global_flag = v65_guest_talks_open set_global_flag = v65_guest_target_MKG set_global_flag = v65_guest_region_agreed '
    s+='MKG = { v65_guest_finish = yes '+check('has_war_with = SVN','NO_PEACE_WITHOUT_HOST_AND_CENTRAL_CONSENT')+' } '
    s+='set_global_flag = v65_guest_island_agreed set_global_flag = v65_guest_central_agreed '
    s+='DNM = { v65_guest_finish = yes '+check('NOT = { has_country_flag = v65_guest_mediated } MKG = { has_war_with = SVN }','OTHER_COMMAND_CANNOT_SIGN_SELECTED_ARMISTICE')+' } '
    s+='MKG = { v65_guest_finish = yes '+check('NOT = { has_war_with = SVN } has_war_with = FNL has_country_flag = v65_guest_mediated','CONSENT_ENDS_ONLY_INTERNAL_WAR')+' } '
    s+=check('NOT = { has_global_flag = v65_guest_talks_open } NOT = { has_global_flag = v65_guest_region_agreed } NOT = { has_global_flag = v65_guest_target_MKG }','ARMISTICE_CLEARS_TRANSIENT_STATE')
    s+='set_global_flag = v65_guest_cooldown SVN = { country_event = { id = v65guest.99 days = 1 } } } '
    s+='if = { limit = { date > 1965.11.15 NOT = { has_global_flag = v65_guest_probe_expired } } set_global_flag = v65_guest_probe_expired '
    s+=check('NOT = { has_global_flag = v65_guest_cooldown }','MEDIATION_EXPIRY_UNLOCKS_NEXT_PROPOSAL')
    s+=check('has_global_flag = v65_north_story_started has_global_flag = v65_south_delay_resolved','NORTH_AND_NLF_SOURCE_EVENTS_REACH_SEPARATE_CHOICES')+' } '
    s+=f'if = {{ limit = {{ date > 1965.11.16 }} log = "{end}" }} }} }} }}'
    return s
