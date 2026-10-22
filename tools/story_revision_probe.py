"""Native in-game assertions for Park's private wealth and partner network."""


def build(check, begin, end):
    s = f'on_actions = {{ on_startup = {{ effect = {{ log = "{begin}" }} }} on_daily = {{ effect = {{ '
    s += 'if = { limit = { date > 1965.10.28 NOT = { has_global_flag = v65_personal_network_probe } } set_global_flag = v65_personal_network_probe '
    s += 'PKS = { '+check('has_country_leader = { character = v65_chae_myeong_sin }','CHAE_COMMANDS_THEATER_AT_START')
    s += 'v65_park_visit_DNM = yes '+check('SVN = { check_variable = { v65_park_host = 3 } owns_state = 11 } owns_state = 15 DNM = { owns_state = 12 }','PARK_VISITS_WITHOUT_ANNEXATION')
    s += 'v65_park_visit_SVN = yes '+check('SVN = { check_variable = { v65_park_host = 3 } }','TRAVEL_COOLDOWN_BLOCKS_DUPLICATE')
    s += 'clr_global_flag = v65_park_visit_cooldown v65_park_visit_PKS = yes '+check('SVN = { check_variable = { v65_park_host = 1 } }','PARK_CAN_RETURN_WITHOUT_MOVING_CAPITAL')
    s += 'clr_global_flag = v65_park_visit_cooldown } '

    # Give the permanent SVN ledger stable values before exercising production effects.
    s += 'SVN = { set_variable = { v65_private_wealth = 40 } set_variable = { v65_private_comfort = 20 } '
    for tag in ('SVN', 'DNM', 'HLC', 'MKG', 'BHD', 'PHQ', 'KHM'):
        s += f'set_variable = {{ v65_network_{tag} = 0 }} '
    s += 'v65_refresh_personal_network = yes '
    s += check('check_variable = { v65_private_wealth = 40 } check_variable = { v65_private_comfort = 20 }','PERSONAL_ANCHORS_INITIALIZED')
    for tag in ('SVN', 'DNM', 'HLC', 'MKG', 'BHD', 'PHQ', 'KHM'):
        s += check(f'check_variable = {{ v65_network_{tag} = 0 }}','NETWORK_'+tag+'_INITIALIZED')
    s += '} '

    # Open as Park, then resolve immediately in DNM scope while the pending global flag is live.
    s += 'PKS = { v65_open_contact_DNM = yes } DNM = { set_political_power = 10 v65_accept_contact_DNM = yes '
    s += check('SVN = { check_variable = { v65_network_DNM = 20 } } has_political_power > 29','DNM_ACCEPTANCE_PAYS_BOTH_SIDES')+' } '

    # Depot eligibility uses the new bilateral network threshold and permanent SVN wealth ledger.
    s += 'SVN = { set_variable = { v65_network_DNM = 25 } set_variable = { v65_private_wealth = 40 } } '
    s += 'DNM = { set_variable = { v65_local_unrest = 5 } } '
    s += 'PKS = { v65_network_depot_DNM = yes '
    s += check('SVN = { check_variable = { v65_private_wealth = 32 } check_variable = { v65_network_DNM = 28 } } has_idea = v65_network_supply DNM = { has_idea = v65_network_supply check_variable = { v65_local_unrest = 4 } }','DEPOT_COSTS_WEALTH_AND_REWARDS_BOTH_SIDES')+' } '

    # Verify threshold and existence filtering without creating a war: PHQ does not exist yet.
    s += 'FNL = { set_variable = { v65_private_wealth = 27 } } SVN = { set_variable = { v65_private_wealth = 10 } set_variable = { v65_network_DNM = 50 } set_variable = { v65_network_PHQ = 60 } v65_network_dividend = yes '
    s += check('check_variable = { v65_private_wealth = 11 } PHQ = { exists = no } FNL = { has_war_with = SVN check_variable = { v65_private_wealth = 27 } }','FRIENDLY_PARTNER_PAYS_ENEMY_DOES_NOT')+' } '

    # When no relationships qualify, the existing SVN-FNL war remains untouched and the ledger pays nothing.
    s += 'SVN = { set_variable = { v65_private_wealth = 10 } set_variable = { v65_network_DNM = 0 } set_variable = { v65_network_HLC = 0 } set_variable = { v65_network_MKG = 0 } set_variable = { v65_network_BHD = 0 } set_variable = { v65_network_PHQ = 0 } set_variable = { v65_network_KHM = 0 } v65_network_dividend = yes '
    s += check('check_variable = { v65_private_wealth = 10 } has_war_with = FNL','NO_QUALIFYING_CONTACT_NO_DIVIDEND')+' } '

    # Holiday is rooted in the Park actor, while wealth and comfort stay anchored to SVN.
    s += 'PKS = { set_political_power = 200 v65_private_holiday = yes '
    s += check('has_political_power > 200 has_idea = v65_private_staff SVN = { check_variable = { v65_private_wealth = 0 } check_variable = { v65_private_comfort = 35 } }','HOLIDAY_SPENDS_TEN_AND_GRANTS_COMFORT_PP_AND_STAFF')+' } '

    # Release the island region and invoke its native uprising callback; no war is started by the probe.
    s += 'SVN = { v65_devolve_PHQ = yes '
    s += check('PHQ = { exists = yes owns_state = 31 controls_province = 361 }','PHQ_RELEASE_RETAINS_ISLAND_CONTROL')+' } '
    s += 'PKS = { complete_national_focus = v65chapter_pks_root complete_national_focus = v65chapter_pks_reports_first_report complete_national_focus = v65chapter_pks_reports_casualty_ledger country_event = { id = v65story.5101 days = 1 } '
    s += check('has_completed_focus = v65chapter_pks_reports_casualty_ledger has_global_flag = v65chapter_focus_reports_casualty_ledger_claimed','CHAPTER_FOCUS_LAUNCHES_EVENT_AND_CLAIM_GUARD')+' } '

    s += '} if = { limit = { date > 1965.11.03 NOT = { has_global_flag = v65_story_probe_phase2 } } set_global_flag = v65_story_probe_phase2 '
    s += 'PHQ = { '+check('has_war_with = FNL','ISLAND_TEST_EXERCISES_REAL_SHARED_WAR')+' v65_regional_outbreak = yes '
    s += check('owns_state = 31 controls_province = 361 FNL = { NOT = { controls_province = 361 } }','PHQ_OUTBREAK_CANNOT_GIVE_FNL_THE_ISLAND')+' } '
    s += check('has_global_flag = v65chapter_event_100_resolved OR = { AND = { has_global_flag = v65chapter_event_100_choice_a NOT = { has_global_flag = v65chapter_event_100_choice_b } } AND = { has_global_flag = v65chapter_event_100_choice_b NOT = { has_global_flag = v65chapter_event_100_choice_a } } }','CHAPTER_EVENT_RESOLVES_EXACTLY_ONE_CHOICE')
    s += check('OR = { has_global_flag = v65_story_5101_a has_global_flag = v65_story_5101_b }','CHAPTER_SCENE_HAS_NATIVE_CHOICE')
    s += 'PKS = { complete_national_focus = v65chapter_pks_reports_media_contract '+check('has_completed_focus = v65chapter_pks_reports_media_contract','CHAPTER_FORK_REJOINS_IN_NATIVE_FOCUS_TREE')+' } '

    # Follow the existing takeover probe path and assert the permanent variables survive annexation.
    s += 'SVN = { set_variable = { v65_private_wealth = 37 } set_variable = { v65_private_comfort = 42 } } '
    s += 'PKS = { clr_global_flag = v65_park_visit_cooldown v65_park_visit_SVN = yes '
    s += check('has_global_flag = v65_park_visit_cooldown SVN = { check_variable = { v65_park_visit_days = 30 } }','PRE_UNION_TRAVEL_TIMER_IS_ARMED')
    s += 'set_variable = { v65_park_influence = 6 } v65_finalize_union = yes } '
    s += 'SVN = { '+check('has_country_flag = v65_union_complete check_variable = { v65_private_wealth = 37 } check_variable = { v65_private_comfort = 42 }','UNION_PRESERVES_SVN_PRIVATE_ANCHORS')+' } '

    s += '} '
    s += 'if = { limit = { date > 1965.11.10 NOT = { has_global_flag = v65_story_probe_mirror } } set_global_flag = v65_story_probe_mirror SVN = { '
    s += check('has_focus_tree = v65_park_government has_completed_focus = v65chapter_svn_reports_first_report has_completed_focus = v65chapter_svn_reports_casualty_ledger','TAKEOVER_BYPASSES_ALREADY_CLAIMED_STORY_FOCUSES')+' } } '
    s += 'if = { limit = { date > 1965.12.16 NOT = { has_global_flag = v65_story_probe_callback } } set_global_flag = v65_story_probe_callback '
    s += check('has_global_flag = v65_callback_5101','CHAPTER_SCENE_REACHES_FORTY_FIVE_DAY_CALLBACK')
    s += check('NOT = { has_global_flag = v65_park_visit_cooldown }','TRAVEL_COOLDOWN_EXPIRES_AFTER_PKS_ANNEXATION')
    s += check('SVN = { check_variable = { v65_park_visit_days < 1 } }','TRAVEL_COUNTDOWN_REACHES_ZERO')+' } '
    s += f'if = {{ limit = {{ date > 1965.12.17 }} log = "{end}" }} }} }} }}'
    return s


