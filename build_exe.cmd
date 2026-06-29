@echo off
echo Building SETJA.exe using PyInstaller...
set "PYEXE=d:\Downloads\deep_research_agent\.venv\Scripts\pyinstaller.exe"
if exist "%PYEXE%" (
    "%PYEXE%" --noconfirm --onefile --windowed --name "SETJA" --icon="SetupClassicIcon.ico" "src\SETJA_Control_Panel.py"
    move /Y "dist\SETJA.exe" ".\"
    rmdir /S /Q dist build
    del /Q SETJA.spec
    echo SUCCESS! SETJA.exe created in root folder.
) else (
    echo PyInstaller not found. Please install it first using: pip install pyinstaller
)
pause
