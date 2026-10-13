"""Mod settings window draws the ON/OFF / value box over description lines 10-11 (index 9, 10).
The original EN descriptions all keep those lines blank; re-align the KO ones."""
import json

p = 'translate/ko_desc.json'
d = json.load(open(p, encoding='utf8'))


def push_past_box(s):
    """content that starts at line 11 after blank line 10 -> add one blank so it starts at line 12."""
    L = s.split('\n')
    if len(L) > 10 and not L[9].strip() and L[10].strip():
        L.insert(10, '')
    return '\n'.join(L)


for k in ("FMW4SongMechanics.json", "RestoreRevengeStorage.json", "ChangeSpellColor.json"):
    d[k] = push_past_box(d[k])

d["ResetEventFlags.json"] = (
    "인터미션을 저장하고 다시 불러올 때마다\n"
    "챕터별 이벤트 플래그를 초기화하고 참으로 설정합니다.\n"
    "디버그 메뉴(EnableDebugMenu)가\n"
    "켜져 있어야 작동합니다.\n"
    "\n"
    "경고: 필드 아큐/릴리 블랙/클래식 레이무·마리사처럼\n"
    "특정 이벤트 플래그로 얻는 캐릭터가 로스터에서\n"
    "제거됩니다. 이벤트 플래그를 시험할 때만\n"
    "주의해서 사용하세요.")
json.dump(d, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0)

q = 'translate/extra_mods/Modifiers/NGUnitCount.json'
j = json.load(open(q, encoding='utf8'))
j['Desc'] = (
    "주회 플레이(드림 모드)에서 데려갈 수 있는\n"
    "유닛 수의 상한을 바꿉니다. (최소:0, 최대:99)\n"
    "- 6: 기본값 (원래 게임과 같은 상한)\n"
    "- 0: 제한 없음\n"
    "1명 이상 고르면 다음으로 진행할 수 있습니다.\n"
    "7명 이상이면 선택한 유닛이 두 줄로 표시됩니다.\n"
    "편성에 따라 일부 보너스 조건을\n"
    "달성할 수 없게 될 수 있습니다.\n"
    "(한글판 통합 패치에서 추가한 항목)")
with open(q, 'w', encoding='utf8', newline='') as f:
    f.write(json.dumps(j, ensure_ascii=False, separators=(',', ':')))
print('ok')
