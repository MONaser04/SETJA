@echo off
setlocal
set "ROOT=%~dp0"
echo ==============================================
echo SETJA Smart Installer Launcher
echo ==============================================
echo.

:: Check if python is installed on system
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.11+ and check "Add Python to PATH".
    pause
    exit /b 1
)

echo Launching Smart Setup GUI...
start "" pythonw "%ROOT%setup_gui.py"
endlocal
