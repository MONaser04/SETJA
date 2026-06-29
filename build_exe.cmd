@echo off
echo Building SETJA.exe using PyInstaller...
set "PYEXE=d:\Downloads\deep_research_agent\.venv\Scripts\pyinstaller.exe"
set "PIPEXE=d:\Downloads\deep_research_agent\.venv\Scripts\pip.exe"
if exist "%PYEXE%" (
    "%PIPEXE%" install customtkinter
    "%PYEXE%" --noconfirm --onefile --windowed --name "SETJA" --icon="app_icon.ico" "src\SETJA_Control_Panel.py"
    move /Y "dist\SETJA.exe" ".\"
    rmdir /S /Q dist build
    del /Q SETJA.spec
    echo SUCCESS! SETJA.exe created in root folder.
) else (
    echo PyInstaller not found. Please install it first using: pip install pyinstaller
)
pause
