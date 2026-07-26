#define AppShortName "YTMDPlayer"
#define AppFullName  "YouTube Music Desktop Player"
#define AppVersion   "1.29.0"
#define AppExeName   AppShortName + ".exe"
#define AppIconRel   "_internal\resources\icons\icon.ico"
#define DistDir      AppShortName + ".dist"
#define SrcDir       DistDir + "\" + AppShortName + "-v" + AppVersion + "-Win32\" + AppShortName

[Setup]
AppId={{F2999036-01A6-4BDA-B0EC-1E549F9D7257}
AppName={#AppFullName}
AppVersion={#AppVersion}
AppVerName={#AppFullName} v{#AppVersion}
AppPublisher=deeffest
WizardStyle=modern dynamic
DefaultDirName={commonpf64}\{#AppShortName}
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\{#AppIconRel}
UninstallDisplayName={#AppFullName}
SetupIconFile={#SrcDir}\{#AppIconRel}
Compression=lzma2
SolidCompression=yes
OutputDir={#DistDir}
OutputBaseFilename={#AppShortName}-v{#AppVersion}-Win32-Setup
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes

[Tasks]
Name: "desktopicon";   Description: "Create a &desktop shortcut";    Flags: checkedonce
Name: "startmenuicon"; Description: "Create a &Start Menu shortcut"; Flags: checkedonce

[InstallDelete]
Type: filesandordirs; Name: "{app}\_internal"

[UninstallDelete]
Type: dirifempty; Name: "{app}"

[Files]
Source: "{#SrcDir}\{#AppExeName}"; DestDir: "{app}";           Flags: ignoreversion
Source: "{#SrcDir}\_internal\*";   DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{userdesktop}\{#AppShortName}";    Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\{#AppIconRel}"; Tasks: desktopicon
Name: "{commonprograms}\{#AppShortName}"; Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\{#AppIconRel}"; Tasks: startmenuicon

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  UninstallRoot: string;
  Keys: TArrayOfString;
  i: Integer;
  Sub, DisplayName: string;
begin
  if CurStep = ssInstall then
  begin
    UninstallRoot := 'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall';
    if RegGetSubkeyNames(HKLM, UninstallRoot, Keys) then
      for i := 0 to GetArrayLength(Keys) - 1 do
      begin
        Sub := UninstallRoot + '\' + Keys[i];
        if RegQueryStringValue(HKLM, Sub, 'DisplayName', DisplayName) and
           (DisplayName = '{#AppFullName}') then
          RegDeleteKeyIncludingSubkeys(HKLM, Sub);
      end;
    DeleteFile(ExpandConstant('{app}\Uninstall.exe'));
    DeleteFile(ExpandConstant('{app}\Uninstall.ini'));
    DeleteFile(ExpandConstant('{userstartmenu}\{#AppShortName}.lnk'));
  end;
end;
