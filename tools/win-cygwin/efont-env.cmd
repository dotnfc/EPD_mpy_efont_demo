@echo off

set MPYBASE=%~dp0
set PATH=%MPYBASE%;%PATH%
set MICROPYPATH=.frozen:%MPYBASE%\%1:%MPYBASE%\%1\lib
