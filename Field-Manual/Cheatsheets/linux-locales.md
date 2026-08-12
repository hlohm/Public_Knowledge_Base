---
type: cheatsheet
area: "Linux Administration"
aliases: [locale, locales, LC_ALL, LANG, i18n]
tags: [linux, locale, i18n, l10n]
status: working
---

# linux-locales

> **Area:** [[Linux Administration]]

Locales control language, date/time, number, and collation behavior per process, via
environment variables. Most "why is this app showing the wrong format" problems come down
to which variable a given program actually reads.

---

## 1. The variables & precedence

```
LC_ALL          # overrides everything (debug/force only — don't set permanently)
LC_<CATEGORY>   # per-category override
LANG            # default for all categories not otherwise set
```

Precedence per category: `LC_ALL` > `LC_<CATEGORY>` > `LANG`.

| Category | Controls |
| --- | --- |
| `LC_MESSAGES` | UI language of programs |
| `LC_TIME` | date/time formats (12h/24h, day names) |
| `LC_NUMERIC` | decimal separator, grouping |
| `LC_MONETARY` | currency formats |
| `LC_COLLATE` | sort order (affects `sort`, globbing, `[a-z]` ranges!) |
| `LC_CTYPE` | character classification, encoding |
| `LC_PAPER`, `LC_MEASUREMENT`, `LC_NAME`, `LC_ADDRESS`, `LC_TELEPHONE`, `LC_IDENTIFICATION` | mostly cosmetic |

Desktop "Region & Formats" settings panels typically set only the format categories
(`LC_TIME`, `LC_NUMERIC`, …) and leave `LANG`/`LC_MESSAGES` on the UI language — a valid
mixed setup, but the source of the gotchas in §4.

## 2. Inspect

```bash
locale                  # effective settings for this session ("..." = inherited from LANG)
locale -a               # locales actually generated/available on this system
localectl status        # system-wide default (systemd)
env | grep -Ei 'lang|lc_'
locale -k LC_TIME       # dump the actual format strings of the active LC_TIME
```

## 3. Generate & set

```bash
# Arch/Debian-style: uncomment wanted locales, then generate
sudoedit /etc/locale.gen        # e.g. en_DK.UTF-8 UTF-8
sudo locale-gen

# Debian/Ubuntu alternative
sudo dpkg-reconfigure locales

# System-wide default
sudo localectl set-locale LANG=en_US.UTF-8 LC_TIME=de_DE.UTF-8

# Per-session / per-command
LC_TIME=de_DE.UTF-8 date
LC_ALL=C sort file      # bytewise sort, reproducible scripts
```

`LC_ALL=C` (or `C.UTF-8`) in scripts pins predictable parsing/sorting regardless of the
user's locale — standard practice for anything that parses command output.

## 4. Gotchas

- **Chromium/Electron apps ignore `LC_TIME`.** They derive their entire locale (UI *and*
  `Intl` date/number formatting) from `LC_ALL` → `LC_MESSAGES` → `LANG`. With
  `LANG=en_US.UTF-8` + `LC_TIME=de_DE.UTF-8` you still get AM/PM in Obsidian, VS Code,
  Signal, etc. Verify in the app's devtools console: `navigator.language`.
- **English UI + 24h/European formats:** use a locale whose *language* is English but whose
  *formats* aren't US — `en_DK.UTF-8` (the classic "English + ISO" hack) or `en_GB.UTF-8`.
  Setting just `LC_MESSAGES` is enough for Electron and doesn't clobber the rest:

  ```bash
  LC_MESSAGES=en_DK.UTF-8 obsidian
  ```

  Permanent, app-scoped (survives session locale untouched):

  ```bash
  cp /usr/share/applications/obsidian.desktop ~/.local/share/applications/
  # Exec=env LC_MESSAGES=en_DK.UTF-8 obsidian %u
  ```

  Note: copied desktop entries shadow the packaged one and silently outlive reinstalls —
  document or you'll forget why it behaves differently.
- **Flatpaks have their own environment** — the session's `LC_*` may not propagate as
  expected. Inspect and override per-app:

  ```bash
  flatpak override --show md.obsidian.Obsidian
  flatpak override --user --env=LC_MESSAGES=en_DK.UTF-8 md.obsidian.Obsidian
  ```
- **"Cannot set LC_ALL to default locale"** / perl locale warnings ⇒ the requested locale
  isn't generated — fix with §3, not by exporting `LC_ALL=C` everywhere.
- **`LC_COLLATE` changes `sort` and bracket ranges**: `[a-z]` may match uppercase letters
  in non-C locales. Another reason for `LC_ALL=C` in scripts.
- Remote sessions: SSH clients often forward `LANG`/`LC_*` (`SendEnv`); a server missing
  that locale then warns on every login — generate it server-side or stop forwarding
  (`AcceptEnv`).
