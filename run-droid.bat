@echo off
chcp 65001 > nul
cd /d "%~dp0"

REM Launch PowerShell Windows Forms GUI
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0gui_droid_winforms.ps1"

pause
