@echo off
chcp 65001 >nul
setlocal EnableExtensions
title FMWCB 1.2.4.1 + 한글패치 설치

rem ---- 경로 결정: 이 폴더에 fmw_dosd.exe가 있으면 여기, 아니면 인자/입력으로 받는다
set "HERE=%~dp0"
set "GAME=%~1"
if "%GAME%"=="" if exist "%HERE%fmw_dosd.exe" set "GAME=%HERE%"
if "%GAME%"=="" (
  echo 게임 폴더 경로를 입력하세요. 예: D:\SteamLibrary\steamapps\common\Fantasy Maiden Wars DoSD
  set /p "GAME=> "
)
if not "%GAME:~-1%"=="\" set "GAME=%GAME%\"
set "XD=%HERE%xdelta\xdelta.exe"
set "PT=%HERE%patch\"

if not exist "%XD%" ( echo [오류] xdelta\xdelta.exe 가 없습니다. 압축을 전부 풀었는지 확인하세요. & goto :fail )
if not exist "%GAME%fmw_dosd.exe" ( echo [오류] 게임 폴더가 아닙니다: %GAME% & goto :fail )
if not exist "%PT%data.win.xdelta" ( echo [오류] patch 폴더가 없습니다. & goto :fail )

set "TMPD=%GAME%_kr_patch_tmp\"
if exist "%TMPD%" rmdir /s /q "%TMPD%"
mkdir "%TMPD%data" "%TMPD%meta"

echo [1/3] 패치 파일 생성 중... (원본이 영어판 1.2.4가 아니면 여기서 중단됩니다)
"%XD%" -d -f -s "%GAME%data.win" "%PT%data.win.xdelta" "%TMPD%data.win" || goto :srcfail
for %%F in ("%PT%data\*.xdelta") do (
  "%XD%" -d -f -s "%GAME%data\%%~nF" "%%~fF" "%TMPD%data\%%~nF" || goto :srcfail
)
for %%F in ("%PT%meta\*.xdelta") do (
  "%XD%" -d -f -s "%GAME%meta\%%~nF" "%%~fF" "%TMPD%meta\%%~nF" || goto :srcfail
)

echo [2/3] 원본 백업 후 교체 중...
set "BK=%GAME%backup_before_kr\"
if not exist "%BK%data.win" (
  mkdir "%BK%data" "%BK%meta" 2>nul
  copy /y "%GAME%data.win" "%BK%data.win" >nul
  for %%F in ("%PT%data\*.xdelta") do copy /y "%GAME%data\%%~nF" "%BK%data\%%~nF" >nul
  for %%F in ("%PT%meta\*.xdelta") do copy /y "%GAME%meta\%%~nF" "%BK%meta\%%~nF" >nul
)
copy /y "%TMPD%data.win" "%GAME%data.win" >nul || goto :fail
copy /y "%TMPD%data\*" "%GAME%data\" >nul || goto :fail
copy /y "%TMPD%meta\*" "%GAME%meta\" >nul || goto :fail
rmdir /s /q "%TMPD%"

echo [3/3] 모드 설정 파일 복사 중... (%LOCALAPPDATA%\fmw_dosd)
set "LA=%LOCALAPPDATA%\fmw_dosd\"
if not exist "%LA%" mkdir "%LA%"
if exist "%LA%mods" if not exist "%BK%LocalAppData\mods" xcopy /e /i /q /y "%LA%mods" "%BK%LocalAppData\mods" >nul
if exist "%LA%addOns" if not exist "%BK%LocalAppData\addOns" xcopy /e /i /q /y "%LA%addOns" "%BK%LocalAppData\addOns" >nul
xcopy /e /i /q /y "%HERE%LocalAppData_fmw_dosd\mods" "%LA%mods" >nul || goto :fail
xcopy /e /i /q /y "%HERE%LocalAppData_fmw_dosd\addOns" "%LA%addOns" >nul || goto :fail

echo.
echo 설치 완료! 원본은 %BK% 에 백업되었습니다.
echo 게임 안 글로벌 메뉴 - 「모드」 에서 모드를 켜고 끌 수 있습니다.
pause
exit /b 0

:srcfail
echo.
echo [오류] 원본 파일이 맞지 않습니다. 이미 패치했거나 영어판 1.2.4 원본이 아닙니다.
echo        Steam에서 「로컬 파일 무결성 검사」를 한 뒤 다시 실행하세요. 게임 파일은 바뀌지 않았습니다.
if exist "%TMPD%" rmdir /s /q "%TMPD%"
:fail
echo 설치를 중단했습니다.
pause
exit /b 1
