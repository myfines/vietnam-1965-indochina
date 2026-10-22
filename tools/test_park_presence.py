"""Travel must not silently annex the government hosting a visitor."""
from pathlib import Path
import sys,unittest,json
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'vendor'))
import pdx

class PresenceTests(unittest.TestCase):
    def test_travel_is_not_headquarters_transfer(self):
        s=(R/'mod/common/scripted_effects/v65_presence.txt').read_text()
        self.assertEqual(len(pdx.parse(s)),8)
        for forbidden in ['transfer_state','set_capital','annex_country','declare_war_on']:
            self.assertNotIn(forbidden,s)
        for gate in ['is_fully_controlled_by','v65_personal_network_actor','v65_park_visit_cooldown']:
            self.assertIn(gate,s)
        self.assertEqual(len(pdx.parse(s)),8)

    def test_park_is_not_starting_theater_commander(self):
        chars=pdx.read(R/'mod/common/characters/v65_PKS.txt')[0][2]
        park=next(b for k,_,b in chars if k=='v65_park_seicheng')
        chae=next(b for k,_,b in chars if k=='v65_chae_myeong_sin')
        self.assertNotIn('country_leader',[k for k,_,_ in park])
        self.assertIn('corps_commander',[k for k,_,_ in park])
        self.assertIn('country_leader',[k for k,_,_ in chae])

    def test_expiry_does_not_depend_on_visiting_country_survival(self):
        effects=(R/'mod/common/scripted_effects/v65_presence.txt').read_text()
        daily=(R/'mod/common/on_actions/v65_presence.txt').read_text()
        self.assertNotIn('country_event',effects)
        self.assertIn('v65_park_visit_days = 30',effects)
        self.assertIn('subtract_from_variable = { v65_park_visit_days = 1 }',daily)
        self.assertIn('clr_global_flag = v65_park_visit_cooldown',daily)

    def test_spirits_distinguish_political_conditions(self):
        d=json.loads((R/'spirit-art-manifest.json').read_text())
        a=d['assignments']
        self.assertNotEqual(a['v65_central_respected'],a['v65_central_discredited'])
        self.assertNotEqual(a['v65_private_staff'],a['v65_personal_staff'])
        self.assertGreaterEqual(len(set(a.values())),30)

if __name__=='__main__':unittest.main()
