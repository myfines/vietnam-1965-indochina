"""Keep focus widgets and the continuous-focus panel in separate regions."""
from pathlib import Path
import sys,json
from build_campaign import M,R
sys.path.insert(0,str(R/'vendor'))
import pdx

report={}
for path in sorted((M/'common/national_focus').glob('v65_*.txt')):
    blocks=pdx.read(path)
    for kind,_,tree in blocks:
        if kind!='focus_tree':continue
        nodes=[n for k,_,n in tree if k=='focus']
        positions=[]
        for node in nodes:
            d=dict((k,v) for k,_,v in node)
            positions.append(dict(id=d['id'],x=float(d.get('x',0)),y=float(d.get('y',0))))
        # Coordinates for continuous_focus_position are pixels, focus x/y are grid units.
        # The old y=1500 put this large panel on top of branches around rows 10–14.
        panel_y=int(max(n['y'] for n in positions)*130+500)
        tree[:]=[(k,o,v) for k,o,v in tree if k!='continuous_focus_position']
        tree.append(('continuous_focus_position','=',pdx.parse(f'x = 0 y = {panel_y}')))
        collisions=[]
        for i,a in enumerate(positions):
            for b in positions[i+1:]:
                if abs(a['x']-b['x'])<2 and abs(a['y']-b['y'])<1.5:
                    collisions.append([a['id'],b['id']])
        if collisions:raise ValueError(f'{path.name}: overlapping focus widgets {collisions}')
        report[path.stem]=dict(nodes=positions,continuous_panel_y=panel_y,collisions=collisions)
    path.write_text(pdx.dump(blocks),encoding='utf-8')
(R/'focus-layout-manifest.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Focus layout:',len(report),'trees; continuous panels below all nodes')
