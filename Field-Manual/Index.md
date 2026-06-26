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
- **[[systemd]]** · users & permissions · package management (apt/dnf/pacman) · networking (ip/ss/nmcli) · storage (lsblk/mount/LVM) · processes & performance (ps/top/htop) · logging & journald · cron & timers · SSH server hardening
- playbooks: **[[Service Down — Triage & Recovery]]** · disk full · out of memory
- snippets: **[[systemd Service and Timer]]**

### [[Windows Administration]]
- PowerShell · winget · services & scheduled tasks · event logs · WSL

### [[Programming Languages]]
- Python · C · Java · Perl · JavaScript · SQL

### [[Networking & Protocols]]
- **[[ssh]]** · DNS (dig/host) · HTTP (curl) · (S)FTP/SCP · TLS/openssl · **[[nc]]** (netcat)

## By type

- **Cheatsheets:** [[bash]] · [[borgmatic]] · [[docker]] · [[git]] · [[nc]] · [[nvim]] · [[ssh]] · [[systemd]] · [[tmux]]
- **Runbooks:** [[Backup Restore Drill]]
- **Playbooks:** [[Service Down — Triage & Recovery]]
- **Snippets:** [[Bash Strict Mode Header]] · [[systemd Service and Timer]]

## Roadmap notes

- The everyday spine is seeded; the next highest-value additions are **curl**, **rsync**,
  and a **Linux Administration** split (users/permissions, packages, networking).
- Languages start as one solid sheet each (the 80% you reach for), then split into
  sub-notes as they grow — see [[How to Extend]].
