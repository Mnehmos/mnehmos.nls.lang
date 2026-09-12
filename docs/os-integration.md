# OS File Association Guide

This guide explains how to associate `.nl` files with your preferred editor on macOS, Windows, and Linux so double-click and context-menu actions open NLS files in the right tool — and how to add "Verify / Compile / Test with NLS" actions that run the toolchain.

## What is provided

| Item | Status |
| --- | --- |
| Windows association + icon (`nlsc assoc`, `--user`, `--uninstall`) | Provided (Windows 10/11) |
| Windows context-menu entries (Verify/Compile) | `.reg` snippet below — copy, edit the path, import |
| Linux MIME type + desktop entry files | Generated: `nlsc assoc --desktop` |
| Linux install commands, Nautilus/Dolphin snippets | Instructions below |
| macOS editor association, Automator Quick Action | Instructions below |
| macOS Quick Look plugin rendering the IR | Not provided (note below) |

## Why File Associations Matter

- Faster local workflow for opening and editing specs.
- More reliable team onboarding when everyone can open `.nl` files consistently.
- Better integration with right-click / "Open With" flows from your OS and file manager.

## Safety Notes

- Prefer opening `.nl` files in text editors or IDEs, not executors.
- Do not configure automatic execution on open.
- Review shell context-menu entries before enabling them system-wide.
- For shared machines, apply per-user associations instead of machine-wide defaults.

## macOS

### Set default app for `.nl`

1. In Finder, select any `.nl` file.
2. Choose **File → Get Info**.
3. In **Open with**, select your editor (for example VS Code).
4. Click **Change All...** to apply to all `.nl` files.

### Finder context-menu integration

- Use **Open With** for one-off choices.
- If your editor installs Finder services (or Quick Actions), enable them in:
  - **System Settings → Privacy & Security → Extensions**

### Quick Action: "Verify with NLS"

1. Open Automator → New → **Quick Action**.
2. Set "Workflow receives current" to **files** in **Finder**.
3. Add **Run Shell Script**, pass input **as arguments**, script:

   ```bash
   for f in "$@"; do
     nlsc verify "$f" --strict || exit 1
   done
   ```

4. Save as "Verify with NLS". The same pattern works for `compile`, `fmt
   --check`, and `ci --test`.

### Quick Look

macOS previews `.nl` files as plain text out of the box. A dedicated Quick
Look plugin that renders the checked IR (`nlsc ir`) is not provided;
`qlmanage -p` on a compiled `.py` shows the generated artifact instead.

### Terminal-friendly approach

You can keep your default app and still launch from terminal:

```bash
open -a "Visual Studio Code" path/to/file.nl
```

## Windows

### Set default app for `.nl`

Option A (quick):

1. Right-click a `.nl` file.
2. Select **Open with → Choose another app**.
3. Pick your editor and check **Always use this app to open .nl files**.

Option B (Settings):

1. Open **Settings → Apps → Default apps**.
2. Search for `.nl` under "Choose defaults by file type".
3. Assign your preferred editor.

### File Explorer context-menu integration

- Editors such as VS Code can add "Open with Code" entries.
- If missing, reinstall or repair the editor and enable shell integration.
- In enterprise environments, prefer installer options that scope context-menu integration per user.

### Verify from command line

```bat
assoc .nl
ftype
```

If you manage associations manually, validate command targets before rollout.

### `nlsc assoc` diagnostics

`nlsc assoc` automates the Windows registry entries for `.nl` files. Add `--json` when the command is driven by scripts or installers and you need stable diagnostics instead of human-readable stderr.

- `EASSOC001` - command invoked on a non-Windows host.
- `EASSOC002` - packaged `nls-file.ico` asset is missing.
- `EASSOC003` - registry write blocked by permissions; retry elevated or use `--user`.
- `EASSOC004` - other registry or shell-notification failure.

### Context-menu entries (Verify / Compile)

Save the snippet below as `nls-menu.reg`, replace `C:\Path\To\nlsc.exe`
with your launcher (or `pythonw.exe -m nlsc`), and double-click to import.
It registers per-user entries so no admin rights are required:

```reg
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\.nl\shell\NLSVerify]
@="Verify with NLS"
[HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\.nl\shell\NLSVerify\command]
@="\"C:\\Path\\To\\nlsc.exe\" verify \"%1\""

[HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\.nl\shell\NLSCompile]
@="Compile with NLS"
[HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\.nl\shell\NLSCompile\command]
@="\"C:\\Path\\To\\nlsc.exe\" compile \"%1\""
```

## Linux

Linux behavior depends on desktop environment (GNOME, KDE, etc.) and `xdg` defaults.

### Set default app for `.nl` with GUI

1. Right-click a `.nl` file in your file manager.
2. Open **Properties** (or **File Type Options**).
3. Choose your editor as the default application.

### Set default app with `xdg-mime`

1. Identify the MIME type currently used for `.nl` files.
2. Bind that MIME type to your editor desktop entry.

Typical commands:

```bash
xdg-mime query filetype example.nl
xdg-mime default code.desktop text/plain
```

If your environment uses a custom MIME mapping for `.nl`, apply the association to that MIME type instead of `text/plain`.

### Context-menu/editor integration

- Ensure your editor has a valid `.desktop` file.
- For custom editors, add a `.desktop` entry in `~/.local/share/applications/`.
- Refresh desktop caches or restart the file manager if menu entries do not appear immediately.

### NLS MIME type and desktop actions

`nlsc assoc --desktop` generates the two files that make NLS actions
appear in file managers (the command runs on any OS, so you can generate
and commit them from anywhere):

```bash
nlsc assoc --desktop --output build/desktop-integration
```

- `nlsc.desktop` — application entry with **Verify**, **Compile**, and
  **Test** actions bound to `nlsc verify/compile/test %f`;
- `text-x-nls.xml` — shared-mime-info definition for the `text/x-nls`
  MIME type (`*.nl` glob).

Install:

```bash
mkdir -p ~/.local/share/applications ~/.local/share/mime/packages
cp nlsc.desktop ~/.local/share/applications/
cp text-x-nls.xml ~/.local/share/mime/packages/
update-mime-database ~/.local/share/mime
update-desktop-database ~/.local/share/applications
xdg-mime default nlsc.desktop text/x-nls     # default app (optional)
```

### Nautilus scripts (GNOME)

Drop executable scripts in `~/.local/share/nautilus/scripts/`:

```bash
#!/usr/bin/env bash
# ~/.local/share/nautilus/scripts/Verify with NLS
for f in "$@"; do nlsc verify "$f" --strict; done
read -n 1 -s -r -p "Press any key to close..."
```

### Dolphin service menu (KDE)

Create `~/.local/share/kio/servicemenus/nls-verify.desktop`:

```ini
[Desktop Entry]
Type=Service
ServiceTypes=KonqPopupMenu/Plugin
MimeType=text/x-nls;
Actions=nlsVerify;

[Desktop Action nlsVerify]
Name=Verify with NLS
Exec=konsole --hold -e nlsc verify %F
```

## Recommended Editor Workflow

- Use a single team-standard editor for docs and examples.
- Keep NLS syntax tooling enabled where available (for example [VS Code extension guide](https://github.com/Mnehmos/mnehmos.nls.lang/blob/main/vscode-nls/README.md)).
- Combine OS associations with project tooling:
  - `nlsc compile ...`
  - `nlsc test ...`
  - `nlsc watch ...`

## Pairing associations with the toolchain

Context-menu and Quick Action entries are most useful when they run the
quality gates, not just open files:

- `nlsc verify <file> --strict` — fail fast on unresolved or unproven content.
- `nlsc fmt --check <file>` — canonical formatting guard (`nlsc fmt` fixes it).
- `nlsc lint <file>` — intent-quality review before sharing a spec.
- `nlsc ci <file> --compile --test` — the full CI gate, no OS integration required.

## Troubleshooting

- **Double-click opens wrong app**: reset default app for `.nl` and retry.
- **Context-menu action missing**: reinstall editor with shell integration enabled.
- **Linux app does not appear**: verify `.desktop` file validity and MIME bindings.
- **Managed/enterprise device**: check policy restrictions for default apps and shell extensions.
