@echo off
rem Install global AI agent rules (ASCII only)
rem   global_rules.md [+ machine_rules\personal.md + machine_rules\<machine>.md] + machine tag
rem     -> %USERPROFILE%\.claude\CLAUDE.md        (Claude Code)
rem     -> %USERPROFILE%\.gemini\GEMINI.md        (Antigravity)
rem     -> %USERPROFILE%\.codex\AGENTS.md         (Codex)
rem     -> %USERPROFILE%\.config\opencode\AGENTS.md (OpenCode)
rem Dev/General PCs (home/dev/general): also make Claude Code read both CLAUDE.md and AGENTS.md
rem   (%USERPROFILE%\.claude\settings.json, only created if missing)
rem OpenCode: global config %USERPROFILE%\.config\opencode\opencode.jsonc (only created if missing)
rem Existing files are backed up as *.YYYYMMDD_HHMMSS.bak before overwrite.
rem Usage: install.bat [home|dev|controlled|general]   (no argument = ask)
setlocal
cd /d "%~dp0"

if not exist "global_rules.md" (
    echo [ERROR] global_rules.md not found next to install.bat.
    goto :fail
)

set "MACHINE=%~1"
if not "%MACHINE%"=="" goto :check_machine
echo Which computer is this?
echo   [1] home       - home PC (personal workflow)
echo   [2] dev        - company personal PC (internet, no intranet)
echo   [3] controlled - company PC (intranet, restricted install)
echo   [4] general    - general / colleague PC (standard rules only)
choice /c 1234 /n /m "Press 1, 2, 3 or 4: "
if errorlevel 4 (set "MACHINE=general") else if errorlevel 3 (set "MACHINE=controlled") else if errorlevel 2 (set "MACHINE=dev") else (set "MACHINE=home")

:check_machine
if /i not "%MACHINE%"=="home" if /i not "%MACHINE%"=="dev" if /i not "%MACHINE%"=="controlled" if /i not "%MACHINE%"=="general" (
    echo [ERROR] Unknown machine "%MACHINE%". Use home, dev, controlled or general.
    goto :fail
)

rem Build the final rules file: global_rules.md + optional machine rules + machine tag line
set "SRC=%TEMP%\ai_agent_rules_%RANDOM%.md"
copy /y "global_rules.md" "%SRC%" >nul || goto :fail
if /i not "%MACHINE%"=="general" (
    if exist "machine_rules\personal.md" (
        >>"%SRC%" echo.
        type "machine_rules\personal.md" >>"%SRC%"
    )
    if exist "machine_rules\%MACHINE%.md" (
        >>"%SRC%" echo.
        type "machine_rules\%MACHINE%.md" >>"%SRC%"
    )
)
>>"%SRC%" echo.
>>"%SRC%" echo ---
>>"%SRC%" echo THIS MACHINE: %MACHINE%

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "TS=%%i"

call :install "%USERPROFILE%\.claude" "CLAUDE.md" || goto :fail
call :install "%USERPROFILE%\.gemini" "GEMINI.md" || goto :fail
call :install "%USERPROFILE%\.codex" "AGENTS.md" || goto :fail
call :install "%USERPROFILE%\.config\opencode" "AGENTS.md" || goto :fail
if /i not "%MACHINE%"=="controlled" call :settings || goto :fail
call :opencodecfg || goto :fail
call :trigger_skills_deploy
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
rem Claude Code: read CLAUDE.md and AGENTS.md together (+ permissions.deny for personal modes)
set "CFG=%USERPROFILE%\.claude\settings.json"
where claude >nul 2>&1 && (
    for /f "tokens=*" %%v in ('claude --version 2^>nul') do (
        echo [INFO] Detected Claude Code CLI: %%v ^(v2.1.285+ recommended; older needs agents-md@builtin^)
    )
)
if exist "%CFG%" (
    if /i "%MACHINE%"=="general" (
        findstr /c:"\"agents-md@builtin\"" "%CFG%" >nul && findstr /c:"cc-plugin-agents-md@builtin" "%CFG%" >nul && (
            echo [SKIP] %CFG% already configured.
            exit /b 0
        )
    ) else (
        findstr /c:"\"agents-md@builtin\"" "%CFG%" >nul && findstr /c:"cc-plugin-agents-md@builtin" "%CFG%" >nul && findstr /c:"google.cloud_oauth.relay" "%CFG%" >nul && (
            echo [SKIP] %CFG% already configured.
            exit /b 0
        )
    )
    echo [WARN] %CFG% exists. Add instructionFiles / permissions.deny manually, see README.
    exit /b 0
)
>"%CFG%" echo {
if /i not "%MACHINE%"=="general" (
    >>"%CFG%" echo   "permissions": {
    >>"%CFG%" echo     "deny": [
    >>"%CFG%" echo       "Read(./**/google.cloud_oauth.relay/**)"
    >>"%CFG%" echo     ]
    >>"%CFG%" echo   },
)
>>"%CFG%" echo   "pluginConfigs": {
>>"%CFG%" echo     "agents-md@builtin": {
>>"%CFG%" echo       "options": { "instructionFiles": "claude-md-and-agents-md" }
>>"%CFG%" echo     },
>>"%CFG%" echo     "cc-plugin-agents-md@builtin": {
>>"%CFG%" echo       "options": { "instructionFiles": "claude-md-and-agents-md" }
>>"%CFG%" echo     }
>>"%CFG%" echo   }
>>"%CFG%" echo }
echo [OK] %CFG%
exit /b 0

:opencodecfg
rem OpenCode: workspace rules above the project root + sensitive path block
set "OCFG=%USERPROFILE%\.config\opencode\opencode.jsonc"
if exist "%OCFG%" (
    if /i "%MACHINE%"=="general" (
        findstr /c:"git push" "%OCFG%" >nul && (
            echo [SKIP] %OCFG% already configured.
            exit /b 0
        )
    ) else (
        findstr /c:"AI_Workspace/AGENTS.md" "%OCFG%" >nul && findstr /c:"google.cloud_oauth.relay" "%OCFG%" >nul && findstr /c:"git push" "%OCFG%" >nul && (
            echo [SKIP] %OCFG% already configured.
            exit /b 0
        )
    )
    echo [WARN] %OCFG% exists. Add instructions / permissions manually, see README.
    exit /b 0
)
>"%OCFG%" echo {
>>"%OCFG%" echo   "$schema": "https://opencode.ai/config.json",
if /i not "%MACHINE%"=="general" (
    >>"%OCFG%" echo   "instructions": [
    >>"%OCFG%" echo     "D:/AI_Workspace/AGENTS.md"
    >>"%OCFG%" echo   ],
)
>>"%OCFG%" echo   "permissions": [
if /i not "%MACHINE%"=="general" (
    >>"%OCFG%" echo     { "action": "read", "resource": "*google.cloud_oauth.relay*", "effect": "deny" },
)
>>"%OCFG%" echo     { "action": "shell", "resource": "git push *", "effect": "ask" }
>>"%OCFG%" echo   ]
>>"%OCFG%" echo }
echo [OK] %OCFG%
exit /b 0

:trigger_skills_deploy
rem Auto-link to ai.agent_skills repository if present in the same workspace or parent
set "SKILLS_BAT="
if exist "..\ai.agent_skills\deploy_global_skills.bat" set "SKILLS_BAT=..\ai.agent_skills\deploy_global_skills.bat"
if exist "..\..\ai.agent_skills\deploy_global_skills.bat" set "SKILLS_BAT=..\..\ai.agent_skills\deploy_global_skills.bat"
if defined SKILLS_BAT (
    echo.
    echo [INFO] Detected ai.agent_skills. Triggering global skills deployment...
    cmd /c "%SKILLS_BAT% < nul" || (
        echo [WARN] Global skills deployment returned non-zero.
    )
)
exit /b 0

:fail
if defined SRC del "%SRC%" >nul 2>&1
echo [ERROR] Install failed.
pause
exit /b 1
