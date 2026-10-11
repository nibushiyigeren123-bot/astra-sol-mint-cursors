@echo off
setlocal
set "PSModulePath="
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" -Character sol -Size 48 -Apply
if errorlevel 1 pause
