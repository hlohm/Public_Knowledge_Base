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
- **[[systemd.exec]]** *(unit hardening / sandboxing)*
- **[[filesystems]]** — the landscape & decision reference: ext4/XFS/Btrfs/ZFS, interchange (exFAT/NTFS), network (NFS/SMB), special-purpose (tmpfs/overlayfs)
- **[[btrfs]]** *(incl. snapper)*
- **[[linux-fhs]]** — the directory tree & layout conventions: FHS top-level map, `/etc` drop-in patterns, `/var` triage, where to put your own scripts/services/data, XDG user dirs
- **[[linux-users]]** — `useradd`, groups, `sudo`, file modes, ACLs, PAM
- **[[linux-packages]]** — apt / dnf / pacman / apk side by side
- **[[linux-networking]]** — `ip`, `ss`, `nmcli`, routing, DNS resolution
- **[[linux-processes]]** — `ps`, `top`/`htop`, `nice`, load, I/O, OOM signals
- **[[linux-storage]]** — `lsblk`, `mount`, fstab, LVM, SMART
- **[[linux-logging]]** — journalctl, /var/log, logrotate, rsyslog forwarding
- **[[linux-timers]]** — crontab, `at`, systemd timer units
- SSH server hardening — see runbook below *(client-side in [[ssh]])*

## Playbooks
- **[[Service Down — Triage & Recovery]]**
- **[[Agentic AI Sandboxing]]** — contain an autonomous LLM agent: profile selection (dirty workshop / curator / vendor-hosted / computer use), enforcement-plane rules, adversarial verification
- **[[Unix OS Hardening]]** — decision-tree hardening reference across all Unix families (Linux, BSDs, macOS), every threat model (TM0–TM3), and every form factor (server, VM, cloud, container host, appliance, workstation, laptop, embedded)
- **[[Disk Full]]** — find the culprit, free space, prevent recurrence
- **[[Out of Memory]]** — OOM killer, swap pressure, leak investigation, cgroup limits
- **[[SSH Key Management]]** — provisioning, rotation, offboarding, compromise response, fleet audit, CA-signed certs

## Runbooks
- **[[SSH Server Hardening]]** — sshd_config, keys-only, algorithm whitelist, fail2ban
- **[[Hardened Syncthing Node on an Untrusted Host]]** — deploy a sandboxed, receive-encrypted [[syncthing]] node on hardware you don't trust
- **[[Hardened Golden Base Image for a Single-Purpose Host]]** — reproducible, sandboxed, firewalled base image you can clone fast and trust

## Snippets
- **[[systemd Service and Timer]]**
- **[[Swap File Setup]]** — add swap to a running system; swappiness tuning; Btrfs gotcha

## See also
- [[Networking & Protocols]] · [[Containers]] · [[Backup & Recovery]]
