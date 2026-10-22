"""Guard source integrity and prevent silent localization of nonexistent keys."""
import hashlib,json,re,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]

class SourceTests(unittest.TestCase):
    def test_passage_hashes(self):
        passages=json.loads((R/'data/novel-source-passages.json').read_text(encoding='utf-8'))['passages']
        for p in passages:
            self.assertEqual(hashlib.sha256(p['quote'].encode()).hexdigest(),p['sha256'])
            self.assertGreaterEqual(p['chapter'],1)
            self.assertTrue(p['title'])

    def test_overrides_reference_existing_content(self):
        manifest=json.loads((R/'source-prose-manifest.json').read_text(encoding='utf-8'))
        keys={x['loc_key'] for x in manifest['mappings']}
        other=set()
        for p in (R/'mod/localisation').rglob('*.yml'):
            if p.as_posix().endswith(manifest['localization_file'].removeprefix('mod/')):continue
            other.update(re.findall(r'^\s*([^\s:]+):\d*\s',p.read_text(encoding='utf-8-sig'),re.M))
        self.assertFalse(keys-other,keys-other)

if __name__=='__main__':unittest.main()
