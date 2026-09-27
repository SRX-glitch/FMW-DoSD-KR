"""Collect translatable mod texts (mods/*.json Desc, addOns text fields) -> translate/worksheet.json"""
import json, glob, re, os
S = 'mods_src/fmw_patches-main/'
TEXTKEYS = {'Dialog', 'Name', 'Text', 'VAL3', 'Special', 'NameShort', 'Name1', 'Name2'}
rows, seen = [], set()


def add(kind, src, en):
    if not isinstance(en, str) or not re.search('[A-Za-z]', en) or (kind, en) in seen:
        return
    seen.add((kind, en))
    rows.append({'kind': kind, 'src': src.replace(os.sep, '/'), 'en': en, 'ko': ''})


for f in sorted(glob.glob(S + 'mods/**/*.json', recursive=True) + glob.glob(S + 'experimental_mods/**/*.json', recursive=True)):
    add('desc', os.path.relpath(f, S), json.load(open(f, encoding='utf8')).get('Desc'))
for f in sorted(glob.glob(S + 'addOns/**/*.json', recursive=True)):
    for top, v in json.load(open(f, encoding='utf8')).items():
        for a in v.get('AddOn', []):
            for k, x in a.items():
                if k in TEXTKEYS:
                    add(top.split('_')[0] + '.' + k, os.path.relpath(f, S + 'addOns'), x)

if __name__ == '__main__':
    old = {}
    if os.path.exists('translate/worksheet.json'):
        old = {(r['kind'], r['en']): r['ko'] for r in json.load(open('translate/worksheet.json', encoding='utf8'))}
    for r in rows: r['ko'] = old.get((r['kind'], r['en']), '')
    json.dump(rows, open('translate/worksheet.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    print(len(rows))
