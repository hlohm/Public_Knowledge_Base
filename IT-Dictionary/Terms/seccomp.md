---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
aliases: ["Secure Computing Mode", "seccomp-bpf"]
tags: ["endpoint"]
status: "developed"
---

# seccomp

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]
> **Also known as:** Secure Computing Mode, seccomp-bpf

A Linux kernel facility that filters which [[System Call]]s a process may make: a small BPF program inspects each syscall and allows, denies, logs, or kills. Once installed, a filter is irrevocable and inherited by children.

**Context.** seccomp shrinks the *kernel attack surface* reachable from a compromised process — most kernel exploits begin with an unusual syscall, and a tight filter means that door was never reachable in the first place. Everyday deployments: Docker's default profile (blocks dozens of syscalls), browser sandboxes (Chrome, Firefox), and systemd's `SystemCallFilter=`. It completes the layered picture: [[Capabilities]] gate privileged operations, MAC ([[SELinux]], [[AppArmor]]) gates access to objects, seccomp gates the syscall menu itself.

## See also

- [[System Call]]
- [[Sandbox]]
- [[Capabilities]]
- [[Container Security]]

## Often confused with

- [[LSM]] — seccomp is a separate mechanism, not an LSM module: it decides whether a syscall happens at all, while LSM hooks decide access to objects within one.

## Further reading

- [man7: seccomp(2)](https://man7.org/linux/man-pages/man2/seccomp.2.html)
- [Wikipedia: seccomp](https://en.wikipedia.org/wiki/Seccomp)
