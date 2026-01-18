; NLS (Natural Language Source) Windows Installer
; Built with Inno Setup - https://jrsoftware.org/isinfo.php

#define MyAppName "NLS Compiler"
#define MyAppVersion "0.2.1"
#define MyAppPublisher "Mnehmos"
#define MyAppURL "https://github.com/Mnehmos/mnehmos.nls.lang"
#define MyAppExeName "nls_launcher.exe"

[Setup]
AppId={{B8F5E9A2-7C3D-4E1F-A6B9-8D2C5E0F1A3B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\NLS
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=..\LICENSE
OutputDir=installer_output
OutputBaseFilename=nls-setup-{#MyAppVersion}
SetupIconFile=nls-file.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ChangesAssociations=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
; Main launcher executable with embedded icon
Source: "dist\nls_launcher.exe"; DestDir: "{app}"; Flags: ignoreversion
; Icon file for backup
Source: "nls-file.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

[Registry]
; File extension registration - the PROPER way
Root: HKCR; Subkey: ".nl"; ValueType: string; ValueName: ""; ValueData: "NLSFile"; Flags: uninsdeletevalue
Root: HKCR; Subkey: ".nl"; ValueType: string; ValueName: "Content Type"; ValueData: "text/plain"; Flags: uninsdeletevalue
Root: HKCR; Subkey: "NLSFile"; ValueType: string; ValueName: ""; ValueData: "NLS Specification File"; Flags: uninsdeletekey
Root: HKCR; Subkey: "NLSFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKCR; Subkey: "NLSFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKCR; Subkey: "NLSFile\shell\edit"; ValueType: string; ValueName: ""; ValueData: "Edit with VS Code"
Root: HKCR; Subkey: "NLSFile\shell\edit\command"; ValueType: string; ValueName: ""; ValueData: """code"" ""%1"""

; Also register the compile action
Root: HKCR; Subkey: "NLSFile\shell\compile"; ValueType: string; ValueName: ""; ValueData: "Compile with NLS"
Root: HKCR; Subkey: "NLSFile\shell\compile\command"; ValueType: string; ValueName: ""; ValueData: """cmd"" /c ""nlsc compile ""%1"" && pause"""

[Code]
// Notify shell of association changes after install
procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    // Refresh shell icon cache
    Exec('ie4uinit.exe', '-ClearIconCache', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  end;
end;

// Notify shell on uninstall
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  ResultCode: Integer;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    Exec('ie4uinit.exe', '-ClearIconCache', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  end;
end;
