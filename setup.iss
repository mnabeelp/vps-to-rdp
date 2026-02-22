[Setup]
AppName=VPS to RDP Wizard
AppVersion=1.0
DefaultDirName={autopf}\VPS to RDP Wizard
DefaultGroupName=VPS to RDP Wizard
UninstallDisplayIcon={app}\VPS-RDPMaster.exe
Compression=lzma2
SolidCompression=yes
OutputDir=Output
OutputBaseFilename=VPS-RDPMaster-Setup
PrivilegesRequired=lowest

[Files]
Source: "dist\VPS-RDPMaster.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\VPS to RDP Wizard"; Filename: "{app}\VPS-RDPMaster.exe"
Name: "{autodesktop}\VPS to RDP Wizard"; Filename: "{app}\VPS-RDPMaster.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\VPS-RDPMaster.exe"; Description: "Launch VPS to RDP Wizard"; Flags: nowait postinstall skipifsilent
