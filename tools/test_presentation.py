"""Content gates for the command panel and the takeover phase."""
from pathlib import Path
import json, unittest
from PIL import Image

R = Path(__file__).resolve().parents[1]
M = R / 'mod'


class PresentationTests(unittest.TestCase):
    def test_command_panel_is_attached_and_widgets_fit(self):
        category = (M/'common/decisions/categories/v65_command.txt').read_text(encoding='utf-8')
        self.assertIn('scripted_gui = v65_command_panel', category)
        layout = json.loads((R/'command-panel-layout.json').read_text(encoding='utf-8'))
        for item in layout['widgets']:
            self.assertGreaterEqual(item['x'], 0)
            self.assertGreaterEqual(item['y'], 0)
            self.assertLessEqual(item['x']+item['width'], layout['width'], item['name'])
            self.assertLessEqual(item['y']+item['height'], layout['height'], item['name'])
        # Sprite sheets must fit a 16K texture; frame count otherwise hides an oversized atlas.
        with Image.open(M/'gfx/interface/v65_command/prestige.dds') as atlas:
            self.assertLessEqual(max(atlas.size), 16384)
            self.assertEqual(atlas.width % 101, 0)

    def test_union_enters_government_phase_after_annexation(self):
        s=(M/'common/scripted_effects/v65_union_sanctuary.txt').read_text(encoding='utf-8')
        self.assertLess(s.index('send_equipment_fraction'), s.index('annex_country'))
        self.assertLess(s.index('annex_country'), s.index('v65_begin_park_government = yes'))
        phase=(M/'common/scripted_effects/v65_park_government.txt').read_text(encoding='utf-8')
        self.assertIn('load_focus_tree = { tree = v65_park_government',phase)
        self.assertIn('keep_completed = yes',phase)

    def test_art_has_substantially_more_distinct_bindings(self):
        manifest=json.loads((R/'focus-art-manifest.json').read_text(encoding='utf-8'))
        self.assertGreaterEqual(len({x['texture'] for x in manifest['bindings']}),45)
        self.assertGreaterEqual(len({x['texture'] for x in manifest['assignments'].values()}),45)
        self.assertEqual(len(manifest['assignments']),447)

    def test_rear_pressure_has_local_effects_and_local_response(self):
        dynamic=(M/'common/dynamic_modifiers/v65_rear.txt').read_text(encoding='utf-8')
        for n in [1,2,3]:self.assertIn('v65_rear_pressure_'+str(n),dynamic)
        decisions=(M/'common/decisions/v65_rear.txt').read_text(encoding='utf-8')
        self.assertIn('v65_rear_patrol_18',decisions)
        self.assertIn('v65_rear_network_18',decisions)
        self.assertIn('v65_rear_rise_18',decisions)


if __name__=='__main__':unittest.main()
