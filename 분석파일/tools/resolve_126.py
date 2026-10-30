"""Resolve the 1.2.6-update vs FMWCB-1.2.4.2 merge conflicts (survey/merge126b/*.gml, git merge-file output).

Policy: keep the mod's side, then re-add exactly what 1.2.6 added in that region.
  opt_loading / data_load_events : 1.2.6 only touched the legacy (non-new_ArXiv) branch -> add its "not found" guard there
  resource_load                  : 1.2.6 only changed a debug print in the archive branch -> mod side (debug only)
  unit_main_menu                 : 1.2.6 added check_wait(c_id, true) before redrawing the move tiles -> keep mod colour + add it
Also: launch_set_test keeps saves in %LOCALAPPDATA% (isInst true) instead of 1.2.6's game folder (user decision 2026-10-31).
"""
import re, glob, os, sys

D = 'survey/merge126b'
CONF = re.compile(r'<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n', re.S)


def ours(text):
    return CONF.sub(lambda m: m.group(1), text)


def edit(name, fn):
    p = os.path.join(D, f'gml_GlobalScript_{name}.gml')
    s = open(p, encoding='utf8').read()
    s2 = fn(s)
    assert '<<<<<<<' not in s2 and '>>>>>>>' not in s2, name
    open(p, 'w', encoding='utf8', newline='').write(s2)


def legacy_guard(tag, did, msg):
    def f(s):
        s = ours(s)
        old = f'var fname = GSWA_find(FileID, "{did}");\n'
        i = s.rindex(old)  # the legacy (non-new_ArXiv) branch is the LAST one; the first is the mod's LayeredFS probe
        ind = s[s.rfind('\n', 0, i) + 1:i]
        add = (f'{ind}if (fname == "")\n{ind}{{\n{ind}    print("{msg}", FileID, "not found");\n'
               f'{ind}    exit;\n{ind}}}\n')
        j = i + len(old)
        return s[:j] + add + s[j:]
    return f


edit('opt_loading', legacy_guard('opt', '5-3', 'otp_load_stage: stage file for'))
edit('data_load_events', legacy_guard('ev', '5-2', 'data_load_events_part: event data for'))
edit('resource_load', ours)


def main_menu(s):
    s = ours(s)
    old = '                    var default_color = colorOverride("unitTileColor", "233,33,33");\n'
    assert s.count(old) >= 1
    # only the hunk that conflicted: the one 1.2.6 prefixed with check_wait (first occurrence after isLoaded reset)
    k = s.index('c_id.y = orig_y;')
    i = s.index(old, k)
    return s[:i] + '                    check_wait(c_id, true);\n' + s[i:]


edit('unit_main_menu', main_menu)
edit('launch_set_test', lambda s: s.replace('global.isInst = 0;', 'global.isInst = true;', 1))

left = [f for f in glob.glob(D + '/*.gml') if '<<<<<<<' in open(f, encoding='utf8').read()]
print('remaining conflicts:', left)
