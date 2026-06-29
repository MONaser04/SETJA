[Setup]
AppName=SETJA Real-Time Screen Translator
AppVersion=1.0
AppPublisher=SETJA Developer
DefaultDirName={autopf}\SETJA
DefaultGroupName=SETJA
OutputDir=.
OutputBaseFilename=SETJA_Setup_v1.0
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\main.cmd

[Types]
Name: "full"; Description: "Full Installation (Recommended - Includes Offline AI Models)"
Name: "online"; Description: "Online API Only (Lightweight - Saves ~5 GB)"
Name: "offline"; Description: "Local Offline Model Only (Strict Privacy)"

[Components]
Name: "core"; Description: "Core Application (UI, Screen Capture, OCR)"; Types: full online offline; Flags: fixed
Name: "local_models"; Description: "Local AI Translation Models"; Types: full offline

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: ".git\*, setja_stable\*, venv\*, __pycache__\*, *.iss, Build_Setup.ps1"

[Icons]
Name: "{group}\SETJA"; Filename: "{app}\main.cmd"
Name: "{autodesktop}\SETJA"; Filename: "{app}\main.cmd"; Tasks: desktopicon

[Run]
Filename: "{app}\post_install.bat"; Parameters: "full"; Components: local_models; Flags: waituntilterminated runascurrentuser shellexec
Filename: "{app}\post_install.bat"; Parameters: "online"; Components: not local_models; Flags: waituntilterminated runascurrentuser shellexec
