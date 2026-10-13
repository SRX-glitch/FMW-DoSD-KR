# 설치 방법

**파일: [`FMWCB-1.2.4.1_KR_xdelta.zip`](FMWCB-1.2.4.1_KR_xdelta.zip)** (약 62MB)
→ 파일을 누른 뒤 오른쪽 위 **다운로드(↓) 버튼**으로 받으세요.

적용 대상: Steam 영어판 **1.2.4** (수정하지 않은 상태)
포함 내용: 한글패치 260529 + 모드 FMWCB 1.2.4.1 + 모드 한글화

---

## 1. 게임을 원본 상태로 준비

이미 다른 패치를 적용했다면 먼저 원본으로 되돌립니다.
> Steam 라이브러리 → 게임 우클릭 → **속성** → **설치된 파일** → **게임 파일 무결성 검사**

## 2. 게임 폴더에 압축 풀기

`FMWCB-1.2.4.1_KR_xdelta.zip` 을 **게임 폴더에 바로** 풉니다.

```
...\steamapps\common\Fantasy Maiden Wars DoSD\
```

> 게임 폴더 찾기: Steam 라이브러리 → 게임 우클릭 → 관리 → **로컬 파일 보기**

풀고 나면 이렇게 됩니다.

```
Fantasy Maiden Wars DoSD\
├─ fmw_dosd.exe              (원래 있던 파일)
├─ data.win                  (원래 있던 파일)
├─ data\  meta\              (원래 있던 폴더)
├─ install.bat               ← 새로 생김
├─ restore.bat
├─ README.txt
├─ patch\
├─ xdelta\
├─ LocalAppData_fmw_dosd\
└─ experimental_mods(선택)\
```

## 3. install.bat 실행

`install.bat` 을 더블클릭합니다. 「설치 완료!」가 나오면 끝입니다.

- 원본 파일은 `backup_before_kr\` 폴더에 자동으로 백업됩니다.
- 모드 설정 파일은 `%LOCALAPPDATA%\fmw_dosd\` 에 복사됩니다.
- 원본이 영어판 1.2.4가 아니면 **아무것도 바꾸지 않고** 멈춥니다. 1번부터 다시 하세요.

## 4. 게임 실행

글로벌 메뉴 → **「모드」** 에서 각 모드를 켜고 끌 수 있습니다.

---

## 제거

게임 폴더의 `restore.bat` 을 실행하면 설치 전 상태로 돌아갑니다.

## 문제 해결

| 증상 | 해결 |
|---|---|
| 「원본 파일이 맞지 않습니다」 | 1번(무결성 검사)을 한 뒤 다시 `install.bat` 실행 |
| 「xdelta\xdelta.exe 가 없습니다」 | zip을 **전부** 풀었는지 확인 (폴더째 풀어야 함) |
| 「게임 폴더가 아닙니다」 | `fmw_dosd.exe` 가 있는 폴더에 풀었는지 확인. 다른 곳에 풀었다면 게임 폴더를 `install.bat` 위로 끌어다 놓기 |
| 창이 잠깐 떴다가 바로 꺼짐 | 2026-09-27 이전에 받은 zip의 버그입니다(게임이 `C:\Program Files (x86)\` 에 있을 때). **zip을 다시 받아** 주세요. |
| 「액세스가 거부되었습니다」 | `install.bat` 우클릭 → **관리자 권한으로 실행** |

파일별 적용 위치와 수동 설치 방법(xdeltaUI 사용)은 zip 안의 `README.txt` 에 있습니다.

## 업데이트 기록

| 날짜 | 내용 | 이미 설치했다면 |
|---|---|---|
| 2026-10-13 | **[테스트 중] 새 모드 항목 `NGUnitCount`** (모드 설정 → Modifiers): 주회 플레이에서 데려갈 유닛 수 상한 변경. 6 = 기본, **0 = 제한 없음**, 1명 이상이면 진행 가능. 드림 모드 화면 실기 검증 전이라 이상하면 Issues로 알려 주세요 | `data.win` 이 바뀌었으므로 Steam 무결성 검사 후 **새 zip으로 다시 설치** |
| 2026-10-13 | 모드 설정 창에서 ON/OFF·값 칸이 설명 글자와 겹치던 5개 설명 정리 | 위와 같음 (새 zip에 포함) |
| 2026-10-13 | 모드 설명 6개를 실제 동작에 맞게 수정 (`EnableAllUnitsNG+`: 인원 무제한이 아니라 **후보 추가**, 인원은 6명 그대로 등) | 게임 동작은 같습니다. 새 설명을 보려면 zip의 `LocalAppData_fmw_dosd\mods` 를 `%LOCALAPPDATA%\fmw_dosd\` 에 덮어쓰기 (모드 ON/OFF 설정은 초기화됨) |
| 2026-09-27 | 게임이 `C:\Program Files (x86)\` 에 있을 때 `install.bat` 이 바로 꺼지던 문제 수정 | zip을 다시 받아 설치 |

## 제보 · 피드백

위 표로 해결되지 않거나 오역·번역 누락을 발견하면
**[Issues에 제보하기](https://github.com/SRX-glitch/FMW-DoSD-KR/issues/new/choose)** → 「설치 문제」 또는 「오역 · 표시 문제」 양식을 골라 주세요.
스크린샷을 함께 올려 주시면 가장 빨리 확인할 수 있습니다. (GitHub 로그인 필요)
