@echo off
setlocal
set "ROOT=%~dp0"
set "MODE=%~1"

echo ==============================================
echo SETJA Post-Installation Setup
echo ==============================================
echo Mode selected: %MODE%
echo.

:: Check for python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.11+ and check "Add Python to PATH".
    pause
    exit /b 1
)

echo Creating Virtual Environment...
python -m venv "%ROOT%setja_stable"

set "PYEXE=%ROOT%setja_stable\Scripts\python.exe"

echo Upgrading pip...
"%PYEXE%" -m pip install --upgrade pip

echo Installing Core Requirements...
"%PYEXE%" -m pip install -r "%ROOT%req_core.txt"

if /I "%MODE%"=="full" (
    echo Installing Offline AI Requirements...
    "%PYEXE%" -m pip install -r "%ROOT%req_offline.txt"
)

if exist "%ROOT%req_custom_model.txt" (
    echo Installing Custom Local Models...
    "%PYEXE%" -m pip install -r "%ROOT%req_custom_model.txt"
)

:: Update settings.json based on mode
echo Configuring settings.json...
set "ENABLE_OFFLINE=true"
set "ENGINE=offline"
if /I "%MODE%"=="online" (
    set "ENABLE_OFFLINE=false"
    set "ENGINE=gemini"
)

:: Use python to update the json safely
"%PYEXE%" -c "import json; p='%ROOT:\=\\%settings.json'; d=json.load(open(p)) if __import__('os').path.exists(p) else {}; d['enable_offline']=(True if '%ENABLE_OFFLINE%'=='true' else False); d['engine']='%ENGINE%'; open(p,'w').write(json.dumps(d, indent=4))"

echo.
echo ==============================================
echo Setup Completed Successfully!
echo You can now run SETJA from the Desktop shortcut.
echo ==============================================
pause
endlocal
