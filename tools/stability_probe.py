"""Unforced early-war balance: leave wars, ownership and decisions to the AI."""
def build(check,begin,end):
    s=f'on_actions = {{ on_startup = {{ effect = {{ log = "{begin}" }} }} on_daily = {{ effect = {{ '
    s+='if = { limit = { date > 1966.1.28 NOT = { has_global_flag = v65_stability_probe } } set_global_flag = v65_stability_probe '
    s+=check('SVN = { exists = yes owns_state = 25 controls_province = 305 }','NATURAL_SAIGON_HELD_AFTER_THREE_MONTHS')
    s+=check('PKS = { exists = yes controls_state = 15 }','NATURAL_PARK_NOT_OVERRUN')
    s+=check('10 = { is_owned_by = XTR is_fully_controlled_by = XTR }','NATURAL_DMZ_REMAINS_NEUTRAL')
    s+=check('31 = { OR = { is_controlled_by = SVN is_controlled_by = PHQ is_controlled_by = PKS } }','NATURAL_ISLAND_NOT_LOST_WITH_MAINLAND')
    s+=f'log = "{end}" }} }} }} }}'
    return s
