"""Named leaders, generals and advisers; third-party portraits hydrate locally."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];M=R/'mod'
# tag, identity, name, portrait in CWIC, role
PEOPLE=[
('NVN','ho_chi_minh','胡志明','VIN/Ho_Chi_Minh_60s.dds','leader'),
('NVN','vo_nguyen_giap','武元甲','VIN/Vo_Nguyen_Giap.dds','marshal'),
('NVN','le_duan','黎笋','VIN/Le_Duan.dds','adviser'),
('NVN','truong_chinh','长征','VIN/Truong_Chinh.dds','adviser'),
('SVN','nguyen_van_thieu','阮文绍','VIE/Nguyen_Van_Thieu_1960.dds','leader'),
('SVN','duong_van_minh','杨文明','VIE/GENERALS/Duong_Van_Minh.dds','general'),
('SVN','tran_thien_khiem','陈善谦','VIE/GENERALS/Tran_thien_Khiem.dds','general'),
('SVN','tran_van_huong','陈文香','VIE/Tran_Van_Huong.dds','adviser'),
('SVN','nguyen_ngoc_tho','阮玉书','VIE/Nguyen_Ngoc_Tho_60s.dds','adviser'),
('PKS','park_seicheng','朴世诚',None,'leader_general'),
('PKS','kim_jong_pil','金钟泌','KOR/Kim_Jong-pil.dds','adviser'),
('PKS','kim_jae_gyu','金载圭','KOR/Kim_Jae-gyu.dds','adviser'),
('PKS','park_chung_hee','朴正熙（政治庇护）','KOR/Park_Chung-hee_63.dds','adviser'),
('FNL','nguyen_huu_tho','阮友寿','VIN/Nguyen_Huu_Tho.dds','leader'),
('FNL','nguyen_van_linh','阮文灵','VIN/Nguyen_Van_Linh.dds','adviser'),
('DNM','ngo_quang_truong','吴光长','VIE/GENERALS/Ngo_Quang_Truong.dds','leader_general'),
('DNM','do_cao_tri','杜高智','VIE/GENERALS/Do_Cao_Tri.dds','general'),
('KHM','norodom_sihanouk','诺罗敦·西哈努克','CAM/Norodom_Sihanouk_60s.dds','leader'),
('KHM','lon_nol','朗诺','CAM/Lon_Nol_70s.dds','adviser'),
('KHM','sisowath_monireth','西索瓦·莫尼勒','CAM/FARK/Sisowath_Monireth.dds','general'),
('KHM','les_kosem','莱斯·科森','CAM/FARK/Les_Kosem.dds','general'),
]
catalog=[];locales={};chars={t:[] for t in ['SVN','NVN','PKS','DNM','FNL','KHM']}
for tag,key,name,source,role in PEOPLE:
 cid='v65_'+key;portrait='gfx/leaders/v65/'+key+'.dds'
 if source:catalog.append({'id':key,'source':source,'target':portrait,'provider':'Cold War Iron Curtain','distribution':'downloaded into runtime only; not bundled in public repository'})
 locales[cid]=name
 body=f'{cid} = {{\n name = {cid}\n portraits = {{ civilian = {{ large = "{portrait}" small = "{portrait}" }} army = {{ large = "{portrait}" small = "{portrait}" }} }}\n'
 if 'leader' in role:
  ideology='marxism' if tag in ['NVN','FNL'] else 'despotism'
  body+=f' country_leader = {{ ideology = {ideology} expire = "1990.1.1" }}\n'
 if role in ['general','marshal','leader_general']:
  body+=f' {"field_marshal" if role=="marshal" else "corps_commander"} = {{ skill = {5 if role=="marshal" else 3} attack_skill = 3 defense_skill = 4 planning_skill = 3 logistics_skill = 3 traits = {{ }} }}\n'
 if role=='adviser':
  body+=f' advisor = {{ slot = political_advisor idea_token = {cid}_advisor cost = 100 traits = {{ {"backroom_backstabber" if key=="kim_jae_gyu" else "silent_workhorse"} }} }}\n'
 chars[tag].append(body+'}')
for tag,items in chars.items():
 p=M/f'common/characters/v65_{tag}.txt';p.parent.mkdir(parents=True,exist_ok=True);p.write_text('characters = {\n'+'\n'.join(items)+'\n}',encoding='utf-8')
 h=M/f'history/countries/{tag} - Theater.txt';s=h.read_text(encoding='utf-8-sig');s='\n'.join(x for x in s.splitlines() if not x.startswith('recruit_character = v65_'))
 s+='\n'+'\n'.join('recruit_character = v65_'+x[1] for x in PEOPLE if x[0]==tag)+'\n';h.write_text(s,encoding='utf-8')
for lang in ['simp_chinese','english']:
 p=M/f'localisation/{lang}/v65_characters_l_{lang}.yml'
 names=locales if lang=='simp_chinese' else {'v65_'+p[1]:p[1].replace('_',' ').title() for p in PEOPLE}
 p.write_text('l_'+lang+':\n'+'\n'.join(f' {k}:0 "{v}"\n {k}_advisor:0 "{v}"' for k,v in names.items())+'\n',encoding='utf-8-sig')
(R/'portrait-catalog.json').write_text(json.dumps(catalog,indent=2),encoding='utf-8')
print('Named characters:',len(PEOPLE),'(leaders, commanders, advisers)')
