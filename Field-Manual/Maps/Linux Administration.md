---
type: map
area: Linux Administration
status: working
---

# Linux Administration

> **Area Map** — running and keeping a Linux host healthy.

This is an **area, not a single sheet** — each sub-topic gets its own focused note as it
grows (see [[How to Extend]]).

## In this area
- **[[systemd]]** — services, units, timers, journald (`systemctl` / `journalctl`)
- users & permissions — `useradd`, groups, `sudo`, file modes & ACLs
- package management — apt / dnf / pacman side by side
- networking — `ip`, `ss`, `nmcli`, routing, DNS resolution
- storage — `lsblk`, `mount`, fstab, LVM, filesystems
- processes & performance — `ps`, `top`/`htop`, `nice`, load, OOM
- logging & journald — querying and pruning logs *(also in [[systemd]])*
- cron & timers — scheduling (cron vs systemd timers)
- SSH server hardening — `sshd_config`, keys-only, fail2ban *(client in [[ssh]])*

## Playbooks
- **[[Service Down — Triage & Recovery]]**
- disk full — find it, free it, prevent it
- out of memory — the OOM killer and how to read it

## Boilerplate
- **[[systemd Service and Timer]]**

## See also
- [[Networking & Protocols]] · [[Containers]] · [[Backup & Recovery]]
