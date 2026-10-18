from pathlib import Path
import json, unittest

R=Path(__file__).resolve().parents[1]
M=R/'mod'

class RevisionTests(unittest.TestCase):
    def test_recall_preserves_capital_until_whole_command_dissolved(self):
        s=(M/'common/decisions/v65_revision.txt').read_text(encoding='utf-8')
        self.assertIn('v65_recall_HLC_18',s)
        self.assertNotIn('v65_recall_HLC_16 =',s)
        self.assertIn('v65_dissolve_HLC',s)

    def test_mobile_park_has_no_quynhon_union_lock(self):
        s=(M/'common/scripted_triggers/v65_union_sanctuary.txt').read_text(encoding='utf-8')
        self.assertNotIn('controls_state = 15',s)
        s=(M/'common/scripted_effects/v65_revision.txt').read_text(encoding='utf-8')
        self.assertIn('v65_move_park_31',s)
        self.assertIn('v65_refresh_factions',s)

    def test_us_guard_and_island_evacuation_exist(self):
        s=(M/'common/scripted_effects/v65_intervention.txt').read_text(encoding='utf-8')
        self.assertIn('transfer_state = 10',s)
        self.assertIn('v65_evacuate_island',s)
        self.assertIn('v65_withdraw_intervention',s)

    def test_every_authored_spirit_has_resolvable_custom_art(self):
        manifest=json.loads((R/'spirit-art-manifest.json').read_text(encoding='utf-8'))
        self.assertGreaterEqual(len(manifest['assignments']),75)
        self.assertGreaterEqual(len(manifest['sources']),12)

if __name__=='__main__':unittest.main()
