@echo off
set CODE=..\..\code

REM CALLER WORD DIR
set "CWD=%CD%"
echo %CWD%

REM BAT Located
set "BAT_CWD=%~dp0"
cd /d "%BAT_CWD%"

call efont-env.cmd lib:ex10d2

cd %CODE%
micropython -X heapsize=16m main.py

REM BACK TO CALLER WORD DIR
cd /d %CWD%

