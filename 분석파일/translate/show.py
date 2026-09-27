import sys
mode = sys.argv[1]
for i, l in enumerate(open('translate/worksheet_en.tsv', encoding='utf8').read().split('\n')):
    k, s, e = l.split('\t')
    isd = k.startswith('addon.dialog')
    if (mode == 'dialog') == isd:
        print(i, k, '|', s.replace(chr(92), '/').split('/')[-1], '|', e)
