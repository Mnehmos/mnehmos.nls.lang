# OS File Association Guide

This guide explains how to associate `.nl` files with your preferred editor on macOS, Windows, and Linux so double-click and context-menu actions open NLS files in the right tool.

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

## Recommended Editor Workflow

- Use a single team-standard editor for docs and examples.
- Keep NLS syntax tooling enabled where available (for example [VS Code extension guide](https://github.com/Mnehmos/mnehmos.nls.lang/blob/main/vscode-nls/README.md)).
- Combine OS associations with project tooling:
  - `nlsc compile ...`
  - `nlsc test ...`
  - `nlsc watch ...`

## Troubleshooting

- **Double-click opens wrong app**: reset default app for `.nl` and retry.
- **Context-menu action missing**: reinstall editor with shell integration enabled.
- **Linux app does not appear**: verify `.desktop` file validity and MIME bindings.
- **Managed/enterprise device**: check policy restrictions for default apps and shell extensions.
