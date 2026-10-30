"""Korean Desc for the 27 JSON mods added in FMWCB 1.2.4.2 (CHANGELOG 1.2.4.2 + mod JSON Desc).
Lines 10-11 stay blank: the settings window draws the ON/OFF / value box there (apply_json.py gate)."""
import json

D = {
    'SEAMFix.json':
        '정신커맨드 검색에서 후위 유닛의 정신커맨드 메뉴로\n들어갈 때 전위 유닛 포인터를 안전하게 처리해\n'
        '「낡은 개체 공격 조작(SEAM)」 버그를 고칩니다.\n'
        '(후위 유닛이 전위에 복제되어\n전투 정보 화면에 들어가는 버그)',
    'DisableDebugAutoLeveling.json':
        '이미 부대에 있는 캐릭터의 자동 레벨업을 끕니다.\n'
        '일반 진행, 디버그 메뉴의 스테이지 선택으로\n챕터를 넘길 때, 디버그 메뉴를 켠 채\n세이브를 불러올 때 모두 해당됩니다.\n\n'
        '새로 합류한 캐릭터는 지금까지처럼\n해당 챕터 번호에 맞춰 자동 레벨업됩니다.',
    'EnableAnimationPauser.json':
        '전투 애니메이션 일시정지 기능을 켭니다.\n전투 애니메이션을 원하는 때에 멈추고\n원하는 만큼 진행시킬 수 있습니다.\n\n'
        '주의: 멈춰 있는 동안 게임 창이\n응답 없음처럼 보입니다(대기 루프 사용).\n'
        '창이 비활성이어도 키 입력은 적용됩니다.\n\n\n\n\n'
        '키보드 조작:\nP - 일시정지\nO - 일시정지 해제\n아래 방향키 - 누르는 동안 진행\n'
        '위/오른쪽 방향키 - 번갈아 눌러 1프레임씩\n왼쪽 방향키 - 60FPS로 진행',
    'QuickArcEndingSkip.json':
        '장 엔딩 연출 중의 챕터 요약을 건너뜁니다.\n\n켜 두면 A 버튼으로\n장 엔딩 연출을 넘길 수 있습니다.',
    'ChangeMaxSaves.json':
        '게임이 세이브 폴더에서 찾는\n최대 세이브 수를 바꿉니다.\n'
        '바꾼 값은 게임을 다시 시작해야 적용됩니다.\n(4 = 기본 최대 200개)\n\n'
        '많이 늘릴수록 시작할 때 로딩이 길어집니다.\n최소:4, 최대:1000',
    'ChangeSaveLocation.json':
        '게임이 세이브를 찾고 읽는 폴더를 바꿉니다.\n'
        '바꾼 값은 게임을 다시 시작해야 적용됩니다.\n(기본값: savedata/)\n\n'
        'GMS 샌드박스 때문에 세이브 폴더는\nAPPDATA/fmw_dosd 폴더 안에 있어야\n쓰기가 가능합니다.\n'
        '끝에 / 를 붙여 폴더로 지정하세요.',
    'AverageTeamUpAtkUpgrades.json':
        '합체 공격의 무기 강화 수치를\n참가 유닛 수로 나눈 평균으로 계산합니다.\n(원작 CB/FMW 방식)\n\n'
        '예: 레이무의 무기 강화가 6단계일 때\n2인 합체 공격인 「삼색연화접」은\n6/2=3단계 분량만 강화가 적용됩니다.',
    'BacklineReAttack.json':
        '타임 패러독스/재공격이\n후위에서도 발동하게 합니다.\n(원작 FMW3 1.0.4 이전의 동작)',
    'RestoreBacklineAllOutShootout.json':
        '레이센의 「전탄발사」 버프가\n후위에서도 지속되고 탄수를 아끼는\n원작 FMW4의 발동 조건을 복원합니다.',
    'RestoreGameOvers.json':
        '챕터를 다시 시작할 때마다\n게임오버 횟수가 0으로 초기화되지 않게 해\n챕터 전체의 게임오버 횟수를 기록합니다.',
    'RestoreOldWPConditions.json':
        '챕터 보너스 조건을 달성하면\n점수 10000 대신 WP +5를 주는\n원작의 보상으로 되돌립니다.\n'
        '이 모드를 켜면 스테이지 클리어 기본 보상은\nWP +10이 됩니다.\n\n'
        '게임오버 기록 복원 모드도 켜 두면\n게임오버를 1번이라도 한 챕터는\nWP를 얻지 못합니다.\n\n\n'
        '보너스 달성 메시지를 고치려면\ndata5-4/Data_Text의 Restore_WPMessage\naddOn의 Active를 true로 하세요.',
    'DisableStrictPSChecking.json':
        '일부 개인 스킬 효과를 8번째 스킬 칸에서만\n확인하는 내부 처리를 끕니다.\n\n'
        '해당 개인 스킬을 일반 스킬 칸에 넣어도\n효과가 적용됩니다.',
    'DisableUnitCharUpdates.json':
        '내부 Data_Updates 파일에 따라\n유닛/캐릭터 버전을 갱신하는 처리를 끕니다.\n'
        '(현재 챕터까지 챕터별 기록을 차례로 적용)\n\n'
        '갱신이 꺼지므로 성능을 바꾸려면\n세이브의 UnitID/CharID를\n직접 수정해야 합니다.',
    'EnforceCappedUnitUpgrades.json':
        '각 장의 유닛 강화 상한을\n주회 플레이에서도 적용합니다.\n\n'
        '장별 유닛 강화 상한:\n홍의 장: 5단계\n요의 장: 5단계\n영의 장: 7단계\n최종장: 10단계',
    'ForceRouteBFlag.json':
        '챕터 전환 판정을 건너뛰어\n70화 클리어 후 항상 루트 선택 이벤트로\n들어가게 합니다.\n'
        '첫 플레이에서도 루트 B로 갈 수 있습니다.\n\n'
        '아이템 배분과 점수/WP/PP 획득에\n영향이 있을 수 있으니 세이브를 백업하세요.',
    'FullyUnlockAllSpirits.json':
        '레벨/플래그 제한과 관계없이\n모든 캐릭터의 정신커맨드를 전부 해금합니다.\n\n'
        '바꾼 뒤 인터미션이나 세이브를 다시 불러오면\n유닛의 정신커맨드 목록이 갱신됩니다.\n'
        '정신커맨드 상태를 영구히 바꾸지 않으므로\n자유롭게 켜고 끌 수 있습니다.',
    'OverrideLevelCap.json':
        '캐릭터 레벨 상한을 덮어씁니다.\n(0 = 장별 기본 상한으로 되돌림)\n최소:0, 최대:99\n\n'
        '바꾼 값은 세이브를 다시 불러와야 적용됩니다.',
    'RestoreMemoriesStacking.json':
        '「요의 기억」 장비를 여러 개 장착해\nSP 소비를 줄이는 중첩 효과를 복원합니다.\n\n'
        '바꾼 뒤 장비를 바꾸거나 게임을 다시 불러오면\nSP 소비가 갱신됩니다.',
    'DisplayFriendshipBonus.json':
        '대미지 계산 화면에\n신뢰 시스템으로 인한\n주는/받는 대미지 보정을 표시합니다.',
    'ExpandedDamageStatus.json':
        '대미지 계산 화면에 메인·지원·원호 공격의\n계산을 모두 표시합니다.\n'
        '아군과 적 각각의 계산이\n여러 페이지로 나뉘어 표시됩니다.',
    'FinalDamageStatus.json':
        '대미지 계산 화면에\n예상 최종 대미지를 표시합니다.\n\n'
        '주의: 반응/크리티컬/파워 상승/정신커맨드 사용 등\n전투 중 변동이 반영되기 전의 값입니다.',
    'DisableIMIconSpriteAnim.json':
        '인터미션의 작은 유닛 아이콘이\n움직이는 애니메이션을 끕니다.',
    'DisableMapIconSpriteAnim.json':
        '챕터 맵에서 공중/땅 지형에 있는\n작은 유닛 아이콘의 움직이는 애니메이션을 끕니다.',
    'ObfuscateSpellCard.json':
        'MAP 병기의 스펠카드를 빨간색으로 표시하는\nCB의 변경을 되돌립니다.\n'
        '원작처럼 모든 스펠카드를\n파란색으로 표시합니다.',
    'RestoreExtraEndingStats.json':
        '엔딩 연출 중에 보너스 통계를 표시합니다.\n\n'
        '게임 중 여러 행동으로 이 통계를\n기록하는 처리도 함께 복원합니다.',
    'RestoreQuicksaveLoads.json':
        '원작처럼 퀵세이브 로드 횟수를\n기록하고 표시합니다.\n\n'
        '「로드」 횟수에는 챕터 중 퀵세이브 로드 버튼,\n챕터 맵 메뉴의 턴별 로드,\n'
        '게임을 끈 뒤 타이틀이나 버튼 조합으로\n이어할 때의 로드가 포함됩니다.',
    'RestoreWPName.json':
        'EXE 내부의 여러 텍스트에서\nEx-P 대신 WP, EX 대신 WP를\n표시하도록 되돌립니다.\n\n'
        '나머지 Ex 표기까지 바꾸려면\ndata5-4/Data_Text의 Restore_WPName\naddOn의 Active를 true로 하세요.',
    'TogglePrivateSquare.json': None,  # placeholder (real file name below)
    'TogglePrivateSquareAnimation.json':
        '켜면 「프라이빗 스퀘어」의\n원래 애니메이션을 표시합니다.\n끄면 일반 분신 애니메이션을 표시합니다.',
    'UnlockFPMUsage.json':
        '모든 챕터에서 풀 파워 모드(FPM)를\n쓸 수 있게 합니다.\n\n[실험적] 충분히 검증되지 않은 모드입니다.',
    'UnlockPairUsage.json':
        'FMW1·FMW2 장을 포함한 모든 챕터에서\n페어를 쓸 수 있게 합니다.\n\n[실험적] 충분히 검증되지 않은 모드입니다.',
}
D.pop('TogglePrivateSquare.json')
p = 'translate/ko_desc.json'; d = json.load(open(p, encoding='utf8'))
d.update(D)
json.dump(d, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('ko_desc', len(d))
