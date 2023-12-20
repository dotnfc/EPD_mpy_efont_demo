@echo off
set CODE=..\..\code

set "BAT_CWD=%~dp0"
cd /d "%BAT_CWD%"

call efont-env.cmd %CODE%

pushd %CODE%
micropython -X heapsize=8m main.py
popd

