"""Regression checks for the playable campaign, not just balanced braces."""
from pathlib import Path
import sys,re,unittest,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'vendor'))
import pdx

def values(block,key):
    return [v for k,op,v in block if k==key]
def one(block,key):
    return values(block,key)[0]

class CampaignTests(unittest.TestCase):
    def test_icons_and_portraits_are_bound(self):
        sprites=(ROOT/'mod/interface/v65_focus_icons.gfx').read_text()
        self.assertGreaterEqual(sprites.count('spriteType ='),9)
        for path in re.findall(r'texturefile = "([^"]+)"',sprites):
            self.assertTrue((ROOT/'mod'/path).exists() or (Path(json.loads((ROOT/'runtime/install-report.json').read_text())['game'])/path).exists(),path)
        people=list((ROOT/'mod/common/characters').glob('v65_*.txt'))
        text='\n'.join(p.read_text() for p in people)
        self.assertNotIn('Portrait_Asia_Generic',text)
        self.assertEqual(len(re.findall(r'\bname = v65_',text)),26)
        self.assertTrue((ROOT/'mod/gfx/leaders/v65/park_seicheng.dds').exists())
    def test_union_and_neutral_sanctuary(self):
        p=ROOT/'mod/common/scripted_effects/v65_union_sanctuary.txt'
        self.assertTrue(p.exists(),'Missing negotiated union and Cambodian rear-base mechanics')
        text=' '.join(p.read_text(encoding='utf-8').split())
        for effect in ['v65_finalize_union','v65_open_sanctuary','v65_close_sanctuary','v65_sanctuary_pulse']:
            self.assertIn(effect+' =',text)
        self.assertIn('is_ai = no',text)
        self.assertIn('v65_park_shadow_ruler',text)
        self.assertIn('NOT = { has_war_with = SVN }',text)
        self.assertIn('controls_state = 42',text)
        decisions=(ROOT/'mod/common/decisions/v65_union_sanctuary.txt').read_text(encoding='utf-8')
        self.assertIn('v65_request_union',decisions)
        self.assertIn('v65_border_dossier',decisions)

    def test_focus_layout_and_descriptions(self):
        loc='\n'.join(p.read_text(encoding='utf-8-sig') for p in (ROOT/'mod/localisation/simp_chinese').glob('*.yml'))
        for tag in ['SVN','NVN','KHM','PKS','FNL','DNM','RKH','HLC','MKG','BHD','PHQ']:
            tree=one(pdx.read(ROOT/f'mod/common/national_focus/v65_{tag}.txt'),'focus_tree')
            focuses=values(tree,'focus');self.assertGreaterEqual(len(focuses),19,tag)
            positions=[];descriptions=[];ids={one(f,'id') for f in focuses}
            for f in focuses:
                name=one(f,'id');x=int(one(f,'x'));y=int(one(f,'y'))
                for px,py in positions:self.assertTrue(y!=py or abs(x-px)>=5,(tag,name,'focus labels overlap'))
                positions.append((x,y))
                match=re.search(r'^\s*'+re.escape(name)+r'_desc:\d+ "(.+)"',loc,re.M)
                self.assertIsNotNone(match,name)
                descriptions.append(match[1])
                for prereq in values(f,'prerequisite'):
                    for parent in values(prereq,'focus'):self.assertIn(parent,ids,name)
            self.assertEqual(len(descriptions),len(set(descriptions)),tag)
    def test_playable_factions_have_real_territory(self):
        tags=(ROOT/'mod/common/country_tags/v65.txt').read_text(encoding='utf-8-sig')
        bookmark=(ROOT/'mod/common/bookmarks/v65.txt').read_text(encoding='utf-8-sig')
        states='\n'.join(p.read_text(encoding='utf-8-sig') for p in (ROOT/'mod/history/states').glob('*.txt'))
        for tag in ['SVN','NVN','KHM','PKS','FNL','DNM','RKH']:
            self.assertRegex(tags,rf'\b{tag}\s*=');self.assertRegex(bookmark,rf'\b{tag}\s*=')
            self.assertRegex(states,rf'owner\s*=\s*{tag}')
            self.assertTrue((ROOT/f'mod/history/units/{tag}_1965.txt').exists())
    def test_coup_requires_battlefield_defeat(self):
        trigger=ROOT/'mod/common/scripted_triggers/v65_campaign.txt'
        self.assertTrue(trigger.exists(),'No battlefield defeat trigger exists')
        effects=(ROOT/'mod/common/scripted_effects/v65_politics.txt').read_text(encoding='utf-8-sig')
        self.assertIn('v65_front_has_collapsed',effects)
        decisions=(ROOT/'mod/common/decisions/v65_politics.txt').read_text(encoding='utf-8-sig')
        self.assertIn('has_country_flag = v65_front_defeat',decisions)

if __name__=='__main__':unittest.main()
