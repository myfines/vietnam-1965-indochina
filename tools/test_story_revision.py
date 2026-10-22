"""Regression gates for island spawning and focus-panel geometry."""
from pathlib import Path
import sys, unittest

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R/'vendor'))
import pdx


class StoryRevisionTests(unittest.TestCase):
    def test_island_has_no_local_liberation_spawn(self):
        text=(R/'mod/common/scripted_effects/v65_society.txt').read_text(encoding='utf-8')
        outbreak=next(v for k, _, v in pdx.parse(text) if k=='v65_regional_outbreak')
        self.assertNotIn('tag = PHQ', pdx.dump(outbreak))
        self.assertNotIn('location = 361', pdx.dump(outbreak))

    def test_continuous_panel_sits_below_every_focus(self):
        for path in (R/'mod/common/national_focus').glob('v65_*.txt'):
            for key, _, tree in pdx.read(path):
                if key!='focus_tree':continue
                nodes=[dict((k,v) for k,_,v in n) for k,_,n in tree if k=='focus']
                panel=next((dict((k,v) for k,_,v in n) for k,_,n in tree if k=='continuous_focus_position'),None)
                self.assertIsNotNone(panel,path.name)
                self.assertGreaterEqual(float(panel['y']),max(float(n.get('y',0)) for n in nodes)*130+400,path.name)

    def test_chapter_routes_are_real_forks_in_both_phases(self):
        for filename,prefix in [('v65_PKS.txt','pks'),('v65_PARK_GOVERNMENT.txt','svn')]:
            tree=pdx.read(R/'mod/common/national_focus'/filename)[0][2]
            nodes=[n for k,_,n in tree if k=='focus' and dict((a,v) for a,_,v in n)['id'].startswith('v65chapter_')]
            self.assertEqual(len(nodes),22,filename)
            self.assertEqual(sum(any(k=='mutually_exclusive' for k,_,v in n) for n in nodes),12)
            for node in nodes:
                for k,_,v in node:
                    if k=='prerequisite':
                        self.assertTrue(all(key=='focus' and isinstance(target,str) for key,_,target in v))
            if prefix=='svn':self.assertTrue(all(any(k=='bypass' for k,_,v in n) for n in nodes))

    def test_new_variable_effects_do_not_hide_second_assignments(self):
        def walk(entries):
            for key,_,value in entries:
                if isinstance(value,list):
                    if key in ['add_to_variable','subtract_from_variable','set_variable']:
                        self.assertLessEqual(len(value),1,(key,value))
                    walk(value)
        for name in ['v65_chapter_focus.txt','v65_narrative.txt','v65_personal_network.txt']:
            walk(pdx.read(R/'mod/events'/name))

    def test_network_tooltips_use_numeric_variable_interpolation(self):
        text=(R/'mod/localisation/simp_chinese/zzzzzzzzzzzz_v65_personal_network_l_simp_chinese.yml').read_text(encoding='utf-8-sig')
        self.assertIn('[?SVN.v65_private_wealth|0]',text)
        self.assertIn('[?SVN.v65_network_DNM|0]',text)
        self.assertNotIn('[SVN.v65_',text)


if __name__=='__main__':unittest.main()
