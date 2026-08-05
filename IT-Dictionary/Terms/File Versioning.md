---
type: "term"
branch: "DevOps & SRE"
aliases: ["File Version History", "Versioning File System"]
tags: ["devops", "backup"]
status: "developed"
---

# File Versioning

> **Branch:** [[12 - DevOps & SRE|DevOps & SRE]]
> **Also known as:** File Version History, Versioning File System

Automatically keeping superseded copies of individual files as they change or get deleted, so any single file can be rolled back to a recent state without a restore operation. Found in sync tools (Syncthing's trash-can/simple/staggered schemes, Dropbox version history), snapshotting file systems (ZFS, Btrfs), and Windows VSS.

**Context.** This is the *fat-finger layer*, not the disaster layer: it answers "I just overwrote/deleted one file" in seconds, while real [[Backup]] answers "the machine is gone." Two design points matter. **Where it runs:** in a sync mesh, versioning captures changes *arriving from peers*, so it belongs on an always-on node that receives everything — versions then accumulate locally on that node, outside the synced tree. **How it prunes:** staggered schemes thin old versions out over time (keep every version from the last hour, hourly for a day, daily for a month…), bounding disk growth while keeping recent history dense, where it's actually needed. The failure mode to avoid is mistaking it for backup — versioning shares the fate of the medium it lives on and protects nothing against ransomware or disk loss.

## See also

- [[Immutable Backup]]
- [[Version Control]]
- [[Rollback]]
- [[Replication]]

## Often confused with

- [[Version Control]] — deliberate, commented commits of a working tree; file versioning is automatic, per-file, and invisible until you need it.
- [[Backup]] — an independent, restorable copy on separate media with its own retention; versioning is a convenience recovery layer on the same system.

## Further reading

- [Wikipedia: Versioning file system](https://en.wikipedia.org/wiki/Versioning_file_system)
- [Syncthing documentation: File Versioning](https://docs.syncthing.net/users/versioning.html)
