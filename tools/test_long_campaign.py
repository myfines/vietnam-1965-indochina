"""Behavioral content gates for the 1965–1979 campaign expansion."""
from pathlib import Path
import re,unittest,json
R=Path(__file__).resolve().parents[1]

class LongCampaignTests(unittest.TestCase):
 def test_every_authored_spirit_explains_its_role(self):
  import sys
  sys.path.insert(0,str(R/'vendor'));import pdx
  loc='\n'.join(p.read_text(encoding='utf-8-sig') for p in (R/'mod/localisation').rglob('*simp_chinese.yml'))
  for path in (R/'mod/common/ideas').glob('v65*.txt'):
   for _,_,top in pdx.read(path):
    for kind,_,body in top:
     if kind=='country':
      for key,_,value in body:
       if key.startswith('v65_'):self.assertTrue(re.search(r'(?m)^ '+re.escape(key)+r'_desc:',loc),key+' missing description')
 def test_cambodian_civil_war_is_two_real_countries(self):
  tags=(R/'mod/common/country_tags/v65.txt').read_text(encoding='utf-8')
  self.assertRegex(tags,r'\bRKH\s*=','The Khmer Rouge is missing as a real country')
  states='\n'.join(p.read_text(encoding='utf-8-sig') for p in (R/'mod/history/states').glob('*.txt'))
  self.assertRegex(states,r'owner = RKH')
  self.assertIn('RKH', (R/'mod/common/bookmarks/v65.txt').read_text(encoding='utf-8'))
 def test_one_authoritative_cambodian_name_per_language(self):
  root=R/'mod/localisation'
  for lang in ['simp_chinese','english']:
   hits=[]
   for p in root.rglob('*.yml'):
    if p.name.endswith('_l_'+lang+'.yml'):
     hits.extend(re.findall(r'^\s*KHM:0 "([^"]+)"',p.read_text(encoding='utf-8-sig'),re.M))
   self.assertEqual(len(hits),1,hits)
   if lang=='simp_chinese':self.assertEqual(hits[0],'柬埔寨王国')
 def test_regional_autonomy_has_land_and_local_security(self):
  p=R/'mod/common/scripted_effects/v65_regions.txt'
  self.assertTrue(p.exists(),'No real regional autonomy mechanism')
  s=p.read_text(encoding='utf-8')
  for tag in ['HLC','MKG','BHD','PHQ']:self.assertIn('target = '+tag,s)
  self.assertIn('v65_local_unrest',s)
  self.assertIn('v65_regional_reintegration',s)
 def test_story_ends_in_1979_and_has_causal_callbacks(self):
  p=R/'narrative-manifest.json';self.assertTrue(p.exists())
  j=json.loads(p.read_text(encoding='utf-8'))
  self.assertEqual(j['years'],[1965,1968,1971,1974,1977,1979])
  self.assertGreaterEqual(j['story_events'],30)
  self.assertGreaterEqual(j['long_term_focuses'],100)
  s=(R/'mod/events/v65_narrative.txt').read_text(encoding='utf-8')
  self.assertIn('v65_public_trust',s)
  self.assertIn('v65_patronage',s)
  self.assertIn('v65story.901',s)

if __name__=='__main__':unittest.main()
