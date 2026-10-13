"""Update only the Desc field of installed mod JSONs (%LOCALAPPDATA%/fmw_dosd/mods), keeping the user's Value."""
import json, glob, os
src = 'build/localappdata/mods'
dst = os.path.join(os.environ['LOCALAPPDATA'], 'fmw_dosd', 'mods')
n = 0
for f in glob.glob(src + '/**/*.json', recursive=True):
    rel = os.path.relpath(f, src)
    t = os.path.join(dst, rel)
    if not os.path.exists(t):
        continue
    new = json.load(open(f, encoding='utf8'))
    cur = json.load(open(t, encoding='utf8'))
    if cur.get('Desc') != new['Desc']:
        cur['Desc'] = new['Desc']
        with open(t, 'w', encoding='utf8', newline='') as fh:
            fh.write(json.dumps(cur, ensure_ascii=False, separators=(',', ':')))
        n += 1
        print('updated', rel)
print(n, 'files')
