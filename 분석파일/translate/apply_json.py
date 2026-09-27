"""Write translated copies of the mod's JSON folders (mods/, experimental_mods/, addOns/) into build/localappdata/.
Files stay single-line compact UTF-8 (the game reads them with file_text_read_string)."""
import json, os, glob, re, shutil
S = 'mods_src/fmw_patches-main/'
OUT = 'build/localappdata/'
desc = json.load(open('translate/ko_desc.json', encoding='utf8'))
text = json.load(open('translate/ko_text.json', encoding='utf8'))
ws = {r['en']: r['ko'] for r in json.load(open('translate/worksheet.json', encoding='utf8')) if r['ko']}
TEXTKEYS = {'Dialog', 'Name', 'Text', 'VAL3', 'Special', 'NameShort', 'Name1', 'Name2'}
KEEP = {'String', 'Number', 'MEL', 'Reimu', '------', '-----'}   # template placeholders in disabled entries
VALUES = {'ChangeArmyName.json': '환상소녀대전대'}
miss, done = [], 0


def dump(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf8', newline='') as f:
        f.write(json.dumps(obj, ensure_ascii=False, separators=(',', ':')))


if os.path.isdir(OUT): shutil.rmtree(OUT)
for sub in ('mods', 'experimental_mods'):
    for f in glob.glob(S + sub + '/**/*.json', recursive=True):
        j = json.load(open(f, encoding='utf8'))
        b = os.path.basename(f)
        if b in desc: j['Desc'] = desc[b]; done += 1
        else: miss.append(f)
        if b in VALUES: j['Value'] = VALUES[b]
        dump(j, OUT + os.path.relpath(f, S).replace(os.sep, '/'))

for f in glob.glob(S + 'addOns/**/*.json', recursive=True):
    j = json.load(open(f, encoding='utf8'))
    for top, v in j.items():
        for a in v.get('AddOn', []):
            for k, x in list(a.items()):
                if k in TEXTKEYS and isinstance(x, str) and re.search('[A-Za-z]', x) and x not in KEEP:
                    ko = text.get(x) or ws.get(x)
                    if ko: a[k] = ko; done += 1
                    else: miss.append(f'{f}:{k}:{x!r}')
    dump(j, OUT + os.path.relpath(f, S).replace(os.sep, '/'))

print('translated fields', done)
print('untranslated', len(miss))
for m in miss: print('  ', m)
