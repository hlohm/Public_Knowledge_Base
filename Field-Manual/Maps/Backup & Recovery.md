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
- restic — single-binary alternative backup tool
- rsync snapshots — hard-link snapshot scheme

## Runbooks
- **[[Backup Restore Drill]]** — verify you can restore, on a schedule
- bare-metal restore — rebuild a host from nothing

## See also
- [[Linux Administration]] · [[CLI Tools]]
