---
type: "term"
branch: "Operating Systems"
de: "Dateisystem"
tags: [os, fundamental]
status: "developed"
---

# File System

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **German:** Dateisystem

The scheme an OS uses to organise data on storage into files and directories, tracking names, locations, sizes, permissions, and timestamps.

**Context.** Journaling file systems (ext4, NTFS) log intended changes first so a crash mid-write leaves a recoverable state, not corruption. Copy-on-write systems (ZFS, Btrfs) add snapshots and checksums on top.

## See also

- [[Inode]]
- [[Journaling]]
- [[Atomic Write]]
- [[Mount]]
- [[Permissions]]
- [[FUSE]]
- [[ZFS]]

## Further reading

- [Wikipedia: File system](https://en.wikipedia.org/wiki/File_system)
