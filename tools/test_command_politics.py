"""Contract checks for selectable districts and escalating command disputes."""
from pathlib import Path
import unittest

M = Path(__file__).resolve().parents[1] / 'mod'


class CommandPoliticsTests(unittest.TestCase):
    def test_districts_are_individually_commissioned(self):
        s = (M / 'common/decisions/v65_command.txt').read_text(encoding='utf-8')
        for tag in ['HLC', 'MKG', 'BHD', 'PHQ']:
            self.assertIn('v65_commission_' + tag, s)
            self.assertIn('v65_devolve_' + tag + ' = yes', s)
        self.assertIn('is_fully_controlled_by = SVN', s)

    def test_rebellion_requires_escalation_and_breaks_subject_relation(self):
        s = (M / 'common/scripted_effects/v65_command.txt').read_text(encoding='utf-8')
        self.assertIn('v65_central_prestige < 30', s)
        self.assertIn('v65_command_refused', s)
        self.assertIn('v65_regional_loyalty < 25', s)
        for tag in ['HLC', 'MKG', 'BHD', 'PHQ']:
            self.assertIn('set_autonomy = { target = ' + tag + ' autonomy_state = autonomy_free }', s)
        self.assertIn('v65command.10 days = 3', s)
        events = (M / 'events/v65_command.txt').read_text(encoding='utf-8')
        self.assertIn('declare_war_on = { target = SVN', events)

    def test_power_base_can_be_built_before_takeover(self):
        s = (M / 'common/decisions/v65_command.txt').read_text(encoding='utf-8')
        self.assertIn('v65_park_recruit_clients', s)
        self.assertIn('v65_park_request_command', s)
        self.assertIn('v65_park_takeover', s)
        self.assertIn('v65_personal_network > 5', s)
        self.assertIn('v65_central_prestige < 40', s)
        events = (M / 'events/v65_command.txt').read_text(encoding='utf-8')
        self.assertIn('v65_finalize_union = yes', events)
        self.assertIn('clr_country_flag = v65_union_pending', events)


if __name__ == '__main__':
    unittest.main()
