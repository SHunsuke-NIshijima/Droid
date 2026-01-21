@echo off
REM DROID WPF GUI Launcher
REM Modern WPF GUI for DROID with ModernWpf design

echo Building and launching DROID WPF GUI...
cd /d "%~dp0"

REM Check if .NET SDK is installed
where dotnet >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: .NET SDK is not installed.
    echo Please install .NET 8.0 SDK from https://dotnet.microsoft.com/download
    pause
    exit /b 1
)

REM Build and run the WPF application
cd DroidWpfGui
dotnet run

pause
