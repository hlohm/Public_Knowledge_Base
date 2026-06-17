---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
aliases: ["Linux Security Modules"]
tags: ["endpoint"]
status: "developed"
---

# LSM

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]
> **Also known as:** Linux Security Modules

**L**inux **S**ecurity **M**odules. The kernel's framework for pluggable access control: hooks placed at security-relevant points in kernel code paths, where a loaded security module gets the final say on each operation. In mainline since kernel 2.6 (2003).

**Context.** The ordering *is* the architecture: the classic [[Discretionary Access Control]] check runs first, and only if it passes does the LSM hook fire — so a security module can only ever restrict further, never grant what DAC denied. Large "exclusive" modules implement full [[Mandatory Access Control]]: [[SELinux]], [[AppArmor]], [[Smack]], [[TOMOYO]]. Smaller stackable ones add targeted controls — Yama, lockdown, and [[Landlock]], which lets *unprivileged* processes sandbox themselves. Even the [[Capabilities]] logic is wired in as a module. `cat /sys/kernel/security/lsm` shows what's active on a box.

## See also

- [[SELinux]]
- [[AppArmor]]
- [[Capabilities]]
- [[Kernel]]
- [[System Call]]

## Often confused with

- [[seccomp]] — seccomp filters *which syscalls happen at all* and is not an LSM; LSM hooks decide *access to objects* once a syscall is underway.

## Further reading

- [Kernel docs: Linux Security Module usage](https://docs.kernel.org/admin-guide/LSM/index.html)
- [Wikipedia: Linux Security Modules](https://en.wikipedia.org/wiki/Linux_Security_Modules)
