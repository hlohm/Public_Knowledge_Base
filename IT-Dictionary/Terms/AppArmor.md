---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
tags: ["endpoint"]
status: "developed"
---

# AppArmor

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]

A path-based [[Mandatory Access Control]] [[LSM]]: per-program profiles declare which file paths, [[Capabilities]], and network operations a program may use. The default MAC on SUSE and Ubuntu (and Debian since 10).

**Context.** Identifying programs and resources by *pathname* is AppArmor's whole trade. The win: profiles are readable, writable by mortals, and need no filesystem relabeling. The cost: a path is a *name* for an object, not the object itself — hard links, bind mounts, and renames can change which rules apply to the same inode — and there is no system-wide information-flow picture to query. Coverage is opt-in: only binaries with profiles are confined; everything else runs unconfined. *Enforce* mode blocks; *complain* mode logs only — the profile-development loop (`aa-logprof` turns the log into rules). The standing deployment contrast: [[SELinux]] optimizes for analyzable completeness, AppArmor for administrator ergonomics — which is most of why Ubuntu and SUSE chose it.

## See also

- [[SELinux]]
- [[LSM]]
- [[Mandatory Access Control]]
- [[Hardening]]
- [[Container Security]]

## Often confused with

- [[SELinux]] — path-based (AppArmor) vs label-based (SELinux); the label travels with the object, the path is just one way to reach it.

## Further reading

- [Wikipedia: AppArmor](https://en.wikipedia.org/wiki/AppArmor)
- [Ubuntu security docs: AppArmor](https://documentation.ubuntu.com/security/security-features/privilege-restriction/apparmor/)
