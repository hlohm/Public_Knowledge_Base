---
type: map
area: Backup & Recovery
status: working
---

# Backup & Recovery

> **Area Map** — taking backups, and the part that actually matters: getting data back.

A backup you have never restored is not a backup. The runbooks here exist so the restore
path is rehearsed before you need it.

## In this area
- **[[borgmatic]]** — declarative front-end over `borg` (dedup, encryption, retention)
- **[[restic]]** — single-binary, encrypted, deduplicated backup to local/SFTP/S3/B2
- **[[rsync-snapshots]]** — hard-link snapshot scheme: plain-directory, no special software to restore

## Runbooks
- **[[Backup Restore Drill]]** — verify you can restore, on a schedule
- **[[Bare Metal Restore]]** — rebuild a host from nothing: disk prep, chroot, bootloader, fstab/LUKS

## See also
- [[Linux Administration]] · [[CLI Tools]]
