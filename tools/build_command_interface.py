"""Original command-dossier layout; game draws live text over original geometry."""
from pathlib import Path
import json
from PIL import Image, ImageDraw
from build_campaign import M, R, put
from long_foundation import loc_text

W,H=480,548
CARDS=[
 ('DNM','岘港军区','吴光长','ngo_quang_truong'),
 ('PKS','驻越韩军司令部','[PKS.GetLeader]',None),
 ('HLC','西原军区','阮庆','nguyen_khanh'),
 ('BHD','东南军区','阮玉鸾','nguyen_ngoc_loan'),
 ('MKG','湄公河军区','陈文海','tran_van_hai'),
 ('PHQ','富国岛特别区','[PHQ.GetLeader]',None),
]
out=M/'gfx/interface/v65_command';out.mkdir(parents=True,exist_ok=True)
bg=Image.new('RGBA',(W,H),(19,27,34,255));d=ImageDraw.Draw(bg)
# Quiet map-table geometry: inset brass rule, pale labels, separate data fields.
for row in range(H):
 shade=round(5*row/H)
 d.line((0,row,W,row),fill=(23-shade,33-shade,42-shade,255))
d.rectangle((1,1,W-2,H-2),outline=(126,113,83),width=1)
d.rectangle((5,5,W-6,H-6),outline=(50,63,70),width=1)
d.rectangle((12,11,15,39),fill=(195,166,108))
d.line((18,47,462,47),fill=(88,99,102))
d.rectangle((12,77,467,131),fill=(14,23,29),outline=(64,80,87))
for n in range(6):
 x=12+(n%2)*234;y=146+(n//2)*112
 d.rectangle((x+2,y+3,x+223,y+105),fill=(9,16,21))
 d.rectangle((x,y,x+221,y+103),fill=(29,42,50),outline=(70,89,96))
 d.rectangle((x+1,y+1,x+220,y+23),fill=(43,57,64))
 d.line((x+9,y+23,x+212,y+23),fill=(142,126,88))
 d.rectangle((x+9,y+30,x+61,y+100),fill=(12,20,25),outline=(127,117,93))
d.line((14,493,466,493),fill=(91,98,84))
bg.save(out/'dossier.dds')
# Native sprite frames are numbered from one: frame one is an empty bar.
bar=Image.new('RGBA',(110*101,2),(53,60,51,255));draw=ImageDraw.Draw(bar)
for n in range(101):
 if n:draw.rectangle((n*110,0,n*110+round(109*n/100),1),fill=(197,169,112))
bar.save(out/'prestige.dds')
gfx='spriteTypes = {\n spriteType = { name = "GFX_v65_dossier" texturefile = "gfx/interface/v65_command/dossier.dds" }\n spriteType = { name = "GFX_v65_prestige" texturefile = "gfx/interface/v65_command/prestige.dds" noOfFrames = 101 }\n'
gui=f'guiTypes = {{ containerWindowType = {{ name = "v65_command_window" size = {{ width = {W} height = {H} }}\n iconType = {{ name = "dossier" spriteType = "GFX_v65_dossier" position = {{ x = 0 y = 0 }} alwaystransparent = yes }}\n'
widgets=[]
L={
 'v65_panel_title':'南方军政协调处',
 'v65_panel_caption':'军饷 · 任命 · 作战指挥',
 'v65_panel_prestige':'中央威望  [?SVN.v65_central_prestige|0] / 100',
 'v65_panel_footer':'朴的行程：[v65_park_where]',
 'v65_panel_hint':'下方决议办理拨款、设区、划区与抗命。',
 'v65_panel_inactive':'无独立司令部',
 'v65_panel_rebel':'§R已起兵§!', 'v65_panel_refused':'§R拒绝调令§!',
 'v65_panel_ordered':'依指挥协定听令', 'v65_panel_independent':'独立指挥',
 'v65_panel_union':'已接管南越',
}
def text(name,key,x,y,width,height=22,font='hoi_16mbs'):
 global gui
 gui+=f'instantTextBoxType = {{ name = "{name}" position = {{ x = {x} y = {y} }} font = "{font}" text = "{key}" maxWidth = {width} maxHeight = {height} fixedsize = yes }}\n'
 widgets.append(dict(name=name,kind='text',key=key,x=x,y=y,width=width,height=height,font=font))
text('title','v65_panel_title',24,12,432,28,'hoi_24header')
text('caption','v65_panel_caption',17,56,440)
text('prestige_value','v65_panel_prestige',17,81,440,24,'hoi_18mbs')
gui+='iconType = { name = "prestige_bar" scale = 4 spriteType = "GFX_v65_prestige" position = { x = 18 y = 115 } alwaystransparent = yes }\n'
scripted='scripted_gui = { v65_command_panel = { context_type = decision_category window_name = "v65_command_window" ai_enabled = { always = no } properties = { prestige_bar = { frame = v65_prestige_frame } } } }'
loc='defined_text = { name = v65_park_metrics text = { trigger = { SVN = { has_country_flag = v65_union_complete } } localization_key = v65_park_metrics_after } text = { localization_key = v65_park_metrics_before } }\n'
for n,(tag,title,person,portrait) in enumerate(CARDS):
 x=12+(n%2)*234;y=146+(n//2)*112
 L['v65_panel_'+tag]=title
 L['v65_person_'+tag]=person
 L['v65_metrics_'+tag]=f'忠诚 [?{tag}.v65_regional_loyalty|0]  后患 [?{tag}.v65_rear_hotspots|0]'
 if tag=='PKS':
  L['v65_metrics_'+tag]='[v65_park_metrics]'
  L['v65_park_metrics_before']='人脉 [?PKS.v65_personal_network|0]  军援 [?PKS.v65_contract_credit|0]'
  L['v65_park_metrics_after']='人脉 [?SVN.v65_personal_network|0]  军援 [?SVN.v65_contract_credit|0]'
 L['v65_status_'+tag]='[v65_status_text_'+tag+']'
 text('label_'+tag,'v65_panel_'+tag,x+9,y+3,205,20)
 text('person_'+tag,'v65_person_'+tag,x+71,y+29,146,20)
 text('metrics_'+tag,'v65_metrics_'+tag,x+71,y+53,146,20)
 text('status_'+tag,'v65_status_'+tag,x+71,y+78,146,20)
 texture=f'gfx/leaders/v65/{portrait}.dds' if portrait else f'gfx/flags/{tag}.tga'
 gfx+=f'spriteType = {{ name = "GFX_v65_card_{tag}" texturefile = "{texture}" }}\n'
 # Portrait source dimensions are inspected, rather than assuming a shared aspect ratio.
 candidates=[M/texture,R/'runtime/theater-mod'/texture]
 source=next((p for p in candidates if p.exists()),None)
 if source:
  with Image.open(source) as im:iw,ih=im.size
 else:iw,ih=156,210
 scale=min(50/iw,68/ih)
 px=x+10+(50-iw*scale)/2;py=y+31+(68-ih*scale)/2
 gui+=f'iconType = {{ name = "portrait_{tag}" spriteType = "GFX_v65_card_{tag}" position = {{ x = {px:.2f} y = {py:.2f} }} scale = {scale:.4f} alwaystransparent = yes }}\n'
 widgets.append(dict(name='portrait_'+tag,kind='portrait',texture=texture,x=round(px),y=round(py),width=round(iw*scale),height=round(ih*scale)))
 loc+=f'defined_text = {{ name = v65_status_text_{tag}\n'
 if tag=='PKS':loc+='text = { trigger = { SVN = { has_country_flag = v65_union_complete } } localization_key = v65_panel_union }\n'
 loc+=f'text = {{ trigger = {{ {tag} = {{ exists = no }} }} localization_key = v65_panel_inactive }}\n'
 loc+=f'text = {{ trigger = {{ {tag} = {{ has_country_flag = v65_rebel_command }} }} localization_key = v65_panel_rebel }}\n'
 loc+=f'text = {{ trigger = {{ {tag} = {{ has_country_flag = v65_command_refused }} }} localization_key = v65_panel_refused }}\n'
 loc+=f'text = {{ trigger = {{ {tag} = {{ v65_under_central_command = yes }} }} localization_key = v65_panel_ordered }}\n'
 loc+='text = { localization_key = v65_panel_independent } }\n'
text('footer','v65_panel_footer',16,503,448,18)
text('hint','v65_panel_hint',16,525,448,18)
put(Path('interface/v65_command.gui'),gui+'} }')
put(Path('interface/v65_command.gfx'),gfx+'}')
put(Path('common/scripted_guis/v65_command.txt'),scripted)
put(Path('common/scripted_localisation/v65_command.txt'),loc)
put(Path('common/decisions/categories/v65_command.txt'),'v65_command_politics = { icon = GFX_decision_generic_military priority = 1500 visible_when_empty = yes scripted_gui = v65_command_panel allowed = { OR = { tag = SVN tag = PKS tag = DNM tag = HLC tag = MKG tag = BHD tag = PHQ } } visible = { always = yes } }')
put(Path('common/on_actions/v65_command_panel.txt'),'''on_actions = { on_daily = { effect = {
 SVN = { set_variable = { v65_prestige_frame = v65_central_prestige } add_to_variable = { v65_prestige_frame = 1 } round_variable = v65_prestige_frame clamp_variable = { var = v65_prestige_frame min = 1 max = 101 } }
 every_country = { limit = { OR = { tag = SVN tag = PKS tag = DNM tag = HLC tag = MKG tag = BHD tag = PHQ } } set_variable = { v65_prestige_frame = SVN.v65_prestige_frame } }
} } on_startup = { effect = { DNM = { if = { limit = { NOT = { has_country_flag = v65_panel_initialized } } set_country_flag = v65_panel_initialized set_variable = { v65_regional_loyalty = 65 } } } } } }''')
for lang in ['simp_chinese','english']:put(Path(f'localisation/{lang}/zzzzzzzz_v65_panel_l_{lang}.yml'),loc_text(L,lang))
(R/'command-panel-layout.json').write_text(json.dumps(dict(width=W,height=H,widgets=widgets),ensure_ascii=False,indent=2),encoding='utf-8')
print('Command dossier: six cards and live prestige, loyalty, allegiance and rear pressure')
