@echo off
chcp 65001 > nul
cd /d "%~dp0"

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo エラー: Pythonがインストールされていません。
    echo Python 3.8以上をインストールしてください。
    pause
    exit /b 1
)

REM Launch Python GUI
python "%~dp0gui_droid.py"

pause
