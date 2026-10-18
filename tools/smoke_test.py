"""Run the engine's hands-off mode without desktop automation; retain evidence."""
from pathlib import Path
import subprocess,time,re,json,hashlib,datetime,os
R=Path(__file__).resolve().parents[1];O=R/'runtime/theater-mod';G=Path(json.loads((R/'runtime/install-report.json').read_text())['game']);U=Path.home()/'Documents/Paradox Interactive/Hearts of Iron IV';OUT=R/'runtime/test-results';OUT.mkdir(exist_ok=True)
probe=O/'common/on_actions/v65_smoke_test.txt';define=O/'common/defines/zzz_smoke_test.lua'
def check(condition,name):
 return f'if = {{ limit = {{ {condition} }} log = "V65_PASS_{name}" }} else = {{ log = "V65_FAIL_{name}" }}'
script='on_actions = { on_startup = { effect = { log = "V65_SMOKE_BEGIN" '
for tag,count in [('SVN',18),('NVN',18),('KHM',8)]:
 script+=tag+' = { '+check(f'num_divisions > {count-1}',tag+'_UNITS')+' '+check(f'has_focus_tree = v65_{tag}_tree',tag+'_FOCUS_TREE')+' } '
script+='SVN = { '+check('has_war_with = NVN','WAR')+' '+check('has_country_flag = v65_intro_seen','INTRO')+' } } } on_daily = { effect = { if = { limit = { date > 1965.11.05 } log = "V65_SMOKE_END" } } } }'
politics=os.environ.get('V65_TEST_POLITICS')=='1'
if politics:
 script=script.replace('log = "V65_SMOKE_BEGIN"','log = "V65_SMOKE_BEGIN" SVN = { complete_national_focus = v65_SVN_park_mission complete_national_focus = v65_SVN_yushin }')
 scenario='SVN = { v65_enact_martial_law = yes '+check('10 = { NOT = { has_state_flag = v65_under_martial_law } } 25 = { has_state_flag = v65_under_martial_law }','DMZ_EXCEPTION')
 scenario+='v65_resolve_coup = yes '+check('NOT = { has_country_flag = v65_civil_war_started } NOT = { has_country_flag = v65_coup_victory }','COUP_FAILURE')
 scenario+='23 = { set_variable = { v65_loyalty = 80 } } 24 = { set_variable = { v65_loyalty = 80 } } 26 = { set_variable = { v65_loyalty = 80 } } v65_resolve_coup = yes '+check('has_country_flag = v65_coup_victory','COUP_PEACE')+' } '
 scenario+='NVN = { set_variable = { v65_infiltration = 1 } set_variable = { v65_trail_level = 2 } v65_launch_infiltration = yes log = "V65_RAID_TRACE ready=[?v65_infiltration] level=[?v65_trail_level] divisions=[?num_divisions]" '+''.join(f'if = {{ limit = {{ {cond} }} log = "V65_DEBUG_{label}" }} ' for cond,label in [('has_country_flag = v65_raid_fired','FIRED'),('num_divisions > 18','DIVISIONS'),('OR = { controls_province = 251 controls_province = 269 controls_province = 291 }','CONTROL'),('has_country_flag = v65_raid_cooldown','COOLDOWN')])+check('has_country_flag = v65_raid_fired num_divisions > 18 OR = { controls_province = 251 controls_province = 269 controls_province = 291 } check_variable = { v65_infiltration = 0 } check_variable = { v65_trail_level = 1 } has_country_flag = v65_raid_cooldown','REAR_UNITS')+' } '
 civil='SVN = { '+check('has_idea = v65_park_patron','PARK_PORTRAIT_IDEA')+' '+check('OR = { has_country_flag = v65_park_presidential has_country_flag = v65_park_autonomy }','PARK_STORY_BRANCH')+' 24 = { set_variable = { v65_loyalty = 0 } } 26 = { set_variable = { v65_loyalty = 0 } } v65_resolve_coup = yes '+check('has_country_flag = v65_civil_war_started any_other_country = { has_country_flag = v65_coup_rebels }','COUP_CIVIL_WAR')+' } '
 script+=' on_actions = { on_daily = { effect = { if = { limit = { date > 1965.10.29 NOT = { has_global_flag = v65_probe_done } } set_global_flag = v65_probe_done '+scenario+' } if = { limit = { date > 1965.11.01 NOT = { has_global_flag = v65_civil_probe_done } } set_global_flag = v65_civil_probe_done '+civil+' } } } }'
running=subprocess.run(['tasklist','/FI','IMAGENAME eq hoi4.exe','/FO','CSV','/NH'],capture_output=True,text=True).stdout
if 'hoi4.exe' in running.lower():raise RuntimeError('Close the running game before this isolated engine test')
nonce=str(time.time_ns());begin='V65_SMOKE_BEGIN_'+nonce;end='V65_SMOKE_END_'+nonce
script=script.replace('V65_SMOKE_BEGIN',begin).replace('V65_SMOKE_END',end)
probe.write_text(script);define.write_text('NDefines.NGame.HANDS_OFF_START_TAG = "SVN"\n')
proc=None
playset=U/'dlc_load.json';descriptor=U/'mod/v65_public.mod'
old_load=playset.read_bytes() if playset.exists() else None
old_descriptor=descriptor.read_bytes() if descriptor.exists() else None
try:
 descriptor.parent.mkdir(exist_ok=True)
 descriptor.write_text((O/'descriptor.mod').read_text()+'\npath="'+O.as_posix()+'"\n',encoding='utf-8')
 for tag in ['NVN','SVN','KHM','XTR']:
  hist=(O/f'history/countries/{tag} - Theater.txt').read_text();pic=re.search(r'picture = "([^"]+)"',hist)[1];assert (O/pic).exists() or (G/pic).exists(),pic
 playset=U/'dlc_load.json';d=json.loads(playset.read_text());d['enabled_mods']=['mod/v65_public.mod'];playset.write_text(json.dumps(d))
 proc=subprocess.Popen([str(G/'hoi4.exe'),'-hands_off','-start_tag=SVN'],cwd=G)
 print(f'Engine test started, pid {proc.pid}',flush=True);deadline=time.monotonic()+150;saw_start=False
 while time.monotonic()<deadline:
  if proc.poll() is not None:raise RuntimeError(f'Engine exited early: {proc.returncode}')
  s=(U/'logs/game.log').read_text(encoding='utf-8',errors='replace') if (U/'logs/game.log').exists() else ''
  if begin in s:saw_start=True
  if saw_start and 'V65_FAIL_' in s:raise AssertionError('Engine assertions failed: '+str(re.findall(r'V65_FAIL_\w+',s)))
  if saw_start and end in s:break
  time.sleep(1)
 else:raise TimeoutError('Engine did not reach November 6 within 150 seconds')
 markers=sorted(set(re.findall(r'V65_PASS_\w+',s)));assert len(markers)==(15 if politics else 8),markers
 result={'passed':True,'markers':markers,'last_date':re.findall(r'\[(\d{4}\.\d+\.\d+\.\d+)\].*V65_SMOKE_END',s)[-1],'method':'engine -hands_off -start_tag=SVN; no desktop automation','checked_at':datetime.datetime.now().isoformat()}
 errors=(U/'logs/error.log').read_text(encoding='utf-8',errors='replace').splitlines()
 result['mod_runtime_errors']=[e for e in errors if not any(k in e for k in ['checksum','supported_version','thumbnail'])]
 assert not result['mod_runtime_errors'],result['mod_runtime_errors']
 (OUT/('politics-engine-assertions.json' if politics else 'engine-assertions.json')).write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
finally:
 if proc and proc.poll() is None:proc.terminate();proc.wait(timeout=15)
 for name in ['game','error']:
  f=U/f'logs/{name}.log'
  if f.exists():
   data=f.read_bytes();sha=hashlib.sha256(data).hexdigest();(OUT/f'final-{name}-{sha[:12]}.log').write_bytes(data)
 probe.unlink(missing_ok=True);define.unlink(missing_ok=True)
 if old_load is not None:playset.write_bytes(old_load)
 else:playset.unlink(missing_ok=True)
 if old_descriptor is not None:descriptor.write_bytes(old_descriptor)
 else:descriptor.unlink(missing_ok=True)
