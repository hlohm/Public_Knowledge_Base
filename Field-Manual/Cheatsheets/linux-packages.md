---
type: cheatsheet
area: "Linux Administration"
aliases: [apt, dnf, pacman, package management, yum]
tags: [linux, packages, apt, dnf, pacman, pkg]
status: working
---

# Package Management

> **Area:** [[Linux Administration]]

Package management across the major Linux families: apt (Debian/Ubuntu), dnf (RHEL/Fedora/Rocky), pacman (Arch), and Alpine's apk. Side-by-side so you can translate between them.

---

## apt (Debian / Ubuntu / Mint)

```bash
# Update & upgrade
apt update                         # refresh package index (always do this first)
apt upgrade                        # upgrade all packages to latest available
apt full-upgrade                   # upgrade + remove obsolete packages (was dist-upgrade)
apt autoremove                     # remove orphaned packages no longer needed

# Install & remove
apt install nginx                  # install
apt install nginx=1.24.*           # specific version
apt install --no-install-recommends nginx  # skip recommended extras
apt remove nginx                   # remove package (keep config files)
apt purge nginx                    # remove package + config files
apt reinstall nginx                # reinstall (useful when config is broken)

# Search & info
apt search nginx                   # search package names/descriptions
apt show nginx                     # metadata, dependencies, description
apt-cache policy nginx             # installed version, available versions, sources
apt list --installed               # all installed packages
apt list --installed | grep '^nginx'
dpkg -l nginx                      # installed version, installed/removed status
dpkg -L nginx                      # list files installed by the package
dpkg -S /usr/sbin/nginx            # which package owns this file?
dpkg -x package.deb /tmp/extract/  # extract a .deb without installing

# Sources and repositories
cat /etc/apt/sources.list          # primary sources
ls /etc/apt/sources.list.d/        # drop-in sources
add-apt-repository ppa:team/ppa    # Ubuntu PPA (installs the repo key too)
apt-key list                       # deprecated; GPG keys now in /etc/apt/trusted.gpg.d/
```

## dnf (RHEL 8+ / Fedora / Rocky / AlmaLinux) and yum

`yum` is an alias for `dnf` on modern RHEL; commands are identical.

```bash
# Update & upgrade
dnf check-update                   # check what would be updated
dnf update                         # update all packages
dnf update nginx                   # update one package
dnf upgrade --refresh              # refresh metadata first

# Install & remove
dnf install nginx                  # install
dnf install nginx-1.24.*           # version pattern
dnf remove nginx                   # remove (keep config)
dnf autoremove                     # remove orphaned dependencies
dnf reinstall nginx
dnf downgrade nginx                # downgrade to previous version

# Search & info
dnf search nginx
dnf info nginx                     # full package info
dnf list installed                 # all installed
dnf list installed | grep nginx
rpm -ql nginx                      # list files installed by a package
rpm -qf /usr/sbin/nginx            # which package owns this file?
rpm -qi nginx                      # package info via rpm

# Groups and modules
dnf group list
dnf group install "Development Tools"
dnf module list                    # RHEL/CentOS module streams
dnf module enable nginx:stable
dnf module install nginx:stable/common

# Repositories
dnf repolist                       # list enabled repos
dnf repolist --all                 # all repos (enabled + disabled)
dnf config-manager --enable repo-name
dnf config-manager --add-repo https://example.com/repo.repo

# History and rollback
dnf history                        # transaction log
dnf history info 42                # details of transaction 42
dnf history undo 42                # roll back a transaction
```

## pacman (Arch Linux / Manjaro / EndeavourOS)

```bash
# Update
pacman -Syu                        # sync + update all (do this regularly; Arch is rolling)

# Install & remove
pacman -S nginx                    # install (S = sync)
pacman -U /path/to/pkg.tar.zst    # install a local package file
pacman -R nginx                    # remove (keep dependencies)
pacman -Rs nginx                   # remove + orphaned dependencies
pacman -Rns nginx                  # remove + deps + config files
pacman -Sc                         # clean cache (old package versions)
pacman -Scc                        # clean all cached packages

# Search & info
pacman -Ss nginx                   # search the sync database
pacman -Qs nginx                   # search installed packages
pacman -Si nginx                   # package info (from repo)
pacman -Qi nginx                   # package info (installed)
pacman -Ql nginx                   # list files installed by package
pacman -Qo /usr/bin/nginx          # which package owns this file?
pacman -Qm                         # list AUR / foreign packages
pacman -Qdt                        # list orphaned packages

# AUR helpers (yay, paru — not included in pacman; install separately)
yay -S aur-package
paru -S aur-package
```

## apk (Alpine Linux)

```bash
apk update                         # refresh index
apk upgrade                        # upgrade all
apk add nginx                      # install
apk add nginx=~1.24                # version constraint
apk del nginx                      # remove
apk search nginx                   # search
apk info nginx                     # package info
apk info -L nginx                  # list files owned by package
apk fix                            # repair or reinstall packages

# Repositories: /etc/apk/repositories
# echo "https://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
```

---

## Cross-distro comparison

| Task | apt | dnf | pacman | apk |
|---|---|---|---|---|
| Install | `install` | `install` | `-S` | `add` |
| Remove | `remove` | `remove` | `-R` | `del` |
| Update index | `update` | `check-update` | `-Sy` | `update` |
| Upgrade all | `upgrade` | `update` | `-Syu` | `upgrade` |
| Search | `search` | `search` | `-Ss` | `search` |
| Package info | `show` | `info` | `-Si` | `info` |
| List files | `dpkg -L` | `rpm -ql` | `-Ql` | `info -L` |
| File → package | `dpkg -S` | `rpm -qf` | `-Qo` | `info -W` |
| Remove orphans | `autoremove` | `autoremove` | `-Rns $(pacman -Qdtq)` | N/A |

---

## Daily workflows

### "Fully update a Debian/Ubuntu system"
```bash
apt update && apt full-upgrade && apt autoremove
```

### "Find which package provides a missing command"
```bash
# Debian/Ubuntu
apt-file search nginx      # (requires: apt install apt-file && apt-file update)
dpkg -S $(which nginx)

# RHEL/Fedora
dnf provides */nginx

# Arch
pkgfile nginx              # (requires: pkgfile -u)
```

### "Hold a package at its current version (prevent upgrade)"
```bash
# apt
apt-mark hold nginx
apt-mark unhold nginx

# dnf
dnf versionlock add nginx
dnf versionlock delete nginx

# pacman: edit /etc/pacman.conf → IgnorePkg = nginx
```

## Files & locations

| Path | What |
|---|---|
| `/etc/apt/sources.list` | apt primary sources |
| `/etc/apt/sources.list.d/` | apt drop-in sources |
| `/etc/apt/preferences.d/` | apt pinning (version locking) |
| `/etc/yum.repos.d/` | dnf/yum repo definitions |
| `/etc/pacman.conf` | pacman config and mirrors |
| `/etc/pacman.d/mirrorlist` | Arch mirror list |
| `/etc/apk/repositories` | Alpine repo list |

## Gotchas / Golden rules

1. **Always `apt update` before `apt install`** — installing from a stale index installs outdated packages or fails with "not found."
2. **Arch: never do a partial upgrade** — `pacman -Sy pkg` (sync index, install one package, no full upgrade) breaks the system; always `pacman -Syu`.
3. **`dnf history undo` is your rollback mechanism on RHEL** — capture the transaction ID right after a bad update; the window to roll back is before the next system reboot changes anything.
4. **`apt purge` vs `apt remove`** — `remove` leaves config files so reinstalling restores settings; `purge` removes everything including config. Use `remove` for most cases; `purge` when you want a clean slate.
5. **Package signing** — never add a repository without also importing its signing key; an unsigned repo or a repo with an untrusted key can inject arbitrary packages.
