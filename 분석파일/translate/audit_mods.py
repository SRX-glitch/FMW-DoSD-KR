"""For every mod toggle JSON: EN Desc, KO Desc, and the code that reads its global (optionalOf / global.<Name>)."""
import json, glob, os, re

S = 'mods_src/fmw_patches-main/'
ko = json.load(open('translate/ko_desc.json', encoding='utf8'))
gml = {os.path.basename(f)[:-4]: open(f, encoding='utf8').read().split('\n')
       for f in glob.glob('survey/mod_all_gml/*.gml')}
out = []
files = sorted(glob.glob(S + 'mods/**/*.json', recursive=True) + glob.glob(S + 'experimental_mods/**/*.json', recursive=True))
for f in files:
    j = json.load(open(f, encoding='utf8'))
    name = j['Name']; b = os.path.basename(f)
    out.append('=' * 100)
    out.append(f'{os.path.relpath(f, S)}  Name={name}  Type={j.get("Type")}  Value={j.get("Value")!r}')
    out.append('EN: ' + j['Desc'].replace('\n', ' / '))
    out.append('KO: ' + ko.get(b, '??').replace('\n', ' / '))
    pat = re.compile(r'optionalOf\("%s"|global\.%s\b|"%s"' % ((re.escape(name),) * 3))
    hits = 0
    for scr, lines in sorted(gml.items()):
        idx = [i for i, l in enumerate(lines) if pat.search(l)]
        if not idx: continue
        hits += len(idx)
        out.append(f'  -- {scr} ({len(idx)})')
        shown = set()
        for i in idx[:3]:
            for k in range(max(0, i - 2), min(len(lines), i + 9)):
                if k in shown: continue
                shown.add(k); out.append('     ' + lines[k][:150])
            out.append('     ...')
    out.append(f'  total refs: {hits}')
open('survey/mod_audit.txt', 'w', encoding='utf8').write('\n'.join(out))
print(len(files), 'mods')
