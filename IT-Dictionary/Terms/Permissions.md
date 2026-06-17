---
type: "term"
branch: "Operating Systems"
aliases: ["File Permissions", "Access Rights"]
de: "Berechtigungen"
tags: [os]
status: "developed"
---

# Permissions

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **Also known as:** File Permissions, Access Rights
> **German:** Berechtigungen

Rules governing who may read, write, or execute a file or directory. Unix encodes these for owner/group/others (the rwx bits).

**Context.** The classic Unix model is coarse; ACLs add per-user grants, and 'least privilege' says grant the minimum needed. A misset permission (world-writable, or 0600 vs 0644 on a key) is a perennial misconfiguration.

## See also

- [[setuid]]
- [[Capabilities]]
- [[Least Privilege]]

## Further reading

- [Wikipedia: File-system permissions](https://en.wikipedia.org/wiki/File-system_permissions)
