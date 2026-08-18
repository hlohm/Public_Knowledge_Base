---
type: "term"
branch: "Internet & Web"
aliases: []
tags: ["web", "net", "email"]
status: "developed"
---

# Maildir

> **Branch:** [[05 - Internet & Web|Internet & Web]]

A mailbox storage format in which every message is a separate file in a directory tree, written in a way that needs no locking.

**Context.** Delivery happens in three steps — write into `tmp/`, then rename into `new/`, then move to `cur/` once read — and because rename is atomic on POSIX filesystems, a reader never sees a half-written message and no lock is required. That is the whole design, and it is why Maildir displaced mbox, where every delivery had to lock one large file and a crash mid-append could corrupt the lot. The costs are filesystem-shaped: many small files, inode pressure, and slow directory scans on very large folders, which is why large providers move to purpose-built stores with their own indexes. Flags are encoded in the filename, so a rename is also how a message is marked read.

## See also

- [[MDA]]
- [[IMAP]]
- [[Atomic Write]]
- [[Email Ecosystem]]

## Further reading

- [Wikipedia: Maildir](https://en.wikipedia.org/wiki/Maildir)
