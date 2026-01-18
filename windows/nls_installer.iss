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

[Tasks]
Name: "installpip"; Description: "Install nlsc compiler via pip (requires Python)"; GroupDescription: "NLS Compiler:"; Flags: checkedonce

[Files]
; Main launcher executable with embedded icon
Source: "dist\nls_launcher.exe"; DestDir: "{app}"; Flags: ignoreversion
; Icon file for backup
Source: "nls-file.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\NLS Command Prompt"; Filename: "{cmd}"; Parameters: "/k nlsc --help"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

[Registry]
; File extension registration
Root: HKCR; Subkey: ".nl"; ValueType: string; ValueName: ""; ValueData: "NLSFile"; Flags: uninsdeletevalue
Root: HKCR; Subkey: ".nl"; ValueType: string; ValueName: "Content Type"; ValueData: "text/plain"; Flags: uninsdeletevalue
Root: HKCR; Subkey: "NLSFile"; ValueType: string; ValueName: ""; ValueData: "NLS Specification File"; Flags: uninsdeletekey
Root: HKCR; Subkey: "NLSFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKCR; Subkey: "NLSFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKCR; Subkey: "NLSFile\shell\edit"; ValueType: string; ValueName: ""; ValueData: "Edit with VS Code"
Root: HKCR; Subkey: "NLSFile\shell\edit\command"; ValueType: string; ValueName: ""; ValueData: """code"" ""%1"""

; Context menu: Compile with NLS
Root: HKCR; Subkey: "NLSFile\shell\compile"; ValueType: string; ValueName: ""; ValueData: "Compile with NLS"
Root: HKCR; Subkey: "NLSFile\shell\compile"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\{#MyAppExeName},0"
Root: HKCR; Subkey: "NLSFile\shell\compile\command"; ValueType: string; ValueName: ""; ValueData: """cmd"" /c ""nlsc compile ""%1"" && pause"""

; Context menu: Verify NLS
Root: HKCR; Subkey: "NLSFile\shell\verify"; ValueType: string; ValueName: ""; ValueData: "Verify NLS Syntax"
Root: HKCR; Subkey: "NLSFile\shell\verify"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\{#MyAppExeName},0"
Root: HKCR; Subkey: "NLSFile\shell\verify\command"; ValueType: string; ValueName: ""; ValueData: """cmd"" /c ""nlsc verify ""%1"" && pause"""

; Context menu: Run Tests
Root: HKCR; Subkey: "NLSFile\shell\test"; ValueType: string; ValueName: ""; ValueData: "Run NLS Tests"
Root: HKCR; Subkey: "NLSFile\shell\test"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\{#MyAppExeName},0"
Root: HKCR; Subkey: "NLSFile\shell\test\command"; ValueType: string; ValueName: ""; ValueData: """cmd"" /c ""nlsc test ""%1"" && pause"""

[Code]
var
  PythonFound: Boolean;
  PythonPath: String;

// Check if Python is installed
function IsPythonInstalled(): Boolean;
var
  ResultCode: Integer;
begin
  Result := Exec('python', '--version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0);
  if not Result then
    Result := Exec('python3', '--version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0);
end;

// Find Python executable path
function GetPythonExe(): String;
var
  ResultCode: Integer;
begin
  if Exec('where', 'python', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0) then
    Result := 'python'
  else if Exec('where', 'python3', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0) then
    Result := 'python3'
  else
    Result := '';
end;

// Initialize wizard
procedure InitializeWizard();
begin
  PythonFound := IsPythonInstalled();
  if PythonFound then
    PythonPath := GetPythonExe();
end;

// Check prerequisites before install
function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;

  if CurPageID = wpSelectTasks then
  begin
    if WizardIsTaskSelected('installpip') and not PythonFound then
    begin
      if MsgBox('Python was not found on your system.' + #13#10 + #13#10 +
                'The nlsc compiler requires Python 3.11 or later.' + #13#10 + #13#10 +
                'Would you like to continue without installing the compiler?' + #13#10 +
                '(You can install it later with: pip install nlsc)',
                mbConfirmation, MB_YESNO) = IDNO then
        Result := False;
    end;
  end;
end;

// Run pip install after files are installed
procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
  StatusText: String;
begin
  if CurStep = ssPostInstall then
  begin
    // Install nlsc via pip if requested and Python is available
    if WizardIsTaskSelected('installpip') and PythonFound then
    begin
      StatusText := WizardForm.StatusLabel.Caption;
      WizardForm.StatusLabel.Caption := 'Installing nlsc compiler via pip...';
      WizardForm.StatusLabel.Update;

      // Run pip install nlsc
      if not Exec('cmd', '/c "' + PythonPath + ' -m pip install --upgrade nlsc"',
                  '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
      begin
        MsgBox('Failed to run pip install. You can install manually with:' + #13#10 +
               'pip install nlsc', mbError, MB_OK);
      end
      else if ResultCode <> 0 then
      begin
        MsgBox('pip install returned an error. You may need to install manually:' + #13#10 +
               'pip install nlsc', mbError, MB_OK);
      end;

      WizardForm.StatusLabel.Caption := StatusText;
    end;

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
