---
type: "term"
branch: "Operating Systems"
aliases: ["Atomic File Replacement", "Write-Rename Pattern"]
tags: [os, storage]
status: "developed"
---

# Atomic Write

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **Also known as:** Atomic File Replacement, Write-Rename Pattern

Updating a file so that any observer — including one arriving mid-crash — sees either the complete old content or the complete new content, never a torn mixture. On POSIX systems the standard recipe is write-to-temp → `fsync` → `rename()` over the target, because `rename(2)` within one file system is atomic.

**Context.** Plain in-place writes are *not* atomic: a crash or full disk mid-`write()` leaves a truncated or interleaved file, which is how config files and databases get corrupted. The write-rename pattern is the load-bearing trick under text editors, package managers, and every tool that edits files people can't afford to lose — often paired with a pre-write backup so the change is not only crash-safe but *undoable*. Gotchas: `rename` is only atomic on the same file system (temp file goes next to the target, not in `/tmp`), directory entries need their own `fsync` for durability, and the pattern replaces the inode — hard links and open file handles keep seeing the old file.

## See also

- [[File System]]
- [[Inode]]
- [[Race Condition]]
- [[ACID]]

## Often confused with

- [[ACID]] — transactional atomicity spans many operations rolled back on failure; an atomic write is a single all-or-nothing replacement provided by one file-system operation.

## Further reading

- [Wikipedia: Atomicity (database systems)](https://en.wikipedia.org/wiki/Atomicity_(database_systems))
- [rename(2) — Linux manual page](https://man7.org/linux/man-pages/man2/rename.2.html)
