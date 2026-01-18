# Windows File Association for NLS

This folder contains tools to register `.nl` files with Windows Explorer so they display with a custom icon (like Python's `.py` files).

## Quick Install

### Option 1: Windows Installer (Recommended)

Run the installer:

```
windows\installer_output\nls-setup-0.2.0.exe
```

After installation, **complete the icon setup**:
1. Right-click any `.nl` file → **Open with** → **Choose another app**
2. Click **More apps** → **Look for another app on this PC**
3. Navigate to `C:\Program Files (x86)\NLS\nls_launcher.exe`
4. Check **"Always use this app to open .nl files"**
5. Click OK

> **Why is this step needed?** Windows 10 prioritizes "UserChoice" (the app you explicitly choose) over registry-based associations. The installer sets up the registry, but Windows won't display the icon until you "claim" the file type via Open With.

### Option 2: Using nlsc CLI

After installing nlsc, run:

```powershell
# For current user (no admin required)
nlsc assoc --user

# System-wide (requires admin)
nlsc assoc
```

To uninstall:

```powershell
nlsc assoc --uninstall --user
# or
nlsc assoc --uninstall
```

### Option 2: PowerShell Script

```powershell
# Run as Administrator for system-wide, or use -CurrentUser
powershell -ExecutionPolicy Bypass -File windows\install-file-association.ps1

# Current user only (no admin)
powershell -ExecutionPolicy Bypass -File windows\install-file-association.ps1 -CurrentUser

# Uninstall
powershell -ExecutionPolicy Bypass -File windows\install-file-association.ps1 -Uninstall
```

### Option 3: Registry Files

1. Edit the `.reg` file to set the correct icon path
2. Double-click to import:
   - `install-nls-association.reg` - System-wide (requires admin)
   - `install-nls-association-user.reg` - Current user only

To uninstall, use the corresponding uninstall `.reg` file.

## Files

| File | Purpose |
|------|---------|
| `nls_installer.iss` | Inno Setup script for building the installer |
| `nls_launcher.py` | Python source for the launcher executable |
| `build_launcher.py` | Script to build launcher with PyInstaller |
| `installer_output/nls-setup-*.exe` | Built Windows installer |
| `generate_ico.py` | Python script to generate ICO from SVG |
| `nls-file.ico` | Windows icon file (multi-resolution) |
| `install-file-association.ps1` | PowerShell installer (legacy) |
| `install-nls-association.reg` | Registry file for system-wide install (legacy) |
| `install-nls-association-user.reg` | Registry file for current user install (legacy) |
| `uninstall-nls-association.reg` | Registry file to uninstall (system-wide) |
| `uninstall-nls-association-user.reg` | Registry file to uninstall (current user) |

## Icon Generation

If you need to regenerate the icon:

```bash
pip install Pillow
python windows/generate_ico.py
```

For higher quality (requires cairo system library):

```bash
pip install Pillow svglib reportlab
python windows/generate_ico.py
```

## Troubleshooting

### Icons not showing immediately

1. Restart Windows Explorer:
   ```cmd
   taskkill /f /im explorer.exe && start explorer
   ```

2. Or log out and back in

3. Clear icon cache:
   ```cmd
   ie4uinit.exe -show
   ```

### Permission denied

- For system-wide installation, run as Administrator
- Use `--user` flag or `-CurrentUser` for per-user installation

### Generic icon still showing (Windows 10/11)

**This is the most common issue.** Windows 10+ uses "UserChoice" which overrides all registry settings.

**Solution:** Use "Open with" to set the default app:
1. Right-click a `.nl` file → **Open with** → **Choose another app**
2. Browse to `C:\Program Files (x86)\NLS\nls_launcher.exe`
3. Check "Always use this app"
4. Click OK

The icon should appear immediately after this step.

### Other checks

- Ensure the icon path in the registry is correct and the file exists
- Check if another program has claimed the `.nl` extension
