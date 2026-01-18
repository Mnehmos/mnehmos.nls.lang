# NLS File Association Installer for Windows
# Run as Administrator: powershell -ExecutionPolicy Bypass -File install-file-association.ps1

param(
    [string]$IconPath,
    [switch]$Uninstall,
    [switch]$CurrentUser
)

$ErrorActionPreference = "Stop"

# Determine icon path
if (-not $IconPath) {
    # Look for icon in common locations
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $possiblePaths = @(
        "$scriptDir\nls-file.ico",
        "$env:LOCALAPPDATA\Programs\nlsc\nls-file.ico",
        "$env:ProgramFiles\nlsc\nls-file.ico"
    )

    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            $IconPath = $path
            break
        }
    }

    if (-not $IconPath) {
        Write-Error "Could not find nls-file.ico. Please specify path with -IconPath"
        exit 1
    }
}

# Normalize path
$IconPath = (Resolve-Path $IconPath).Path

Write-Host "Using icon: $IconPath"

# Determine registry root
if ($CurrentUser) {
    $regRoot = "HKCU:"
    $rootName = "HKEY_CURRENT_USER"
    Write-Host "Installing for current user only..."
} else {
    $regRoot = "HKLM:"
    $rootName = "HKEY_LOCAL_MACHINE"

    # Check for admin rights
    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
    if (-not $isAdmin) {
        Write-Error "Administrator rights required for system-wide installation. Run as Administrator or use -CurrentUser flag."
        exit 1
    }
    Write-Host "Installing system-wide..."
}

$extKey = "$regRoot\SOFTWARE\Classes\.nl"
$progIdKey = "$regRoot\SOFTWARE\Classes\NLSFile"

if ($Uninstall) {
    Write-Host "Uninstalling NLS file association..."

    if (Test-Path $extKey) {
        Remove-Item -Path $extKey -Recurse -Force
        Write-Host "Removed .nl extension registration"
    }

    if (Test-Path $progIdKey) {
        Remove-Item -Path $progIdKey -Recurse -Force
        Write-Host "Removed NLSFile ProgID"
    }

    Write-Host "Uninstall complete. You may need to restart Explorer or log out/in."
    exit 0
}

Write-Host "Installing NLS file association..."

# Create .nl extension key
if (-not (Test-Path $extKey)) {
    New-Item -Path $extKey -Force | Out-Null
}
Set-ItemProperty -Path $extKey -Name "(Default)" -Value "NLSFile"
Set-ItemProperty -Path $extKey -Name "Content Type" -Value "text/plain"
Set-ItemProperty -Path $extKey -Name "PerceivedType" -Value "text"
Write-Host "Created .nl extension registration"

# Create NLSFile ProgID
if (-not (Test-Path $progIdKey)) {
    New-Item -Path $progIdKey -Force | Out-Null
}
Set-ItemProperty -Path $progIdKey -Name "(Default)" -Value "NLS Specification File"

# Create DefaultIcon subkey
$iconKey = "$progIdKey\DefaultIcon"
if (-not (Test-Path $iconKey)) {
    New-Item -Path $iconKey -Force | Out-Null
}
Set-ItemProperty -Path $iconKey -Name "(Default)" -Value "`"$IconPath`""
Write-Host "Set default icon"

# Create shell\open\command for opening with VS Code (optional)
$openKey = "$progIdKey\shell\open\command"
$vscodeCmd = ""

# Try to find VS Code
$vscodePaths = @(
    "$env:LOCALAPPDATA\Programs\Microsoft VS Code\Code.exe",
    "$env:ProgramFiles\Microsoft VS Code\Code.exe",
    "code"
)

foreach ($path in $vscodePaths) {
    if ($path -eq "code" -or (Test-Path $path)) {
        if ($path -eq "code") {
            $vscodeCmd = "code `"%1`""
        } else {
            $vscodeCmd = "`"$path`" `"%1`""
        }
        break
    }
}

if ($vscodeCmd) {
    if (-not (Test-Path "$progIdKey\shell\open")) {
        New-Item -Path "$progIdKey\shell\open" -Force | Out-Null
    }
    if (-not (Test-Path $openKey)) {
        New-Item -Path $openKey -Force | Out-Null
    }
    Set-ItemProperty -Path $openKey -Name "(Default)" -Value $vscodeCmd
    Write-Host "Set VS Code as default handler"
}

# Notify shell of changes
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public class Shell32 {
    [DllImport("shell32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    public static extern void SHChangeNotify(int wEventId, int uFlags, IntPtr dwItem1, IntPtr dwItem2);
}
"@

[Shell32]::SHChangeNotify(0x08000000, 0, [IntPtr]::Zero, [IntPtr]::Zero)  # SHCNE_ASSOCCHANGED

Write-Host ""
Write-Host "Installation complete!"
Write-Host "Icon path: $IconPath"
Write-Host ""
Write-Host "If icons don't appear immediately, try:"
Write-Host "  1. Restart Windows Explorer (taskkill /f /im explorer.exe && start explorer)"
Write-Host "  2. Log out and back in"
Write-Host "  3. Clear icon cache: ie4uinit.exe -show"
