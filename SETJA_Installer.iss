[Setup]
AppId={{8A1B5C2B-A63E-4D78-9B13-1F4F9A6C8C1F}
AppName=SETJA Real-Time Screen Translator
AppVersion=1.0
AppPublisher=SETJA Developer
DefaultDirName={autopf}\SETJA
DefaultGroupName=SETJA
OutputDir=.
OutputBaseFilename=SETJA_Setup_v1.0
Compression=lzma2
SolidCompression=yes
WizardStyle=classic
SetupIconFile=compiler:SetupClassicIcon.ico
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
Source: "*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: ".git\*, setja_stable\*, venv\*, __pycache__\*, *.iss, Build_Setup.ps1, SETJA_Setup_*.exe"

[Icons]
Name: "{group}\SETJA"; Filename: "{app}\SETJA.exe"
Name: "{autodesktop}\SETJA"; Filename: "{app}\SETJA.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\post_install.bat"; Parameters: "full"; Components: local_models; Flags: waituntilterminated runascurrentuser shellexec
Filename: "{app}\post_install.bat"; Parameters: "online"; Components: not local_models; Flags: waituntilterminated runascurrentuser shellexec


[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  if RegKeyExists(HKEY_LOCAL_MACHINE, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{8A1B5C2B-A63E-4D78-9B13-1F4F9A6C8C1F}_is1') or RegKeyExists(HKEY_CURRENT_USER, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{8A1B5C2B-A63E-4D78-9B13-1F4F9A6C8C1F}_is1') then
  begin
    if MsgBox('SETJA is already installed on your computer.' + #13#10#13#10 + 'Would you like to Repair or Modify the installation?', mbConfirmation, MB_YESNO) = IDNO then
    begin
      Result := False;
    end;
  end;
end;
