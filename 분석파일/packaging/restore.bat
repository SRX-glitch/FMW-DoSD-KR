@echo off
chcp 65001 >nul
setlocal EnableExtensions
title FMWCB + 한글패치 제거(원본 복원)

set "HERE=%~dp0"
set "GAME=%~1"
if "%GAME%"=="" if exist "%HERE%fmw_dosd.exe" set "GAME=%HERE%"
if "%GAME%"=="" (
  echo 게임 폴더 경로를 입력하세요.
  set /p "GAME=> "
)
if not "%GAME:~-1%"=="\" set "GAME=%GAME%\"
set "BK=%GAME%backup_before_kr\"
if not exist "%BK%data.win" ( echo [오류] 백업이 없습니다: %BK% & pause & exit /b 1 )

copy /y "%BK%data.win" "%GAME%data.win" >nul
copy /y "%BK%data\*" "%GAME%data\" >nul
copy /y "%BK%meta\*" "%GAME%meta\" >nul
set "LA=%LOCALAPPDATA%\fmw_dosd\"
if exist "%LA%mods" rmdir /s /q "%LA%mods"
if exist "%LA%addOns" rmdir /s /q "%LA%addOns"
if exist "%BK%LocalAppData\mods" xcopy /e /i /q /y "%BK%LocalAppData\mods" "%LA%mods" >nul
if exist "%BK%LocalAppData\addOns" xcopy /e /i /q /y "%BK%LocalAppData\addOns" "%LA%addOns" >nul
echo 원본으로 복원했습니다.
pause
