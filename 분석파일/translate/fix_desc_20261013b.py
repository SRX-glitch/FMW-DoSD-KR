"""2026-10-13 follow-up: KR unit names (data_unit_all NameShort) and line-length split."""
import json
p = 'translate/ko_desc.json'
d = json.load(open(p, encoding='utf8'))
d["EnableAllUnitsNG+.json"] = d["EnableAllUnitsNG+.json"].replace(
    "요정·프리즘리버 자매를 추가합니다.", "삼요정·프리즘리버 세자매를 추가합니다.")
d["ResetEventFlags.json"] = d["ResetEventFlags.json"].replace(
    "디버그 메뉴(EnableDebugMenu)가 켜져 있을 때만 작동합니다.",
    "디버그 메뉴(EnableDebugMenu)가\n켜져 있을 때만 작동합니다.")
json.dump(d, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print(d["EnableAllUnitsNG+.json"])
