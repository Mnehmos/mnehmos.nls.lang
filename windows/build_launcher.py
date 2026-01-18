"""
Build script for NLS Launcher executable.
Creates a small .exe with the NLS icon embedded.
"""
import subprocess
import sys
import shutil
from pathlib import Path

def main():
    script_dir = Path(__file__).parent
    launcher_py = script_dir / "nls_launcher.py"
    icon_file = script_dir / "nls-file.ico"
    output_dir = script_dir / "dist"

    if not icon_file.exists():
        print(f"Error: Icon file not found at {icon_file}")
        sys.exit(1)

    print("Building NLS Launcher...")
    print(f"  Script: {launcher_py}")
    print(f"  Icon: {icon_file}")

    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",           # Single exe
        "--windowed",          # No console window
        "--name", "nls_launcher",
        "--icon", str(icon_file),
        "--distpath", str(output_dir),
        "--workpath", str(script_dir / "build"),
        "--specpath", str(script_dir),
        str(launcher_py),
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"\nSuccess! Launcher built at: {output_dir / 'nls_launcher.exe'}")

        # Copy to a standard location
        install_path = Path.home() / "AppData" / "Local" / "nlsc"
        install_path.mkdir(parents=True, exist_ok=True)

        src = output_dir / "nls_launcher.exe"
        dst = install_path / "nls_launcher.exe"
        shutil.copy2(src, dst)
        print(f"Installed to: {dst}")

        print("\nTo complete setup, run in elevated PowerShell:")
        print(f'''
Set-ItemProperty -Path 'HKLM:\\Software\\Classes\\NLSFile\\shell\\open\\command' -Name '(Default)' -Value '"{dst}" "%1"'
Set-ItemProperty -Path 'HKLM:\\Software\\Classes\\NLSFile\\DefaultIcon' -Name '(Default)' -Value '"{dst}",0'
''')

    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("PyInstaller not found. Install with: pip install pyinstaller")
        sys.exit(1)

if __name__ == "__main__":
    main()
