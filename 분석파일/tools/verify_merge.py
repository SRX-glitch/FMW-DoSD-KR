"""Gate: merged data.win vs MOD (code must differ only in push.s of KR-changed scripts) and vs KR (logic scripts identical)."""
import sys, re, json, os
sys.path.insert(0, os.path.dirname(__file__)); import gmdis

def dis(p):
    D = gmdis.Data(p); r = {}
    for e in D.code_entries():
        if e['off']: continue
        L = [re.sub(r'^L\w+\s+', '', l) for l in D.dis(e['blob'], e['len'])]
        L = [('push.i <owner>' if i+1 < len(L) and 'setowner' in L[i+1] and l.startswith('push.i') else l) for i, l in enumerate(L)]
        L = [re.sub(r'^(b|bt|bf|pushenv|popenv)(\s+)L\w+', r'\1\2L?', l) for l in L]
        r[e['name']] = L
    return D, r

merged = sys.argv[1] if len(sys.argv) > 1 else 'build/data_mod_kr.win'
_, M = dis('build/data_mod_en.win'); _, K = dis('orig/data.win'); _, X = dis(merged)
scope = json.load(open('survey/merge_scope.json'))
logic = {'gml_GlobalScript_UI_status_weapon', 'gml_Object_ObjResult_Create_0'}
bad = 0; strdiff = 0
assert set(M) == set(X), (set(M) ^ set(X))
for n in M:
    if n in logic:
        if X[n] != K[n]: print('LOGIC != KR', n); bad += 1
        continue
    if X[n] == M[n]: continue
    if len(X[n]) != len(M[n]): print('LEN', n); bad += 1; continue
    d = [(a, b) for a, b in zip(M[n], X[n]) if a != b]
    if any(not (a.startswith('push.s') and b.startswith('push.s')) for a, b in d) or n not in scope['kr']:
        print('NON-STRING DIFF', n, d[:3]); bad += 1
    strdiff += len(d)
# every KR string change must be present in merged
miss = 0
for n in scope['kr']:
    if n in logic: continue
    kr_only = [l for l in K[n] if l.startswith('push.s')] 
    xs = set(l for l in X[n] if l.startswith('push.s'))
    for l in set(kr_only) - set(l for l in (dis.__defaults__ or []) ):
        if re.search('[가-힣]', l) and l not in xs: print('MISSING KR', n, l); miss += 1
print(f'scripts={len(X)} string-lines changed={strdiff} bad={bad} missingKR={miss}')
