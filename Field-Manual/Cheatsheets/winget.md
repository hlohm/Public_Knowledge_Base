---
type: cheatsheet
area: "Windows Administration"
aliases: [Windows Package Manager]
tags: [windows, packages, winget, software]
status: working
---

# winget

> **Area:** [[Windows Administration]]

Windows Package Manager (`winget`) — the official Microsoft CLI for installing, updating, and managing software on Windows. Available in Windows 10 1709+ and Windows 11.

---

## 1. Search and install

```powershell
winget search firefox               # search for packages
winget search --id "Mozilla.Firefox"  # search by exact ID
winget install Mozilla.Firefox      # install (interactive)
winget install --id Mozilla.Firefox --silent    # silent (no UI)
winget install --id Mozilla.Firefox --version 115.0  # specific version
winget install --exact Mozilla.Firefox              # exact ID match (no fuzzy)

# Install from a manifest file
winget install --manifest ./manifest.yaml

# Install multiple packages
winget install Microsoft.VisualStudioCode Git.Git Mozilla.Firefox
```

## 2. List and upgrade

```powershell
winget list                         # all installed packages known to winget
winget list --name "Firefox"        # filter installed list
winget upgrade                      # list all packages with available upgrades
winget upgrade --all                # upgrade everything (be cautious)
winget upgrade --id Mozilla.Firefox # upgrade one package
winget upgrade --id Mozilla.Firefox --silent

# Pin a version (prevent upgrade)
winget pin add --id Mozilla.Firefox --version 115.0
winget pin list
winget pin remove --id Mozilla.Firefox
```

## 3. Remove and export

```powershell
winget uninstall --id Mozilla.Firefox
winget uninstall --id Mozilla.Firefox --silent --purge   # purge removes app data

# Export installed packages to a JSON file (for reprovisioning a new machine)
winget export -o packages.json
winget export -o packages.json --include-versions   # pin current versions

# Import and install from a JSON file (reprovisioning)
winget import -i packages.json
winget import -i packages.json --ignore-unavailable  # skip packages not found
```

## 4. Show package information

```powershell
winget show Mozilla.Firefox         # full package metadata
winget show --id Mozilla.Firefox --versions   # list all available versions
```

## 5. Sources

```powershell
winget source list                  # configured package sources
winget source update                # refresh all source indexes
winget source add --name mycorp --arg https://myserver/winget/  # add a custom source
winget source remove --name mycorp
winget source reset --force         # reset to defaults (msstore + winget)
```

## 6. Settings and configuration

```powershell
winget settings             # open settings.json in default editor
# Location: %LOCALAPPDATA%\Packages\Microsoft.DesktopAppInstaller_...\LocalState\settings.json

# Useful settings:
# {
#   "visual": { "progressBar": "rainbow" },
#   "installBehavior": { "preferences": { "scope": "machine" } }  // machine-wide by default
# }
```

---

## Daily workflows

### "Provision a dev machine"
```powershell
winget import -i dev-packages.json --ignore-unavailable
```

### "Update everything silently (in a maintenance script)"
```powershell
winget upgrade --all --silent --include-unknown
```

### "Find the package ID for something you want to install"
```powershell
winget search 'visual studio code'
# Then use the Id column value:
winget install Microsoft.VisualStudioCode
```

### "Export current packages before a reinstall"
```powershell
winget export -o ~/backup/packages-$(Get-Date -Format yyyyMMdd).json --include-versions
```

## Gotchas / Golden rules

1. **Package IDs are not the display names** — use `winget search` to find the ID; `winget install "Visual Studio Code"` may match multiple packages; `winget install --id Microsoft.VisualStudioCode --exact` is unambiguous.
2. **`--scope machine` requires admin** — user-scope installs go to `%LOCALAPPDATA%`; machine-scope installs to `Program Files`; run as admin for system-wide installs.
3. **`winget upgrade --all` includes apps not originally installed by winget** — it picks up detected apps; some updates may be disruptive; review `winget upgrade` before running `--all` on a production machine.
4. **Packages from the Microsoft Store require authentication** — Store-sourced packages may prompt for sign-in; use the `winget` source (not `msstore`) when scripting.
5. **winget is not available in WinPE or Server Core by default** — App Installer must be installed separately; use Chocolatey or manual installers in those environments.
