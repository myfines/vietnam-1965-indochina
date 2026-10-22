"""Mediation should resolve an agreed internal war, never an unrelated one."""
from pathlib import Path
import unittest,sys
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'vendor'));import pdx

class GuestTests(unittest.TestCase):
    def test_armistice_checks_every_party(self):
        s=(R/'mod/common/scripted_effects/v65_guest_stories.txt').read_text()
        effect=next(v for k,_,v in pdx.parse(s) if k=='v65_guest_finish')
        rendered=pdx.dump(effect)
        for flag in ['talks_open','region_agreed','island_agreed','central_agreed']:
            self.assertIn('v65_guest_'+flag,rendered)
        self.assertIn('white_peace = SVN',rendered)
        self.assertNotIn('white_peace = FNL',rendered)
        self.assertIn('has_war_with = SVN',rendered)

    def test_option_names_do_not_alias_descriptions(self):
        events=pdx.read(R/'mod/events/v65_guest_stories.txt')
        for kind,_,body in events:
            if kind!='country_event':continue
            desc=[v for k,_,v in body if k=='desc']
            for k,_,option in body:
                if k=='option':
                    for name,_,v in option:
                        if name=='name':self.assertNotIn(v,desc)
        self.assertEqual(sum(k=='country_event' for k,_,_ in events),9)

    def test_expiry_releases_global_mutex(self):
        s=(R/'mod/events/v65_guest_stories.txt').read_text()
        self.assertIn('id = v65guest.99',s)
        self.assertIn('clr_global_flag = v65_guest_cooldown',s)

    def test_initiating_player_selects_target(self):
        category=pdx.read(R/'mod/common/decisions/v65_guest_stories.txt')[0][2]
        decision=next(b for k,_,b in category if k=='v65_guest_mediation')
        completion=next(b for k,_,b in decision if k=='complete_effect')
        direct_events=[b for k,_,b in completion if k=='country_event']
        self.assertTrue(any(('id','=','v65guest.1') in b for b in direct_events))

if __name__=='__main__':unittest.main()
