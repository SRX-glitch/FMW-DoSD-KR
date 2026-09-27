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

파일별 적용 위치와 수동 설치 방법(xdeltaUI 사용)은 zip 안의 `README.txt` 에 있습니다.
