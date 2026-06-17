---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
aliases: ["Security-Enhanced Linux", "SEAndroid"]
tags: ["endpoint"]
status: "developed"
---

# SELinux

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]
> **Also known as:** Security-Enhanced Linux, SEAndroid

**S**ecurity-**E**nhanced **Linux**. The Linux kernel's label-based [[Mandatory Access Control]] system: every process and object carries a security context, and a centrally compiled, default-deny policy decides every access — including for root-owned processes. Started as an NSA research project; in the mainline kernel since 2003 as an [[LSM]] module.

**Context.** A context reads `user:role:type:level` (e.g. `system_u:system_r:httpd_t:s0`); the workhorse layer is [[Type Enforcement]] over the `type` field, with role-based control and optional [[MLS]]/[[MCS]] above it. File labels live in the `security.selinux` extended attribute and travel with the inode — renames and path games don't shake them off. Decisions are cached in the [[AVC]]; denials land in the audit log, where `audit2allow` and `sesearch` help you read them. *Enforcing* blocks; *permissive* only logs — the standard mode for developing policy. Most distributions ship the *targeted* policy: exposed daemons confined, ordinary user sessions unconfined, so MAC bites exactly where exposure is highest. Where you meet it: RHEL/Fedora by default, Android (fully enforcing since 5.0), and container isolation via MCS categories. The gotcha to unlearn: `setenforce 0` is the internet's most-pasted "fix" — it disables the control instead of fixing the label; `restorecon` usually is the fix.

## See also

- [[Type Enforcement]]
- [[LSM]]
- [[Mandatory Access Control]]
- [[AppArmor]]
- [[MLS]]
- [[Hardening]]
- [[Kernel]]

## Often confused with

- [[AppArmor]] — both are MAC LSMs; SELinux decides by *labels* attached to objects, AppArmor by filesystem *paths*. Analyzable completeness vs administrator ergonomics.

## Further reading

- [Wikipedia: Security-Enhanced Linux](https://en.wikipedia.org/wiki/SELinux)
- [Kernel docs: Linux Security Module usage](https://docs.kernel.org/admin-guide/LSM/index.html)
