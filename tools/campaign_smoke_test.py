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
probe=O/'common/on_actions/v65_smoke_test.txt';define=O/'common/defines/zzz_smoke_test.lua'
playset=U/'dlc_load.json';descriptor=U/'mod/v65_public.mod'
old_load=playset.read_bytes() if playset.exists() else None
old_descriptor=descriptor.read_bytes() if descriptor.exists() else None
proc=None
try:
 probe.write_text(script);define.write_text('NDefines.NGame.HANDS_OFF_START_TAG = "SVN"\n')
 descriptor.parent.mkdir(exist_ok=True)
 descriptor.write_text((O/'descriptor.mod').read_text().replace('Vietnam 1965 - Indochina Theater','Vietnam 1965 Public')+'\npath="'+O.as_posix()+'"\n',encoding='utf-8')
 for charfile in (O/'common/characters').glob('v65_*.txt'):
  for picture in re.findall(r'large = "([^"]+)"',charfile.read_text()):assert (O/picture).exists(),picture
 d=json.loads(playset.read_text(encoding='utf-8-sig')) if playset.exists() else {'disabled_dlcs':[]}
 d['enabled_mods']=['mod/v65_public.mod'];playset.write_text(json.dumps(d))
 proc=subprocess.Popen([str(G/'hoi4.exe'),'-hands_off','-start_tag=SVN'],cwd=G)
 print('Engine started; expected assertions:',len(expected),flush=True)
 deadline=time.monotonic()+180;saw_start=False
 while time.monotonic()<deadline:
  if proc.poll() is not None:raise RuntimeError(f'Engine exited early: {proc.returncode}')
  s=(U/'logs/game.log').read_text(encoding='utf-8',errors='replace') if (U/'logs/game.log').exists() else ''
  if begin in s:saw_start=True
  if saw_start and 'V65_FAIL_' in s:raise AssertionError(re.findall(r'V65_FAIL_\w+',s))
  if saw_start and end in s:break
  time.sleep(1)
 else:raise TimeoutError('Engine did not finish campaign test within 180 seconds')
 markers=sorted(set(re.findall(r'V65_PASS_\w+',s)));assert set(markers)==set(expected),(markers,expected)
 errors=(U/'logs/error.log').read_text(encoding='utf-8',errors='replace').splitlines()
 mod_errors=[e for e in errors if not any(k in e for k in ['checksum','supported_version','thumbnail'])]
 result={'passed':not mod_errors,'markers':markers,'last_date':'1965.11.29' if balance else '1965.11.06','method':'real engine; hands-off; no UI automation','checked_at':datetime.datetime.now().isoformat(),'mod_runtime_errors':mod_errors}
 (OUT/('balance-engine-assertions.json' if balance else 'campaign-engine-assertions.json')).write_text(json.dumps(result,indent=2))
 assert not mod_errors,mod_errors
 print('PASS:',len(markers),'engine assertions; no mod runtime errors')
finally:
 if proc and proc.poll() is None:proc.terminate();proc.wait(timeout=15)
 for name in ['game','error']:
  p=U/f'logs/{name}.log'
  if p.exists():
   data=p.read_bytes();sha=hashlib.sha256(data).hexdigest();(OUT/f'final-{name}-{sha[:12]}.log').write_bytes(data)
 probe.unlink(missing_ok=True);define.unlink(missing_ok=True)
 if old_load is not None:playset.write_bytes(old_load)
 else:playset.unlink(missing_ok=True)
 if old_descriptor is not None:descriptor.write_bytes(old_descriptor)
 else:descriptor.unlink(missing_ok=True)
