"""FMWCB 1.2.4.2 additions: new code strings (ko_code.json) and addOn strings (ko_text.json).
Terms follow the KR patch (Data_Text / Data_Spirits / Data_Skills of fmw_korean_261030, looked up by ID)."""
import json

p = 'translate/ko_code.json'; d = json.load(open(p, encoding='utf8'))
add = {
    'gml_GlobalScript_UI_NG_draw': {
        'Would you like to carry over all base game units into the next playthrough?': '본편의 모든 유닛을 다음 회차로 이어받으시겠습니까?',
        'Begin your full Dream?': '모든 유닛과 함께 꿈을 시작하겠습니까?'},
    'gml_GlobalScript_UI_NG_list': {'Carry Over All Units': '모든 유닛 이어받기'},
    'gml_GlobalScript_UI_NG_select': {
        'Would you like to choose the resources to bring into NG+?': '다음 회차로 이어받을 자원을 고르시겠습니까?',
        'Proceed with these options? Any resource that is not selected will be reset in the next playthough.':
            '이 설정으로 진행하시겠습니까? 선택하지 않은 자원은 다음 회차에서 초기화됩니다.'},
    'gml_GlobalScript_NG_resources': {
        'Confirm Carryovers': '이어받기 결정', 'Select Carryovers': '이어받을 항목 선택', 'Resources': '자원',
        'Points': '점수', 'EX-Points': 'Ex-P', 'Items': '아이템', 'Kills': '격추수',
        'Carry over current Points and all Points accumulated\nover previous playthroughs.':
            '현재 점수와 이전 회차까지 누적된\n모든 점수를 이어받습니다.',
        'Carry over current EX-Points and all EX-Points accumulated\nover previous playthroughs.':
            '현재 Ex-P와 이전 회차까지 누적된\n모든 Ex-P를 이어받습니다.',
        'Carry over all items accumulated over previous playthoughs.': '이전 회차까지 모은 모든 아이템을 이어받습니다.',
        'Carry over current PP and all PP accumulated\nover previous playthroughs for every player character.':
            '모든 아군 캐릭터가 현재 PP와\n이전 회차까지 누적된 모든 PP를 이어받습니다.',
        'Carry over current Kills and all Kills accumulated\nover previous playthroughs for every player character.':
            '모든 아군 캐릭터가 현재 격추수와\n이전 회차까지 누적된 모든 격추수를 이어받습니다.'},
    'gml_GlobalScript_main_det_avoid_action2': {'Unyielding Spirit': '불굴의 정신'},
    'gml_GlobalScript_calculate_damage_mult': {'Friendship Bonus': '신뢰 보너스'},
    'gml_GlobalScript_UI_info_draw': {'Main': '메인', 'Assist': '지원', 'Support': '원호', 'Final Damage': '최종 대미지'},
    'gml_GlobalScript_UI_clear_draw': {
        'Saves/Loads': '세이브/로드횟수', 'Total Saves/Loads': '합계세이브/로드횟수',
        '|NGs|Army Name|Avg. Upgrade %|Highest Damage Dealt|Highest Damage Taken|Vegetables Eaten|Photos Taken|Dream Spirits Cast|':
            '|주회|부대명|평균 업그레이드 %|최대로 입힌 데미지|최대로 받은 데미지|먹은 채소의 수|찍은 사진 수|「꿈」 사용 횟수|',
        '|NGs|Army Name|Avg. Upgrade %|Vegetables Eaten|Photos Taken|Dream Spirits Cast|Highest Damage Dealt|Highest Damage Taken|':
            '|주회|부대명|평균 업그레이드 %|먹은 채소의 수|찍은 사진 수|「꿈」 사용 횟수|최대로 입힌 데미지|최대로 받은 데미지|',
        '|Forests Purified by Toyohime|Sheep Counters Used by Mehko|Sweet Dreams Induced by Makura|Total Akyu Points|Total Lily White Points|':
            '|토요히메가 정화한 숲|메코가 사용한 양 카운터|마쿠라가 선사한 스위트 드림|아큐 포인트 합계|릴리 화이트 포인트 합계|'},
    'gml_GlobalScript_UI_clear_create': {'Fantasy Maiden Wars': '환상소녀대전대'},
    'gml_Object_ObjDebug_Create_0': {'Fully Unlock All Skills': '스킬 전부 해금'},
    'gml_Object_ObjDebug_Draw_64': {
        'Press the Enter key/Menu button to end the chapter.': 'Enter 키/메뉴 버튼으로 챕터를 종료합니다.',
        'Press the Tab key/View button to force a Game Over.': 'Tab 키/보기 버튼으로 강제 게임 오버합니다.',
        'Unlock All Skills in Arc option enabled.\nThis will unlock all Personal Skills that are learned up to the level cap\n'
        'in the current arc for the current available roster.\nDoes not include Personal Skills learned through events.\n'
        'Saving the game after the Intermission has been reloaded\nwill permanently add these new skills to each character.\n\n'
        'Would you like to apply this change?':
            '「현재 장의 스킬 전부 해금」이 켜져 있습니다.\n현재 편성 가능한 캐릭터 전원이 현재 장의 레벨 상한까지\n'
            '배우는 개인 스킬을 모두 해금합니다.\n이벤트로 배우는 개인 스킬은 포함되지 않습니다.\n'
            '인터미션을 다시 불러온 뒤 세이브하면\n새 스킬이 각 캐릭터에 영구적으로 추가됩니다.\n\n이 변경을 적용하시겠습니까?',
        'Fully Unlock All Skills option enabled.\nThis will unlock all Personal Skills\n'
        'regardless of level and event flags for the current available roster.\n'
        'Saving the game after the Intermission has been reloaded\nwill permanently add these new skills to each character.\n\n'
        'Would you like to apply this change?':
            '「스킬 전부 해금」이 켜져 있습니다.\n현재 편성 가능한 캐릭터 전원의 개인 스킬을\n'
            '레벨·이벤트 조건과 관계없이 모두 해금합니다.\n'
            '인터미션을 다시 불러온 뒤 세이브하면\n새 스킬이 각 캐릭터에 영구적으로 추가됩니다.\n\n이 변경을 적용하시겠습니까?'},
}
for k, v in add.items(): d.setdefault(k, {}).update(v)
json.dump(d, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=1)

p = 'translate/ko_text.json'; t = json.load(open(p, encoding='utf8'))
t.update({
    # Data_Skills (new PSes)
    'Golden Autumn (FMW2)': '황금의 가을(FMW2)',
    'Increases EXP gain by +<VAL1>％, reduces damage taken by -<VAL2>％.': '획득 경험치 +<VAL1>%, 받는 대미지 -<VAL2>%.',
    'Is That So~': '그런가~',
    'When unit hits an enemy with an attack/ enemy loses <VAL1> Power.': '공격이 적에게 명중하면 적의 파워가 <VAL1> 내려간다.',
    'Night Owl (FMW2)': '밤의 권속(FMW2)',
    "Sets unit's Night terrain rating to SS.": '유닛의 지형적응「밤」이 SS가 된다.',
    'Phoenix Claw': '불사조의 발톱',
    'Increases damage dealt by CQB weapons by +<VAL1>%.\nDecreases damage dealt by RNG weapons by -<VAL1>%.':
        '격투무기로 주는 대미지 +<VAL1>%.\n사격무기로 주는 대미지 -<VAL1>%.',
    'Quake Kick (FMW2)': '진각(FMW2)',
    "Sets unit's Land terrain rating to SS and Air terrain rating to B.": '유닛의 지형적응「땅」이 SS, 「공중」이 B가 된다.',
    'Safe Spot': '안지안정',
    'If the enemy does not counterattack/ increases damage dealt by +10% (+20% at level 2).\nDoes not apply to support or assist attacks.':
        '적의 반격을 받지 않을 때 주는 대미지 +10%(레벨2는 +20%).\n원호공격과 지원공격에는 적용되지 않는다.',
    'Slacker (FMW2)': '척락실로(FMW2)',
    'Unit gains HP Regen (L)/ but reduces her EXP and PP gain by -<VAL2>%.': 'HP회복(대)을 얻지만 획득 경험치와 PP가 -<VAL2>%.',
    'Teleport': '텔레포트',
    'The unit can ignore movement penalties from terrain.\nIn addition, the unit can move through any other unit.':
        '지형에 따른 이동 감소 효과를 받지 않는다.\n또한 다른 유닛이 있는 칸을 모두 통과할 수 있다.',
    'Unyielding Spirit': '불굴의 정신',   # also hard-coded in main_det_avoid_action2 (barrier name)
    'If an enemy attack will reduce their HP to 0, the unit will survive with 10 HP.\n(<COUNT> uses.)':
        '적의 공격으로 HP가 0이 될 때 HP 10을 남기고 버틴다.\n(<COUNT>회 사용가능)',
    # Data_Spirits restore addOns: EN restores older fan names; KR never had that split -> KR vanilla text by ID
    'Grit': '불굴',
    'Reduces damage of the next hit taken to 10.\n(Grazes are not considered to be hits.)': '한번만 피탄시 대미지가 10이 된다.\n(그레이즈는 피탄으로 취급하지 않는다)',
    'Courage': '용기',
    'Grants the effects of Accel/ Strike/ Grit/ Yell/ Assail/ Fury/ and Valor.': '「가속」 「필중」 「불굴」 「기합」 「돌격」 「직격」 「열혈」의 효과.',
    'Strike': '필중',
    'For 1 turn/ grants 100% accuracy rate.\nEffect is overridden by Alert.': '1턴동안 명중률이 100%가 된다. 상대가 「번뜩임」을 사용했을 경우 그쪽이 우선된다.',
    'Attune': '감응',
    'Grants target ally the effects of Strike.': '지정한 아군 유닛에게 「필중」의 효과.',
    'Alert': '번뜩임',
    'Grants 100% chance to dodge the next attack.\nOverrides Strike/ but ineffective against Support Attacks.': '한번만 회피율이 100%가 된다.\n효과는 필중보다 우선되지만 원호공격에 대해선 무효.',
    'Assault': '기습',
    'Grants the effects of Accel/ Strike/ and Valor.': '「가속」 「필중」 「열혈」의 효과.',
    'Confuse': '교란',
    'For 1 turn/ all enemies will have their accuracy rates halved.\nEffect overriden by Strike.': '1턴동안 적유닛의 최종 명중률이 절반이 된다.\n효과는 「필중」이 우선.',
    'Miracle': '기적',
    'Grants the effects of Accel/ Strike/ Alert/ Drive/ Valor/ Guard/\nLuck/ Gain/ and Guts.': '「가속」 「필중」 「번뜩임」 「기백」 「열혈」 「철벽」\n「행운」 「노력」 「초근성」의 효과.',
    'Shiver': '전율',
    'All enemies lose 10 Power.': '모든 적유닛의 파워가 10 내려간다.',
    # Data_Text restore addOns (WP wording): KR vanilla sentence with Ex -> WP
    'Bonus condition fulfilled!\n(Gained an extra 5 WP)': '보너스 조건을 클리어했다!(보너스 WP 5 획득)',
    'Bonus condition fulfilled!\n(Gained an extra 5 EX-P)': '보너스 조건을 클리어했다!(보너스 Ex-P 5 획득)',
    'Select MAX WP Bonus Upgrades': 'MAX WP보너스를 선택한다.',
    "Increase a unit's WP Level.": '유닛의 WP레벨을 상승시킵니다.',
    'WP Upgrade': 'WP강화',
    "{}'s WP Level will increase to {}.\nProceed?": '{} 의WP레벨을 {} 으로 올립니다. 괜찮습니까?',
    'WP Level increased to {}!': 'WP레벨이 {} 로 올랐다!',
    'These MAX WP Bonuses will be selected. Proceed?': 'MAX WP보너스를 선택합니다. 괜찮습니까?',
    'Hold off on selecting MAX WP Bonuses.\n(You can select later from the upgrade menu.)': 'MAX WP보너스의 선택을 유보합니다.(강화화면에서 다시 선택할 수 있습니다.)',
    'MAX WP Bonus': 'MAX WP보너스', 'Rem. WP': '남은WP', 'Req. WP': '필요WP', 'WP Bonus': 'WP보너스', 'WP Lv': 'WP-Lv',
    "You've gained {0} WP!": '{0} WP을 입수했다!',
})
json.dump(t, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('ok', len(d), len(t))
