"""Shared country configuration and persistent focus rewards."""
REGIONS={
 'HLC':('西原军区','Central Highlands Command',16,[14,16,18,20],'92 123 80','nguyen_khanh','阮庆','VIE/GENERALS/Nguyen_Khanh.dds'),
 'MKG':('湄公河军区','Mekong Command',28,[27,28,29],'94 148 160','tran_van_hai','陈文海','VIE/GENERALS/Tran_Van_Hai.dds'),
 'BHD':('东南军区','Southeastern Command',22,[21,22],'172 119 81','nguyen_ngoc_loan','阮玉鸾','VIE/GENERALS/Nguyen_Ngoc_Loan.dds'),
 'PHQ':('富国岛特别区','Phu Quoc Special Zone',31,[31],'88 104 174','li_weiyan','李威炎',None),
}
PLAYABLE=['SVN','NVN','FNL','PKS','DNM','KHM','RKH']
ALL=PLAYABLE+list(REGIONS)
def loc_text(values,lang):
 lines=['l_'+lang+':']
 for key,value in values.items():
  value=value.replace('"',r'\"').replace('\n',r'\n')
  lines.append(f' {key}:0 "{value}"')
 return '\n'.join(lines)
def enhance_rewards(rewards):
 rewards.update({
  'command':'v65_upgrade_staff = yes add_political_power = 25',
  'training':'v65_upgrade_training = yes army_experience = 10',
  'intel':'v65_upgrade_signals = yes add_to_variable = { v65_intelligence = 1 }',
  'supply':'v65_upgrade_logistics = yes add_equipment_to_stockpile = { type = infantry_equipment_2 amount = 600 producer = ROOT }',
  'funds':'v65_upgrade_contracts = yes add_to_variable = { v65_patronage = 5 } add_political_power = 35',
  'civil':'add_to_variable = { v65_public_trust = 5 } v65_refresh_society = yes add_political_power = 15',
  'pacify':'add_to_variable = { v65_public_trust = 5 } subtract_from_variable = { v65_local_unrest = 2 } v65_refresh_society = yes',
 })
