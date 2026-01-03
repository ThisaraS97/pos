@echo off
REM This is the SIMPLEST way to start AnyPos
REM Just run this file!

cd /d "%~dp0"
if exist START.bat (
    call START.bat
) else (
    echo Error: START.bat not found
    pause
)
