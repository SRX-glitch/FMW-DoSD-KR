#!/usr/bin/env bash
# Rebuild "FMWCB 1.2.4.2 (ported to game 1.2.6) + Korean patch 261030 + Korean mod translation + our mods" from scratch.
# inputs : orig_en/data.win      Steam EN 1.2.4 (SHA1 24605c59…)  — base the FMWCB xdelta was made for
#          orig_en_new/data.win  Steam EN 1.2.6 (SHA1 f358278b…)  — what users have now (patch source)
#          orig_en_game/         EN 1.2.4 data/ meta/ (10 blobs + 5 metas unchanged in 1.2.6)
#          orig_en_new_game/     EN 1.2.6 data4 blob (cd1075…) + data4.meta (1.2.6 fixed English quotes there)
#          kr_src_261030/        KR patch 261030 (data.win + data/ + meta/)
#          mods_src_1242/fmw_patches-main/  FMWCB repo (1.2.4.2)
#          translate/*.json, translate/extra_mods/
# outputs: build/data126_final.win, build/localappdata/{mods,experimental_mods,addOns}, ../패치파일/<PKG>.zip
set -euo pipefail
cd "$(dirname "$0")"
UTMT="../../../../tools_ext/utmt_cli/UndertaleModCli.exe"
export FMW_W="$(cygpath -w "$PWD")"
MODSRC=mods_src_1242/fmw_patches-main
XD=$MODSRC/1.2.4.x/ENG/FMWCB-1.2.4.2.xdelta
PKG=FMWCB-1.2.4.2_KR_1.2.6_xdelta
ut() { "$UTMT" load "$1" -s "$2" -o "$3" -f < /dev/null | grep -v '^\[MESSAGE\]' || true; test -s "$3"; }

# 1) FMWCB 1.2.4.2 on EN 1.2.4 (adler32-checked)
python -X utf8 tools/vcdiff.py "$XD" orig_en/data.win build/data_mod1242_en124.win

# 2) port the 1.2.6 game update onto the mod: 3-way merge of the 15 updated scripts
RX="$(cat survey/upd_rx.txt)"
for pair in "orig_en/data.win:upd_en4" "orig_en_new/data.win:upd_en6" "build/data_mod1242_en124.win:upd_mod1242"; do
  rm -rf "survey/${pair#*:}"
  FMW_RX="$RX" FMW_OUT="${pair#*:}" "$UTMT" load "${pair%%:*}" -s tools/utmt/decomp.csx < /dev/null > /dev/null
done
rm -rf survey/merge126b && mkdir -p survey/merge126b
for f in survey/upd_en6/*.gml; do
  b=$(basename "$f")
  git merge-file -p "survey/upd_mod1242/$b" "survey/upd_en4/$b" "$f" > "survey/merge126b/$b" || true   # conflicts -> resolve_126
done
python -X utf8 tools/resolve_126.py                     # asserts no conflict markers remain
ut build/data_mod1242_en124.win tools/utmt/port126.csx build/data_mod1242_126.win

# 3) Korean patch 261030 (diff vs EN 1.2.6) merged into the mod
python -X utf8 - <<'EOF'
import sys, json; sys.path.insert(0, 'tools')
from verify_merge import dis
_, E = dis('orig_en_new/data.win'); _, K = dis('kr_src_261030/data.win')
kr = [n for n in E if E[n] != K[n]]
json.dump({'kr': kr, 'kr_logic': ['gml_GlobalScript_UI_status_weapon', 'gml_Object_ObjResult_Create_0'], 'kr_new': [n for n in K if n not in E]},
          open('survey/kr261030_scope.json', 'w'), indent=1)
EOF
export FMW_KR=kr_src_261030/data.win FMW_EN=orig_en_new/data.win FMW_SCOPE=survey/kr261030_scope.json FMW_MODBASE=build/data_mod1242_126.win
ut build/data_mod1242_126.win tools/utmt/merge_kr.csx build/data126_kr.win
python -X utf8 tools/verify_merge.py build/data126_kr.win  # gate: bad=0 missingKR=0

# 4) mod UI translation + our own mods (each a toggle in the mod settings window, default as in translate/extra_mods)
ut build/data126_kr.win           tools/utmt/apply_ko.csx    build/data126_kr_ko.win
ut build/data126_kr_ko.win        tools/utmt/apply_ng.csx    build/data126_kr_ko_ng.win       # NGUnitCount
ut build/data126_kr_ko_ng.win     tools/utmt/apply_bgm.csx   build/data126_kr_ko_ng_bgm.win   # BGMLoopFix
ut build/data126_kr_ko_ng_bgm.win tools/utmt/apply_trust.csx build/data126_final.win          # CombinedTrust
FMW_MODSRC=$MODSRC python -X utf8 translate/apply_json.py                                    # gate: untranslated / desc overlap
sha1sum build/data126_final.win

# 5) distribution package: per-file xdelta against the EN 1.2.6 originals
XD3="${XD3:-xdelta3}"; D=build/$PKG
rm -rf "$D"; mkdir -p "$D/patch/data" "$D/patch/meta" "$D/LocalAppData_fmw_dosd"
src() { if [ -e "orig_en_new_game/$1" ]; then echo "orig_en_new_game/$1"; else echo "orig_en_game/$1"; fi; }
"$XD3" -e -9 -f -S none -B 67108864 -s orig_en_new/data.win build/data126_final.win "$D/patch/data.win.xdelta"
for f in $(ls kr_src_261030/data); do "$XD3" -e -9 -f -S none -B 67108864 -s "$(src data/$f)" kr_src_261030/data/$f "$D/patch/data/$f.xdelta"; done
for f in $(ls kr_src_261030/meta); do "$XD3" -e -9 -f -S none -s "$(src meta/$f)" kr_src_261030/meta/$f "$D/patch/meta/$f.xdelta"; done
cp -r build/localappdata/mods build/localappdata/addOns "$D/LocalAppData_fmw_dosd/"
cp -r build/localappdata/experimental_mods "$D/experimental_mods(선택)"
cp packaging/{install.bat,restore.bat} "$D/"
sed -e "s/@SHA@/$(sha1sum build/data126_final.win | cut -c1-40)/" \
    -e "s/@MODS@/$(find build/localappdata/mods -name '*.json' | wc -l)/" \
    -e "s/@ADDONS@/$(find build/localappdata/addOns -name '*.json' | wc -l)/" packaging/README.txt > "$D/README.txt"
mkdir -p "$D/xdelta" && cp "${XDUI:?XDUI=xdeltaUI.zip 푼 폴더}"/{xdelta.exe,xdeltaUI.exe} "$D/xdelta/" && cp "$XDUI/readme.txt" "$D/xdelta/xdeltaUI_readme.txt"
cp $MODSRC/LICENSE "$D/LICENSE_fmw_patches(MIT).txt"
(cd "$D" && find . -type f ! -name SHA1SUMS.txt -print0 | sort -z | xargs -0 sha1sum > SHA1SUMS.txt)
rm -f ../패치파일/$PKG.zip
powershell -NoProfile -Command "Compress-Archive -Path '$D\*' -DestinationPath '../패치파일/$PKG.zip'"
