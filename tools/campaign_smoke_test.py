"""Real-engine campaign assertions, without desktop automation."""
from pathlib import Path
import subprocess,time,re,json,hashlib,datetime,os
R=Path(__file__).resolve().parents[1];O=R/'runtime/theater-mod'
G=Path(json.loads((R/'runtime/install-report.json').read_text())['game'])
U=Path.home()/'Documents/Paradox Interactive/Hearts of Iron IV'
OUT=R/'runtime/test-results';OUT.mkdir(exist_ok=True)
if 'hoi4.exe' in subprocess.check_output(['tasklist','/FI','IMAGENAME eq hoi4.exe'],text=True).lower():raise RuntimeError('Close HOI4 before testing')
expected=[]
def check(condition,name):
 expected.append('V65_PASS_'+name)
 return f'if = {{ limit = {{ {condition} }} log = "V65_PASS_{name}" }} else = {{ log = "V65_FAIL_{name}" }}'
nonce=str(time.time_ns());begin='V65_SMOKE_BEGIN_'+nonce;end='V65_SMOKE_END_'+nonce
script=f'on_actions = {{ on_startup = {{ effect = {{ log = "{begin}" '
for tag in ['SVN','NVN','KHM','PKS','FNL','DNM']:
 script+=f'{tag} = {{ '+check('num_divisions > 0',tag+'_UNITS')+' '+check(f'has_focus_tree = v65_{tag}_tree',tag+'_TREE')+' } '
script+='SVN = { '+check('has_war_with = NVN has_war_with = FNL','TWO_FRONT_WAR')+' '+check('NOT = { has_country_flag = v65_front_defeat } NOT = { has_country_flag = v65_crisis_active }','NO_INITIAL_COUP')+' } '
script+='FNL = { '+check('controls_province = 243 controls_province = 287 controls_province = 316','THREE_REAR_CELLS')+' } '
for tag,char in [('PKS','park_seicheng'),('NVN','ho_chi_minh'),('SVN','nguyen_van_thieu'),('DNM','ngo_quang_truong'),('FNL','nguyen_huu_tho'),('KHM','norodom_sihanouk')]:
 script+=f'{tag} = {{ '+check('has_character = v65_'+char,tag+'_CHARACTER')+' } '
script+='} } on_daily = { effect = { '
script+='if = { limit = { date > 1965.10.28 NOT = { has_global_flag = v65_probe_phase1 } } set_global_flag = v65_probe_phase1 '
script+='SVN = { v65_resolve_coup = yes '+check('NOT = { has_country_flag = v65_coup_resolved }','COUP_BLOCKED_BEFORE_DEFEAT')+' } '
script+='NVN = { set_state_controller = 10 } SVN = { v65_check_front_defeat = yes '
script+=check('has_country_flag = v65_front_defeat has_country_flag = v65_crisis_active','DEFEAT_OPENS_CRISIS')
script+='v65_enact_martial_law = yes '+check('10 = { NOT = { has_state_flag = v65_under_martial_law } } 25 = { has_state_flag = v65_under_martial_law }','DMZ_EXCEPTION')
script+='v65_resolve_coup = yes '+check('NOT = { has_country_flag = v65_civil_war_started } NOT = { has_country_flag = v65_coup_victory }','COUP_FAILURE')
for state in [23,24,26]:script+=f'{state} = {{ set_variable = {{ v65_loyalty = 80 }} }} '
script+='v65_resolve_coup = yes '+check('has_country_flag = v65_coup_victory has_country_leader = { character = v65_duong_van_minh }','COUP_PEACE_CHANGES_LEADER')+' } '
script+='NVN = { set_variable = { v65_trail_level = 2 } } FNL = { set_variable = { v65_infiltration = 1 } v65_launch_infiltration = yes '
script+=check('has_country_flag = v65_raid_fired has_country_flag = v65_raid_cooldown check_variable = { v65_infiltration = 0 } NVN = { check_variable = { v65_trail_level = 1 } }','TRAIL_CREATES_REAR_FORCE')+' } } '
script+='if = { limit = { date > 1965.11.01 NOT = { has_global_flag = v65_probe_phase2 } } set_global_flag = v65_probe_phase2 '
script+='PKS = { v65_park_intervention = yes '+check('has_country_flag = v65_park_march has_war_with = SVN NOT = { is_in_faction_with = SVN }','PLAYABLE_PARK_INTERVENTION')+' } '
script+='SVN = { 23 = { set_variable = { v65_loyalty = 80 } } 24 = { set_variable = { v65_loyalty = 0 } } 26 = { set_variable = { v65_loyalty = 0 } } 27 = { set_variable = { v65_loyalty = 0 } } v65_resolve_coup = yes '
script+=check('has_country_flag = v65_civil_war_started','COUP_CIVIL_WAR')+' } } '
script+=f'if = {{ limit = {{ date > 1965.11.05 }} log = "{end}" }} }} }} }}'
balance=os.environ.get('V65_BALANCE_TEST')=='1'
if balance:
 expected=expected[:21]
 script=script[:script.index('on_daily =')]+'''on_daily = { effect = {
 if = { limit = { date > 1965.11.27 NOT = { has_global_flag = v65_balance_checked } } set_global_flag = v65_balance_checked
 '''
 script+=check('NVN = { controls_state = 9 } SVN = { controls_state = 10 }','NORTH_FRONT_STILL_HOLDS')
 script+=check('FNL = { exists = yes num_divisions > 0 has_country_flag = v65_raid_fired }','GUERRILLAS_SURVIVE_AND_RAID')
 script+=check('PKS = { exists = yes } DNM = { exists = yes } SVN = { exists = yes }','SOUTHERN_FACTIONS_SURVIVE')
 script+=f' }} if = {{ limit = {{ date > 1965.11.28 }} log = "{end}" }} }} }} }}'
routes=os.environ.get('V65_ROUTES_TEST')=='1'
if routes:
 expected=expected[:21]
 script=script[:script.index('on_daily =')]+'''on_daily = { effect = {
 if = { limit = { date > 1965.10.28 NOT = { has_global_flag = v65_routes_checked } } set_global_flag = v65_routes_checked
 NVN = { set_variable = { v65_trail_level = 1 } } FNL = { set_variable = { v65_infiltration = 0 } }
 KHM = { v65_open_sanctuary = yes v65_sanctuary_pulse = yes
 '''
 script+=check('has_country_flag = v65_sanctuary_open has_idea = v65_neutral_sanctuary has_war_with = RKH NOT = { has_war_with = SVN } NOT = { is_in_faction_with = NVN }','NEUTRAL_CAMBODIAN_REAR')
 script+=check('NVN = { check_variable = { v65_trail_level = 2 } } FNL = { check_variable = { v65_infiltration = 1 } }','SANCTUARY_STRENGTHENS_REAR_WAR')
 script+='v65_close_sanctuary = yes v65_sanctuary_pulse = yes '
 script+=check('NOT = { has_country_flag = v65_sanctuary_open } NOT = { has_idea = v65_neutral_sanctuary } NVN = { check_variable = { v65_trail_level = 2 } }','CLOSURE_STOPS_LOGISTICS')
 script+='v65_open_sanctuary = yes } SVN = { v65_apply_border_pressure = yes } KHM = { '
 script+=check('check_variable = { v65_border_tension = 2 } NOT = { has_war_with = SVN }','DIPLOMATIC_PRESSURE_WITHOUT_WAR')+' } '
 script+='PKS = { if = { limit = { is_ai = no } log = "V65_PLAYER_TRANSFER_BRANCH" } set_variable = { v65_park_influence = 5 } '
 script+=check('v65_can_offer_union = yes','NEGOTIATED_UNION_AVAILABLE')
 script+='v65_finalize_union = yes } SVN = { '
 script+=check('exists = yes owns_state = 15 owns_state = 25 has_idea = v65_park_shadow_ruler has_country_flag = v65_union_complete','UNION_TERRITORY_AND_SHADOW_RULER')
 script+=check('has_character = v65_park_seicheng has_character = v65_kim_jong_pil has_country_leader = { character = v65_nguyen_van_thieu }','PARK_RETAINS_INFLUENCE_WITH_CIVILIAN_PRESIDENT')
 script+=check('num_divisions > 15 has_war_with = NVN has_war_with = FNL','UNION_ARMY_AND_WAR_CONTINUE')+' } '
 script+=check('PKS = { exists = no }','UNION_REPLACES_EXPEDITION_TAG')
 script+=f' }} if = {{ limit = {{ date > 1965.11.03 }} log = "{end}" }} }} }} }}'
stages=os.environ.get('V65_STAGES_TEST')=='1'
if stages:
 expected=expected[:21]
 script=script[:script.index('on_daily =')]+'''on_daily = { effect = {
 if = { limit = { date > 1965.10.28 NOT = { has_global_flag = v65_stages_checked } } set_global_flag = v65_stages_checked
 SVN = { v65_check_war_stages = yes
 '''
 script+=check('has_country_flag = v65_highlands_lost has_country_flag = v65_front_defeat has_idea = v65_highland_disruption','HIGHLAND_DEFEAT_OPENS_POLITICAL_CRISIS')
 script+=check('has_country_flag = v65_saigon_lost has_idea = v65_southern_holdouts capital_scope = { state = 28 }','SAIGON_FALL_RELOCATES_TO_MEKONG')
 script+=f' }} }} if = {{ limit = {{ date > 1965.11.03 }} log = "{end}" }} }} }} }}'
long_run=os.environ.get('V65_LONG_TEST')=='1'
if long_run:
 expected=expected[:21]
 script=script[:script.index('on_daily =')]+'''on_daily = { effect = {
 if = { limit = { date > 1965.10.30 NOT = { has_global_flag = v65_long_checked } } set_global_flag = v65_long_checked
 '''
 script+='RKH = { '+check('exists = yes num_divisions > 5 has_focus_tree = v65_RKH_tree has_character = v65_pol_pot owns_state = 36','KHMER_ROUGE_REAL_STATE')+' } '
 script+='KHM = { v65_open_sanctuary = yes '+check('has_war_with = RKH NOT = { has_war_with = SVN } v65_sanctuary_operational = yes','DOMESTIC_WAR_WITH_EXTERNAL_SANCTUARY')+' } '
 script+='SVN = { v65_upgrade_staff = yes v65_upgrade_staff = yes '+check('has_idea = v65_staff_2 NOT = { has_idea = v65_staff_1 }','INSTITUTIONS_REPLACE_PREVIOUS_TIER')
 script+='set_variable = { v65_public_trust = 70 } set_variable = { v65_war_fatigue = 85 } v65_refresh_society = yes '+check('has_idea = v65_social_mandate has_idea = v65_exhaustion','SOCIETY_AND_FATIGUE_HAVE_REAL_SPIRITS')
 script+='v65_devolve_regions = yes } } if = { limit = { date > 1965.11.07 NOT = { has_global_flag = v65_regions_handed_over } } set_global_flag = v65_regions_handed_over SVN = { '+check('has_idea = v65_decentralized_command NOT = { owns_state = 16 } NOT = { owns_state = 28 }','DEVOLUTION_TRANSFERS_LAND')+' } '
 for tag,capital in [('HLC',16),('MKG',28),('BHD',22),('PHQ',31)]:
  script+=f'{tag} = {{ '+check(f'owns_state = {capital} num_divisions > 1 is_in_faction_with = SVN has_focus_tree = v65_{tag}_tree','REGION_'+tag+'_FUNCTIONAL')+' } '
 script+='} if = { limit = { date > 1965.11.08 NOT = { has_global_flag = v65_local_checked } } set_global_flag = v65_local_checked '
 script+='HLC = { set_variable = { v65_local_unrest = 7 } add_political_power = 100 v65_local_security_pulse = yes '+check('check_variable = { v65_local_unrest < 7 }','LOCAL_AI_HANDLES_ITS_SECURITY')+' } '
 script+='MKG = { v65_regional_outbreak = yes '+check('FNL = { controls_province = 348 }','LOCAL_REBELLION_CREATES_REAR_CONTROL')+' } '
 script+='} if = { limit = { date > 1965.11.10 NOT = { has_global_flag = v65_reintegration_checked } } set_global_flag = v65_reintegration_checked '
 if os.environ.get('V65_KEEP_REGIONS')!='1':
  script+='BHD = { set_variable = { v65_regional_loyalty = 80 } } SVN = { v65_regional_reintegration_BHD = yes '+check('owns_state = 22 has_character = v65_nguyen_ngoc_loan has_country_leader = { character = v65_nguyen_van_thieu } BHD = { exists = no }','LOYAL_REGION_REINTEGRATES_WITH_COMMANDER')+' } '
 else:script+='SVN = { '+check('BHD = { exists = yes }','REGION_REMAINS_AUTONOMOUS')+' } '
 from narrative_scenes import SCENES
 script+='KHM = { '+next(x[6] for x in SCENES if x[0]==606)+' '+check('has_country_leader = { character = v65_lon_nol } has_country_flag = v65_republic_leader','REPUBLIC_ROUTE_CHANGES_ACTUAL_LEADER')+' } '
 script+='} if = { limit = { date > 1965.11.29 NOT = { has_global_flag = v65_capital_diagnostics } } set_global_flag = v65_capital_diagnostics '
 for tag in ['SVN','NVN','FNL','PKS','DNM','KHM','RKH','HLC','MKG','BHD','PHQ']:
  script+=f'{tag} = {{ if = {{ limit = {{ exists = yes }} log = "V65_ALIVE_{tag}" if = {{ limit = {{ capital_scope = {{ is_fully_controlled_by = {tag} }} }} log = "V65_CAPITAL_HELD_{tag}" }} else = {{ log = "V65_CAPITAL_LOST_{tag}" }} if = {{ limit = {{ has_war = yes }} log = "V65_WAR_{tag}" }} }} }} '
 script+='} if = { limit = { date > 1965.12.27 NOT = { has_global_flag = v65_callback_checked } } set_global_flag = v65_callback_checked '+check('has_global_flag = v65_callback_101','NARRATIVE_CHOICE_REACHES_DELAYED_CALLBACK')
 script+=f' }} if = {{ limit = {{ date > 1965.12.28 }} log = "{end}" }} }} }} }}'
command_test=os.environ.get('V65_COMMAND_TEST')=='1'
presentation_test=os.environ.get('V65_PRESENTATION_TEST')=='1'
revision_test=os.environ.get('V65_REVISION_TEST')=='1'
stability_test=os.environ.get('V65_STABILITY_TEST')=='1'
story_revision_test=os.environ.get('V65_STORY_REVISION_TEST')=='1'
if story_revision_test:
 from story_revision_probe import build
 expected=[]
 script=build(check,begin,end)
if command_test:
 from command_probe import build
 expected=[]
 script=build(check,begin,end)
if presentation_test:
 from presentation_probe import build
 expected=[]
 script=build(check,begin,end)
if revision_test:
 from revision_probe import build
 expected=[]
 script=build(check,begin,end)
if stability_test:
 from stability_probe import build
 expected=[]
 script=build(check,begin,end)
probe=O/'common/on_actions/v65_smoke_test.txt';define=O/'common/defines/zzz_smoke_test.lua'
playset=U/'dlc_load.json';descriptor=U/'mod/v65_public.mod'
old_load=playset.read_bytes() if playset.exists() else None
old_descriptor=descriptor.read_bytes() if descriptor.exists() else None
proc=None
scenario_backups={}
try:
 if stages:
  # Force only defeat predicates; leave ownership, armies and AI fronts intact.
  # The normal and natural-balance runs compile/use the real map predicates.
  path=O/'common/scripted_triggers/v65_war_stages.txt';scenario_backups[path]=path.read_bytes()
  path.write_text('v65_highland_has_fallen = { always = yes }\nv65_saigon_has_fallen = { always = yes }\n',encoding='utf-8')
 probe.write_text(script);define.write_text('NDefines.NGame.HANDS_OFF_START_TAG = "'+'SVN'+'"\n')
 descriptor.parent.mkdir(exist_ok=True)
 descriptor.write_text((O/'descriptor.mod').read_text().replace('Vietnam 1965 - Indochina Theater','Vietnam 1965 Public')+'\npath="'+O.as_posix()+'"\n',encoding='utf-8')
 for charfile in (O/'common/characters').glob('v65_*.txt'):
  for picture in re.findall(r'large = "([^"]+)"',charfile.read_text()):assert (O/picture).exists(),picture
 d=json.loads(playset.read_text(encoding='utf-8-sig')) if playset.exists() else {'disabled_dlcs':[]}
 d['enabled_mods']=['mod/v65_public.mod'];playset.write_text(json.dumps(d))
 proc=subprocess.Popen([str(G/'hoi4.exe'),'-hands_off','-start_tag='+'SVN'],cwd=G)
 print('Engine started; expected assertions:',len(expected),flush=True)
 deadline=time.monotonic()+240;saw_start=False
 while time.monotonic()<deadline:
  if proc.poll() is not None:raise RuntimeError(f'Engine exited early: {proc.returncode}')
  s=(U/'logs/game.log').read_text(encoding='utf-8',errors='replace') if (U/'logs/game.log').exists() else ''
  if begin in s:saw_start=True
  if saw_start and 'V65_FAIL_' in s:raise AssertionError(re.findall(r'V65_FAIL_\w+',s))
  if saw_start and end in s:break
  time.sleep(1)
 else:raise TimeoutError('Engine did not finish campaign test within 240 seconds')
 markers=sorted(set(re.findall(r'V65_PASS_\w+',s)));assert set(markers)==set(expected),(markers,expected)
 errors=(U/'logs/error.log').read_text(encoding='utf-8',errors='replace').splitlines()
 mod_errors=[e for e in errors if not any(k in e for k in ['checksum','supported_version','thumbnail'])]
 result={'passed':not mod_errors,'markers':markers,'last_date':'1965.11.04' if routes or stages else '1965.11.29' if balance else '1965.11.06','method':'real engine; hands-off; no UI automation','human_transfer_exercised':'V65_PLAYER_TRANSFER_BRANCH' in s,'checked_at':datetime.datetime.now().isoformat(),'mod_runtime_errors':mod_errors}
 if long_run:result['last_date']='1965.12.29'
 if command_test:result['last_date']='1965.11.18'
 if revision_test:result['last_date']='1965.11.14'
 if stability_test:result['last_date']='1966.1.29'
 if story_revision_test:
  result['last_date']='1965.12.17'
  (OUT/'story-revision-engine-assertions.json').write_text(json.dumps(result,indent=2))
 (OUT/('stability-engine-assertions.json' if stability_test else 'revision-engine-assertions.json' if revision_test else 'presentation-engine-assertions.json' if presentation_test else 'command-engine-assertions.json' if command_test else 'autonomy-engine-assertions.json' if long_run and os.environ.get('V65_KEEP_REGIONS')=='1' else 'long-engine-assertions.json' if long_run else 'stages-engine-assertions.json' if stages else 'routes-engine-assertions.json' if routes else 'balance-engine-assertions.json' if balance else 'campaign-engine-assertions.json')).write_text(json.dumps(result,indent=2))
 assert not mod_errors, f'{len(mod_errors)} runtime errors; complete evidence in {OUT}'
 print('PASS:',len(markers),'engine assertions; no mod runtime errors')
finally:
 if proc and proc.poll() is None:proc.terminate();proc.wait(timeout=15)
 for path,data in scenario_backups.items():path.write_bytes(data)
 for name in ['game','error']:
  p=U/f'logs/{name}.log'
  if p.exists():
   data=p.read_bytes();sha=hashlib.sha256(data).hexdigest();(OUT/f'final-{name}-{sha[:12]}.log').write_bytes(data)
 probe.unlink(missing_ok=True);define.unlink(missing_ok=True)
 if old_load is not None:playset.write_bytes(old_load)
 else:playset.unlink(missing_ok=True)
 if old_descriptor is not None:descriptor.write_bytes(old_descriptor)
 else:descriptor.unlink(missing_ok=True)
