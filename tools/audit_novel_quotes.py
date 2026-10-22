"""Optional local check against a user-supplied novel; no source book is stored."""
import argparse,ast,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]

def normalize(s):return re.sub(r'\s+','',s).strip('\u201c\u201d')

def audit(book):
    text=normalize(book.read_text(encoding='utf-8-sig'))
    tree=ast.parse((R/'tools/build_chapter_focus.py').read_text(encoding='utf-8'))
    data={n.targets[0].id:ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ['ROUTES','EVENTS']}
    rows=[(x[0],x[2]) for r in data['ROUTES'].values() for x in r['focuses']]
    rows += [(str(k),v['desc']) for k,v in data['EVENTS'].items()]
    catalog=json.loads((R/'data/novel-source-passages.json').read_text(encoding='utf-8'))
    rows += [(p['id'],p['quote']) for p in catalog['passages']]
    guests=ast.parse((R/'tools/build_guest_stories.py').read_text(encoding='utf-8'))
    guest_sources=next(ast.literal_eval(n.value) for n in guests.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='STORY_SOURCES')
    rows += [('guest_'+str(k),v[2]) for k,v in guest_sources.items()]
    bad=[]
    for key,quote in rows:
        s=normalize(quote)
        if s not in text:
            i=text.find(s[:20])
            bad.append({'key':key,'excerpt':s,'original_near_start':text[max(i,0):max(i,0)+len(s)+50] if i>=0 else ''})
    return {'checked':len(rows),'mismatches':bad}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('book',type=Path);args=parser.parse_args()
    result=audit(args.book)
    dest=R/'runtime/test-results/novel-quote-audit.json';dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Quote audit:',result['checked'],'checked;',len(result['mismatches']),'mismatches')
    print('Mismatched keys:',[x['key'] for x in result['mismatches']])
    raise SystemExit(bool(result['mismatches']))
