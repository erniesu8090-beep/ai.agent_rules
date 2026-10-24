@echo off
rem Install global AI agent rules (ASCII only)
rem   global_rules.md + machine_rules\<machine>.md + machine tag -> %USERPROFILE%\.claude\CLAUDE.md          (Claude Code)
rem   global_rules.md + machine_rules\<machine>.md + machine tag -> %USERPROFILE%\.gemini\GEMINI.md          (Antigravity)
rem   global_rules.md + machine_rules\<machine>.md + machine tag -> %USERPROFILE%\.codex\AGENTS.md           (Codex)
rem   global_rules.md + machine_rules\<machine>.md + machine tag -> %USERPROFILE%\.config\opencode\AGENTS.md (OpenCode)
rem Dev PCs (home/dev): also make Claude Code read both CLAUDE.md and AGENTS.md
rem   (%USERPROFILE%\.claude\settings.json, only created if missing)
rem Existing files are backed up as *.YYYYMMDD_HHMMSS.bak before overwrite.
rem Usage: install.bat [home|dev|controlled]   (no argument = ask)
setlocal
cd /d "%~dp0"

if not exist "global_rules.md" (
    echo [ERROR] global_rules.md not found next to install.bat.
    goto :fail
)

set "MACHINE=%~1"
if not "%MACHINE%"=="" goto :check_machine
echo Which computer is this?
echo   [1] home       - home PC
echo   [2] dev        - company personal PC (internet, no intranet)
echo   [3] controlled - company PC (intranet, restricted install)
choice /c 123 /n /m "Press 1, 2 or 3: "
if errorlevel 3 (set "MACHINE=controlled") else if errorlevel 2 (set "MACHINE=dev") else (set "MACHINE=home")

:check_machine
if /i not "%MACHINE%"=="home" if /i not "%MACHINE%"=="dev" if /i not "%MACHINE%"=="controlled" (
    echo [ERROR] Unknown machine "%MACHINE%". Use home, dev or controlled.
    goto :fail
)

rem Build the final rules file: global_rules.md + machine tag line
set "SRC=%TEMP%\ai_agent_rules_%RANDOM%.md"
copy /y "global_rules.md" "%SRC%" >nul || goto :fail
rem Machine-only rules (e.g. antivirus limits for the controlled PC)
if exist "machine_rules\%MACHINE%.md" type "machine_rules\%MACHINE%.md" >>"%SRC%"
>>"%SRC%" echo.
>>"%SRC%" echo ---
>>"%SRC%" echo THIS MACHINE: %MACHINE%

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "TS=%%i"

call :install "%USERPROFILE%\.claude" "CLAUDE.md" || goto :fail
call :install "%USERPROFILE%\.gemini" "GEMINI.md" || goto :fail
call :install "%USERPROFILE%\.codex" "AGENTS.md" || goto :fail
call :install "%USERPROFILE%\.config\opencode" "AGENTS.md" || goto :fail
if /i not "%MACHINE%"=="controlled" call :settings || goto :fail
del "%SRC%" >nul 2>&1

echo.
echo [DONE] Installed as "%MACHINE%". Restart Claude Code / Antigravity / Codex / OpenCode to load the new rules.
pause
exit /b 0

:install
set "DIR=%~1"
set "DST=%~1\%~2"
if not exist "%DIR%" mkdir "%DIR%" || exit /b 1
if exist "%DST%" (
    fc /b "%SRC%" "%DST%" >nul 2>&1 && (
        echo [SKIP] %DST% is already up to date.
        exit /b 0
    )
    copy /y "%DST%" "%DST%.%TS%.bak" >nul || exit /b 1
    echo [BACKUP] %DST%.%TS%.bak
)
copy /y "%SRC%" "%DST%" >nul || exit /b 1
echo [OK] %DST%
exit /b 0

:settings
rem Claude Code: read CLAUDE.md and AGENTS.md together
set "CFG=%USERPROFILE%\.claude\settings.json"
if exist "%CFG%" (
    findstr /c:"claude-md-and-agents-md" "%CFG%" >nul && (
        echo [SKIP] %CFG% already reads AGENTS.md.
        exit /b 0
    )
    echo [WARN] %CFG% exists. Add instructionFiles manually, see README.
    exit /b 0
)
>"%CFG%" echo {
>>"%CFG%" echo   "pluginConfigs": {
>>"%CFG%" echo     "cc-plugin-agents-md@builtin": {
>>"%CFG%" echo       "options": { "instructionFiles": "claude-md-and-agents-md" }
>>"%CFG%" echo     }
>>"%CFG%" echo   }
>>"%CFG%" echo }
echo [OK] %CFG%
exit /b 0

:fail
if defined SRC del "%SRC%" >nul 2>&1
echo [ERROR] Install failed.
pause
exit /b 1
