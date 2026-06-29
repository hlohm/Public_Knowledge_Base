---
type: reference
tags: [reference, index]
status: working
---

# Index

Everything in the vault, plus the backlog. **Bold** = written; plain = ghost/backlog
(a name parked for a future note — see [[How to Extend]]). Reorder and extend to match
what you actually run into; it's a checklist, not a contract.

## By area

### [[Shells & Scripting]]
- **[[bash]]** · sh · zsh · fish · PowerShell *(see [[Windows Administration]])*
- snippets: **[[Bash Strict Mode Header]]** · argument-parsing skeleton · getopts template

### [[CLI Tools]]
- **[[git]]** · **[[nvim]]** · **[[tmux]]** · curl · jq · rsync · fzf · ripgrep · find · sed · awk · tar

### [[Containers]]
- **[[docker]]** *(incl. Compose)* · podman · kubectl · Dockerfile patterns

### [[Backup & Recovery]]
- **[[borgmatic]]** · restic · rsync snapshots
- runbooks: **[[Backup Restore Drill]]** · bare-metal restore

### [[Linux Administration]]
- **[[systemd]]** · [[systemd.exec]] *(unit hardening / sandboxing)* · **[[btrfs]]** *(incl. snapper)* · users & permissions · package management (apt/dnf/pacman) · networking (ip/ss/nmcli) · storage (lsblk/mount/LVM) · processes & performance (ps/top/htop) · logging & journald · cron & timers · SSH server hardening
- playbooks: **[[Service Down — Triage & Recovery]]** · disk full · out of memory
- runbooks: **[[Hardened Syncthing Node on an Untrusted Host]]** · [[Hardened Golden Base Image for a Single-Purpose Host]]
- snippets: **[[systemd Service and Timer]]**

### [[Windows Administration]]
- PowerShell · winget · services & scheduled tasks · event logs · WSL

### [[Programming Languages]]
- Python · C · Java · Perl · JavaScript · SQL

### [[Networking & Protocols]]
- **[[ssh]]** · DNS (dig/host) · HTTP (curl) · (S)FTP/SCP · TLS/openssl · **[[nc]]** (netcat) · **[[syncthing]]**

## By type

- **Cheatsheets:** [[bash]] · [[borgmatic]] · [[btrfs]] · [[docker]] · [[git]] · [[nc]] · [[nvim]] · [[ssh]] · [[syncthing]] · [[systemd]] · [[systemd.exec]] · [[tmux]]
- **Runbooks:** [[Backup Restore Drill]] · [[Hardened Syncthing Node on an Untrusted Host]] · [[Hardened Golden Base Image for a Single-Purpose Host]]
- **Playbooks:** [[Service Down — Triage & Recovery]] · [[Unix OS Hardening]] · [[Windows OS Hardening]] · [[Network Infrastructure Hardening]]
- **Snippets:** [[Bash Strict Mode Header]] · [[systemd Service and Timer]]

## Roadmap notes

- The everyday spine is seeded; the next highest-value additions are **curl**, **rsync**,
  and a **Linux Administration** split (users/permissions, packages, networking).
- Languages start as one solid sheet each (the 80% you reach for), then split into
  sub-notes as they grow — see [[How to Extend]].
