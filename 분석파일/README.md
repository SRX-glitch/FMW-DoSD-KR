# FMW-DoSD-KR

환상소녀대전 DoSD(Fantasy Maiden Wars – Dream of the Stray Dreamer, Steam)에
**한글패치 260529 + 커뮤니티 모드 FMWCB 1.2.4.1**을 병합하고 모드 부분을 한글화하는 빌드 도구.

분석 정본: `docs/분석보고서.md` (원본: `실험실/rom/분석보고서/환상소녀대전_분석보고서.md`)

## 빌드 입력 (저장소에 없음 — 각자 준비)
| 경로 | 내용 |
|---|---|
| `orig_en/data.win` | Steam 영어판 1.2.4 (SHA1 24605c59ae42baef78762adecdc315174f39f277) |
| `orig/data.win`, `kr_src/` | 한글패치 fmw_korean_260529 (data.win SHA1 6a713d38…) |
| `mods_src/fmw_patches-main/` | FMW-HUB fmw_patches (MIT) |
| UndertaleModTool CLI 0.9.2.0 | `../../../tools_ext/utmt_cli/` |

```bash
bash build_all.sh     # → build/data_mod_kr_ko.win (SHA1 f918ec6b…), build/localappdata/
```

## 구성
- `tools/gmdis.py` — GameMaker 바이트코드 17 디스어셈블러
- `tools/gmcrypt.py` — meta 암호(`buffer_encode_ext`) 이식
- `tools/gswa.py` — GSWA 아카이브 리더(meta/data 추출)
- `tools/vcdiff.py` — VCDIFF(xdelta3) 디코더, adler32 검증
- `tools/utmt/merge_kr.csx` — 모드판 data.win에 한글패치(폰트·텍스처·문자열·로직 2곳) 이식
- `tools/utmt/apply_ko.csx` — 모드 추가 문자열 한글화(`translate/ko_code.json`)
- `tools/verify_merge.py` — 병합 게이트(문자열 외 차이 0)
- `translate/` — 모드 번역 원본(`ko_code.json`, `ko_desc.json`, `ko_text.json`) + JSON 적용기

## 크레딧
- 한글패치: 한글패치 제작진 (병합 배포 허가 받음, 2026-09-27)
- fmw_patches © 2026 FMW-HUB, MIT License
