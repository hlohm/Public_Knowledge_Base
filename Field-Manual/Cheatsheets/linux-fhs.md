---
type: cheatsheet
area: "Linux Administration"
aliases: [fhs, filesystem hierarchy, directory layout, /etc, /var, /opt, xdg]
tags: [linux, fhs, filesystem, conventions, xdg]
status: draft
---

# Filesystem Hierarchy & Layout Conventions

> **Area:** [[Linux Administration]]

Where everything lives and where *your* things belong: the FHS top-level map, the
conventions inside `/etc` and `/var`, and the decision rules for placing scripts,
services, and data. On-disk formats (ext4/btrfs/ZFS) are in [[filesystems]] — this
sheet is about the *tree*, not the disk.

---

## 1. Top-level map

| Path | What lives there | Notes |
| --- | --- | --- |
| `/bin`, `/sbin`, `/lib` *(binaries, system binaries, libraries)* | → symlinks into `/usr` | usr-merge (§2); treat as legacy names |
| `/boot` | kernel, initramfs, bootloader | often a separate (small) partition/ESP |
| `/dev` *(devices)* | device nodes | virtual (devtmpfs), populated by the kernel + udev |
| `/etc` *(“et cetera” — really)* | host-specific **config** | text files; no binaries; §3 |
| `/home` | user home directories | |
| `/media` | auto-mounts for removable media | desktop environments mount here |
| `/mnt` *(mount)* | *your* temporary manual mounts | scratch mountpoint by convention |
| `/opt` *(optional)* | self-contained third-party apps | one dir per vendor/app; §7 |
| `/proc` *(processes)* | process & kernel state | virtual; §6 |
| `/root` | root's home | deliberately not under `/home` |
| `/run` | runtime state since boot | tmpfs; PID files, sockets; §5 |
| `/srv` *(services)* | data *served* by this host | web roots, ftp, sync targets; §7 |
| `/sys` *(system)* | kernel object tree (devices, drivers) | virtual; §6 |
| `/tmp` *(temporary)* | scratch, may vanish on reboot | often tmpfs; §5 |
| `/usr` *(historically “user”)* | the OS: package-manager territory | read-only in spirit — never hand-edit; §7 |
| `/usr/local` | locally installed software | *yours*; mirrors `/usr` layout; §7 |
| `/var` *(variable)* | variable data: logs, caches, app state | grows; watch it; §4 |

**Etymology corner:** `/usr` is not an abbreviation — it originally held *user* home
directories, and the OS grew into the space after homes moved to `/home`. "Unix System
Resources" is a later backronym (a good mnemonic, but not the origin). `/etc` genuinely
is *et cetera* — "everything that fit nowhere else" — and only later hardened into
"the config directory".

## 2. The usr merge

```bash
ls -ld /bin /sbin /lib      # all symlinks → /usr/bin, /usr/sbin(→bin), /usr/lib
```

Modern distros (Arch since 2013, Debian 12+, Fedora, openSUSE) merged the historical
split — `/bin` vs `/usr/bin` dates from a 1970s disk that ran out of space. Practical
consequences: `/usr/bin` is the single real location for executables; scripts with
`#!/bin/sh` or `#!/usr/bin/env bash` both keep working via the symlinks; and there is
no longer a meaningful "essential vs non-essential binary" split at the path level.

## 3. /etc — configuration conventions

```bash
# The .d drop-in pattern: main file + directory of fragments, merged in lexical order
/etc/sysctl.d/99-custom.conf      # number prefix controls order; higher = later = wins
/etc/sudoers.d/deploy             # never edit /etc/sudoers directly — visudo -f the fragment
/etc/systemd/system/foo.service.d/override.conf   # drop-in overrides a packaged unit

# Vendor defaults vs local override (the systemd-era pattern):
/usr/lib/systemd/system/foo.service   # package's version — DON'T edit
/etc/systemd/system/foo.service       # your full replacement (wins over /usr/lib)
systemctl edit foo                    # or: generate a partial drop-in interactively
```

The general rule across modern tools: **defaults ship in `/usr/lib/<tool>/`, local
policy goes in `/etc/<tool>/`**, and `/etc` wins. Package managers respect this —
your `/etc` edits survive upgrades (pacman leaves `.pacnew` files next to changed
configs; merge them: `pacdiff`).

## 4. /var — the directory that grows

| Path | What | Safe to delete? |
| --- | --- | --- |
| `/var/log` | logs, journal (`/var/log/journal`) | rotate, don't `rm` blindly — see [[linux-logging]] |
| `/var/lib` | persistent application **state** (databases, docker, pacman's DB) | **no** — this is the app's memory |
| `/var/cache` | regenerable caches (`pacman/pkg`, apt archives) | yes — `paccache -r`, `apt clean` |
| `/var/spool` | queued work: mail, cron, print | no — it's pending work |
| `/var/tmp` | temp files that must survive reboot | old files, yes |

```bash
du -xh --max-depth=1 /var | sort -h    # where did the space go (-x: stay on this fs)
```

## 5. /run vs /tmp vs /var/tmp

| Path | Backing | Lifetime | Use for |
| --- | --- | --- | --- |
| `/run` | tmpfs | since boot | PID files, sockets, runtime dirs (`/run/user/$UID`) |
| `/tmp` | usually tmpfs | may be wiped on boot *and* by age (systemd-tmpfiles, ~10d) | small scratch |
| `/var/tmp` | real disk | survives reboot; aged out slower (~30d) | large or resumable temp work |

```bash
# tmpfs means RAM — don't unpack a 40 GB archive into /tmp
df -h /tmp /run                        # check backing and size
systemd-tmpfiles --cat-config | less   # who cleans what, and when
```

## 6. /proc and /sys — the kernel, pretending to be files

```bash
cat /proc/cmdline                 # kernel boot parameters
cat /proc/<PID>/environ | tr '\0' '\n'   # a process's environment
ls -l /proc/<PID>/fd              # its open files — instant "what is it touching"
cat /sys/class/net/*/address      # MAC addresses
echo 1 > /sys/class/leds/.../brightness  # writes = live kernel tuning
```

Zero bytes on disk — reads are answered by the kernel at open time. `/proc` is
process-and-kernel state, `/sys` is the device/driver object tree. Persistent
versions of sysctl tweaks go in `/etc/sysctl.d/` (§3), not in shell profiles.

## 7. Where do I put things? — decision table

| Thing | Put it in | Why |
| --- | --- | --- |
| Your own script, just for you | `~/.local/bin` | on PATH (add it if not), no root needed |
| Script/tool for all users | `/usr/local/bin` | FHS-reserved for the admin; PM never touches it |
| Self-built software (`make install`) | `PREFIX=/usr/local` or `PREFIX=~/.local` | mirrors `/usr` layout; uninstallable by prefix |
| Self-contained third-party bundle | `/opt/<name>/` | one dir, one app, easy to nuke |
| Data a service serves | `/srv/<svc>/` | keeps served data off `/home` and out of `/var/lib` |
| A service's internal state | `/var/lib/<svc>/` | conventional; backup tools expect it |
| Host config you wrote | `/etc/` (drop-in dirs, §3) | survives upgrades |

**The one hard rule:** never install into `/usr` directly — that's the package
manager's territory, and your files will be overwritten, orphaned, or will shadow
packaged ones in unpredictable ways. `/usr/local` and `/opt` exist precisely so you
and the PM never fight. (`PATH` puts `/usr/local/bin` first, so a local install
deliberately shadows the packaged version — that part is by design.)

## 8. User-level layout — XDG conventions

| Path | Role | Analogy |
| --- | --- | --- |
| `~/.config/<app>/` | config | your personal `/etc` |
| `~/.local/share/<app>/` | data | your `/usr/share` + `/var/lib` |
| `~/.local/state/<app>/` | logs, history, state | your `/var` |
| `~/.cache/<app>/` | regenerable cache | safe to delete, always |
| `~/.local/bin` | your executables | your `/usr/local/bin` |

Well-behaved tools follow this (override via `$XDG_CONFIG_HOME` etc.); older ones
still litter `~/.<app>` dotfiles. When freeing space or backing up: back up
`.config` + `.local/share` + `.local/state`, skip `.cache`.

---

## Daily workflows

### "Where does this program and its config actually live?"
```bash
type -a foo                  # every foo on PATH, in resolution order
pacman -Qo $(command -v foo) # which package owns the binary (dpkg -S / rpm -qf elsewhere)
pacman -Ql foo | grep etc    # every file the package installed, filtered to config
ls -l /proc/<PID>/fd         # what a *running* instance has open right now
```

### "Install a self-built tool without making a mess"
```bash
git clone <repo> ~/src/<name> && cd ~/src/<name>
PREFIX=~/.local make install       # or PREFIX=/usr/local with sudo, for all users
# no PREFIX support in the Makefile? → copy to ~/.local/bin manually, or use /opt
```

### "Disk filling up — sweep the conventional suspects"
```bash
du -xh --max-depth=1 / 2>/dev/null | sort -h | tail
journalctl --disk-usage && sudo journalctl --vacuum-size=500M
du -sh /var/cache/* ~/.cache | sort -h
```

## Gotchas / Golden rules

1. **`/tmp` is RAM and it evaporates** — tmpfs on most systems, wiped at boot, and systemd-tmpfiles ages files out even between boots. Anything big or precious goes in `/var/tmp` or real storage.
2. **Never hand-edit under `/usr` (including `/usr/lib/systemd`)** — the next upgrade silently reverts it. Override in `/etc`; the whole layout is built so `/etc` wins.
3. **`/var/lib` is state, not cache** — deleting from `/var/cache` costs a re-download; deleting from `/var/lib` costs a database. Know which one you're in before freeing space.
4. **`.d` fragment order is lexical** — `10-foo.conf` loads before `99-bar.conf`, and for most tools *last wins*. An override that "doesn't work" usually just sorts too early.
5. **`df` and `du` disagreeing usually means a deleted-but-open file** — a process still holds the fd, so the space isn't freed. `lsof +L1` finds them; restart the holder (classic with logs).
