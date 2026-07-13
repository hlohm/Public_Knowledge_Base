---
type: "term"
branch: "DevOps & SRE"
aliases: ["Append-Only Backup", "WORM Backup"]
tags: ["devops", "backup"]
status: "note"
---

# Immutable Backup

> **Branch:** [[12 - DevOps & SRE|DevOps & SRE]]
> **Also known as:** Append-Only Backup, WORM Backup

A backup that cannot be modified or deleted after it is written, for a defined retention period — enforced by the storage layer itself, not by policy. Object locks (S3 Object Lock / WORM) or an append-only transport restriction mean that even a client holding valid backup credentials can *add* archives but never erase history.

**Context.** This is the control that turns backups into a real ransomware defense. Ordinary backups fail the instant the attacker who owns your servers also owns the backup credentials — modern ransomware deletes or encrypts the backups first, then the production data. Immutability breaks that chain: writing is append-only, and pruning or expiry must run from a *separate, more-trusted context* (a different key), never from the same client that writes. Mind the gap between a *retention policy* (advisory, an admin can override it) and an *object lock* (enforced, survives a compromised admin) — only the latter is a control. Pairs with the [[3-2-1 Rule|3-2-1 rule]] and with [[RPO]]/[[RTO]] planning.

## See also

- [[RPO]]
- [[RTO]]
- [[Ransomware]]
