#!/usr/bin/env bash
# Rebuild "FMWCB mod + Korean patch + Korean mod translation" from scratch.
# inputs : orig_en/data.win (Steam EN 1.2.4, SHA1 24605c59…), orig/data.win (KR patch data.win),
#          kr_src/ (KR patch zip), mods_src/fmw_patches-main/ (FMWCB repo zip), translate/*.json
# outputs: build/data_mod_kr_ko.win, build/localappdata/{mods,experimental_mods,addOns}
set -euo pipefail
cd "$(dirname "$0")"
UTMT="../../../../tools_ext/utmt_cli/UndertaleModCli.exe"
export FMW_W="$(cygpath -w "$PWD")"
XD=mods_src/fmw_patches-main/1.2.4.x/FMWCB-1.2.4.1.xdelta

python -X utf8 tools/vcdiff.py "$XD" orig_en/data.win build/data_mod_en.win          # adler32-checked
python -X utf8 - <<'EOF'                                                               # scope: scripts the KR patch changed
import sys, re, json; sys.path.insert(0, 'tools')
from verify_merge import dis
_, E = dis('orig_en/data.win'); _, K = dis('orig/data.win'); _, M = dis('build/data_mod_en.win')
kr = [n for n in E if E[n] != K[n]]; mod = [n for n in M if n not in E or E[n] != M[n]]
json.dump({'kr': kr, 'mod': mod, 'both': [n for n in kr if n in mod]}, open('survey/merge_scope.json', 'w'), indent=1)
EOF
"$UTMT" load build/data_mod_en.win -s tools/utmt/merge_kr.csx -o build/data_mod_kr.win -f < /dev/null
python -X utf8 tools/verify_merge.py build/data_mod_kr.win
"$UTMT" load build/data_mod_kr.win -s tools/utmt/apply_ko.csx -o build/data_mod_kr_ko.win -f < /dev/null
python -X utf8 translate/apply_json.py
sha1sum build/data_mod_kr_ko.win

# ---- 배포 패키지 (영어 원본 기준 파일별 xdelta) ----
XD3="${XD3:-xdelta3}"; D=build/FMWCB-1.2.4.1_KR_xdelta
rm -rf "$D"; mkdir -p "$D/patch/data" "$D/patch/meta" "$D/LocalAppData_fmw_dosd"
"$XD3" -e -9 -f -S none -B 67108864 -s orig_en/data.win build/data_mod_kr_ko.win "$D/patch/data.win.xdelta"
for f in $(ls kr_src/data); do "$XD3" -e -9 -f -S none -B 67108864 -s orig_en_game/data/$f kr_src/data/$f "$D/patch/data/$f.xdelta"; done
for f in $(ls kr_src/meta); do "$XD3" -e -9 -f -S none -s orig_en_game/meta/$f kr_src/meta/$f "$D/patch/meta/$f.xdelta"; done
cp -r build/localappdata/mods build/localappdata/addOns "$D/LocalAppData_fmw_dosd/"
cp -r build/localappdata/experimental_mods "$D/experimental_mods(선택)"
cp packaging/{install.bat,restore.bat,README.txt} "$D/"
mkdir -p "$D/xdelta" && cp "${XDUI:?XDUI=xdeltaUI.zip 푼 폴더}"/{xdelta.exe,xdeltaUI.exe} "$D/xdelta/" && cp "$XDUI/readme.txt" "$D/xdelta/xdeltaUI_readme.txt"
cp mods_src/fmw_patches-main/LICENSE "$D/LICENSE_fmw_patches(MIT).txt"
(cd "$D" && find . -type f ! -name SHA1SUMS.txt -print0 | sort -z | xargs -0 sha1sum > SHA1SUMS.txt)
rm -f ../패치파일/FMWCB-1.2.4.1_KR_xdelta.zip
powershell -NoProfile -Command "Compress-Archive -Path '$D\*' -DestinationPath '../패치파일/FMWCB-1.2.4.1_KR_xdelta.zip'"
