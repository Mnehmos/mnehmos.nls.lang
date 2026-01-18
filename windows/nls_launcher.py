"""
NLS File Launcher
A minimal launcher that opens .nl files with VS Code while displaying the NLS icon.
"""
import subprocess
import sys
import os

def main():
    if len(sys.argv) < 2:
        # No file provided, just show info
        print("NLS File Launcher")
        print("Usage: nls_launcher.exe <file.nl>")
        return

    file_path = sys.argv[1]

    # Try VS Code first, fall back to notepad
    editors = [
        "code",  # VS Code in PATH
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"),
        os.path.expandvars(r"%PROGRAMFILES%\Microsoft VS Code\Code.exe"),
        "notepad",  # Fallback
    ]

    for editor in editors:
        try:
            # Use shell=True for 'code' command, False for full paths
            if editor == "code" or editor == "notepad":
                subprocess.Popen([editor, file_path], shell=True)
            else:
                if os.path.exists(editor):
                    subprocess.Popen([editor, file_path])
                else:
                    continue
            return
        except Exception:
            continue

    # If all else fails, use os.startfile
    os.startfile(file_path)

if __name__ == "__main__":
    main()
