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
- **[[bash]]** · **[[sh]]** · **[[zsh]]** · **[[fish]]** · PowerShell *(see [[Windows Administration]])*
- snippets: **[[Bash Strict Mode Header]]** · **[[Argument Parsing Skeleton]]** · **[[getopts Template]]**

### [[CLI Tools]]
- **[[git]]** · **[[nvim]]** · **[[tmux]]** · **[[curl]]** · **[[jq]]** · **[[rsync]]** · **[[tar]]** · **[[fzf]]** · **[[ripgrep]]** · **[[find]]** · **[[sed]]** · **[[awk]]** · **[[claude-code]]**

### [[Containers]]
- **[[docker]]** *(incl. Compose)* · **[[podman]]** · **[[kubectl]]** · **[[dockerfile]]**

### [[Backup & Recovery]]
- **[[borgmatic]]** · **[[restic]]** · **[[rsync-snapshots]]**
- runbooks: **[[Backup Restore Drill]]** · **[[Bare Metal Restore]]**

### [[Linux Administration]]
- **[[systemd]]** · **[[systemd.exec]]** · **[[btrfs]]** · **[[linux-users]]** · **[[linux-packages]]** · **[[linux-networking]]** · **[[linux-processes]]** · **[[linux-storage]]** · **[[linux-logging]]** · **[[linux-timers]]**
- playbooks: **[[Service Down — Triage & Recovery]]** · **[[Disk Full]]** · **[[Out of Memory]]** · **[[SSH Key Management]]** · **[[Agentic AI Sandboxing]]**
- runbooks: **[[SSH Server Hardening]]** · **[[Hardened Syncthing Node on an Untrusted Host]]** · [[Hardened Golden Base Image for a Single-Purpose Host]]
- snippets: **[[systemd Service and Timer]]** · **[[Swap File Setup]]**

### [[Windows Administration]]
- **[[powershell]]** · **[[powershell-cmdlets]]** · **[[windows-users]]** · **[[winget]]** · **[[windows-services]]** · **[[windows-events]]** · **[[wsl]]**
- runbooks: **[[Primary Domain Controller — New Forest Setup]]**

### [[Programming Languages]]
- **[[python]]** · **[[javascript]]** · **[[sql]]** · **[[c]]** · **[[java]]** · **[[perl]]**

### [[Networking & Protocols]]
- **[[ssh]]** · **[[ssh_config]]** · **[[dns]]** (dig/host) · HTTP *(see [[curl]])* · **[[scp-sftp]]** · **[[openssl]]** (TLS) · **[[nc]]** (netcat) · **[[syncthing]]**

### [[Writing & Docs]]
- **[[markdown]]** · **[[latex]]** · **[[html]]** · **[[css]]**

## By type

- **Cheatsheets:** [[awk]] · [[bash]] · [[borgmatic]] · [[btrfs]] · [[c]] · [[claude-code]] · [[css]] · [[curl]] · [[dns]] · [[docker]] · [[dockerfile]] · [[find]] · [[fish]] · [[fzf]] · [[git]] · [[html]] · [[java]] · [[javascript]] · [[jq]] · [[kubectl]] · [[latex]] · [[linux-logging]] · [[linux-networking]] · [[linux-packages]] · [[linux-processes]] · [[linux-storage]] · [[linux-timers]] · [[linux-users]] · [[markdown]] · [[nc]] · [[nvim]] · [[openssl]] · [[perl]] · [[podman]] · [[powershell]] · [[powershell-cmdlets]] · [[python]] · [[restic]] · [[ripgrep]] · [[rsync]] · [[rsync-snapshots]] · [[scp-sftp]] · [[sed]] · [[sh]] · [[sql]] · [[ssh]] · [[ssh_config]] · [[syncthing]] · [[systemd]] · [[systemd.exec]] · [[tar]] · [[tmux]] · [[windows-events]] · [[windows-services]] · [[windows-users]] · [[winget]] · [[wsl]] · [[zsh]]
- **Runbooks:** [[Backup Restore Drill]] · [[Bare Metal Restore]] · [[SSH Server Hardening]] · [[Hardened Syncthing Node on an Untrusted Host]] · [[Hardened Golden Base Image for a Single-Purpose Host]] · [[Primary Domain Controller — New Forest Setup]]
- **Playbooks:** [[Service Down — Triage & Recovery]] · [[Disk Full]] · [[Out of Memory]] · [[SSH Key Management]] · [[Unix OS Hardening]] · [[Windows OS Hardening]] · [[Network Infrastructure Hardening]] · [[Agentic AI Sandboxing]]
- **Snippets:** [[Argument Parsing Skeleton]] · [[Bash Strict Mode Header]] · [[getopts Template]] · [[Swap File Setup]] · [[systemd Service and Timer]]

## Roadmap notes

- Languages start as one solid sheet each (the 80% you reach for), then split into
  sub-notes as they grow — see [[How to Extend]].
- Add cheat sheets:
	- nmap