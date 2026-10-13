"""2026-10-13 mod description audit fixes (code-verified against survey/mod_all_gml)."""
import json
p = 'translate/ko_desc.json'
d = json.load(open(p, encoding='utf8'))
fix = {
    # UI_NG_draw: only widens the candidate list; the 6-unit cap (UI_NG_list) is unchanged; Korin/Seirensen/FMW4Youmu stay excluded
    "EnableAllUnitsNG+.json":
        "주회 플레이에서 데려갈 유닛 후보에\n"
        "상하이·호라이·젠키·고키·아큐·메코·마쿠라·\n"
        "요정·프리즘리버 자매를 추가합니다.\n"
        "(데려갈 수 있는 인원은 6명 그대로)\n"
        "새 후보를 표시하려면\n"
        "주회 유닛 인계 화면을 다시 불러오세요.",
    # icon_finalize: geki >= 50 -> +5, ACE #1 -> +5 (independent, stack)
    "AceKillBonus.json":
        "출격 시 초기 파워 보너스를 되살립니다.\n"
        "- 격추수 50 이상: 파워 +5\n"
        "- 에이스 1위: 파워 +5 (둘 다면 +10)",
    # im_initialize: global.isTest && debugFlagReset
    "ResetEventFlags.json":
        "인터미션을 저장하고 다시 불러올 때마다\n"
        "챕터별 이벤트 플래그를 초기화하고\n"
        "참(true)으로 설정합니다.\n"
        "디버그 메뉴(EnableDebugMenu)가 켜져 있을 때만 작동합니다.\n\n"
        "경고: 필드 아큐/릴리 블랙/클래식 레이무·마리사처럼\n"
        "특정 이벤트 플래그로 얻는 캐릭터가\n"
        "로스터에서 제거됩니다.\n"
        "챕터별 이벤트 플래그를 시험할 때는\n"
        "주의해서 사용하세요.",
    # sound_load_loop: built-in names load from the archive; LayeredFS only needed for user-added songs (modData/data6-4)
    "ChangeIntermissionBGM.json":
        "인터미션에서 재생되는 BGM을 바꿉니다.\n"
        "루프 지점을 뺀 곡의 내부 이름을 입력하세요.\n"
        "BGM 변경은 세이브를 다시 불러와야 적용됩니다.\n"
        "직접 추가한 곡을 쓰려면 EnableLayeredFS 모드가\n"
        "켜져 있어야 합니다.\n\n"
        "(기본 내부 이름: bgm_gen_intermission2)",
    # draw_unitmenu compares against the KR menu label 「풀파워모드」
    "DisplayFPMTextColor.json":
        "유닛 메뉴의 「풀파워모드」 글자색을\n"
        "되살립니다.",
    # chat_get_cursor_pos [TEAM_NAME] + st_ADV_71Common default/save
    "ChangeArmyName.json":
        "대사에 나오는 부대 이름을 바꿉니다.\n"
        "71화의 부대 이름 입력에서도 기본값으로 쓰이고,\n"
        "거기서 입력한 이름이 여기에 저장됩니다.\n"
        "(기본값: \"환상소녀대전대\")",
}
for k, v in fix.items():
    assert k in d, k
    d[k] = v
json.dump(d, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print('updated', len(fix))
