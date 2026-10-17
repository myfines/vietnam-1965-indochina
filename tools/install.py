"""Build a local runtime from authored files and the user's installed game."""
from pathlib import Path
import argparse,sys,shutil,json
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'vendor'))
import hoi4mod as hm
import pdx
parser=argparse.ArgumentParser()
parser.add_argument('--game',type=Path)
args=parser.parse_args()
def discover():
 candidates=[Path('F:/SteamLibrary/steamapps/common/Hearts of Iron IV'),Path('C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV')]
 try:
  import winreg,re
  with winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Valve\Steam') as k:steam=Path(winreg.QueryValueEx(k,'SteamPath')[0])
  candidates.append(steam/'steamapps/common/Hearts of Iron IV')
  vdf=steam/'steamapps/libraryfolders.vdf'
  if vdf.exists():
   candidates.extend(Path(x.replace('\\\\','/'))/'steamapps/common/Hearts of Iron IV' for x in re.findall(r'"path"\s+"([^"]+)"',vdf.read_text(encoding='utf-8')))
 except (OSError,ImportError):pass
 return next((p for p in candidates if (p/'hoi4.exe').exists()),None)
game=args.game or discover()
if not game or not (game/'hoi4.exe').exists():raise SystemExit('Use python tools/install.py --game "PATH TO Hearts of Iron IV"')
out=R/'runtime/theater-mod';out.mkdir(parents=True,exist_ok=True)
van=hm.Vanilla(game);report={}
print('Preparing compatibility files from the local game installation...',flush=True)
hm.write_neutralised(out,van,report,our_tags=('NVN','SVN','KHM','XTR'))
for name in ['default.map','seasons.txt','cities.txt','colors.txt']:
 p=game/'map'/name
 if p.exists():
  (out/'map').mkdir(exist_ok=True);shutil.copyfile(p,out/'map'/name)
hm.write_ambient(out/'map',van,2048,3072)
shutil.copytree(R/'mod',out,dirs_exist_ok=True)
tags=out/'common/country_tags';tags.mkdir(exist_ok=True)
(tags/'00_countries.txt').write_text('# Countries are defined in v65.txt\n')
shutil.copyfile(game/'common/country_tags/zz_dynamic_countries.txt',tags/'zz_dynamic_countries.txt')
colors=pdx.read(game/'common/countries/colors.txt')
colors=[(k,o,v) for k,o,v in colors if k in set(van.dynamic_tags)]
for tag,rgb in [('NVN','190 40 40'),('SVN','224 184 67'),('KHM','60 110 180'),('XTR','65 70 65')]:
 colors+=pdx.parse(f'{tag} = {{ color = rgb {{ {rgb} }} color_ui = rgb {{ {rgb} }} }}')
(out/'common/countries/colors.txt').write_text(pdx.dump(colors),encoding='utf-8')
hm.write_names(out,{tag:{'tag':tag,'vanilla':base,'gfx':('asian_gfx',)} for tag,base in [('NVN','VIN'),('SVN','VIE'),('KHM','CAM'),('XTR','LAO')]},van)
errors=hm.check_mod(out)
if errors:raise SystemExit('Installation validation errors: '+str(errors))
(R/'runtime/install-report.json').write_text(json.dumps({'game':str(game),'runtime':str(out),'validation_errors':errors},indent=2))
print('Installed and checked:',out)
