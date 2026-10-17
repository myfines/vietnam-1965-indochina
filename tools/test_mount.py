from pathlib import Path
import subprocess,json
r=Path('.').resolve();u=r/'runtime/test-user';u.mkdir(parents=True,exist_ok=True)
p=u/'dlc_load.json';p.write_text(json.dumps({'enabled_mods':['mod/example.mod'],'disabled_dlcs':['test']}))
def call(mode):
 out=subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File','tools/mount-mod.ps1','-Mode',mode,'-UserDir',str(u)],capture_output=True,text=True)
 assert out.returncode==0,(mode,out.stdout,out.stderr)
call('Mount');assert json.loads(p.read_text())['enabled_mods']==['mod/example.mod']
call('Enable');assert json.loads(p.read_text())['enabled_mods']==['mod/vietnam_1965_theater.mod']
call('Disable');assert json.loads(p.read_text())['enabled_mods']==['mod/example.mod']
call('Enable');j=json.loads(p.read_text());j['enabled_mods'].append('mod/new-choice.mod');p.write_text(json.dumps(j))
call('Disable');assert json.loads(p.read_text())['enabled_mods']==['mod/new-choice.mod']
call('Unmount');assert not (u/'mod/vietnam_1965_theater.mod').exists();assert (r/'mod/descriptor.mod').exists()
print('Mount/enable/restore/preserve-new-choices/unmount: PASS')
