---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["Direct Kernel Object Manipulation"]
tags: [threat]
status: "developed"
---

# DKOM

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** Direct Kernel Object Manipulation

A [[Rootkit]] technique that hides activity by editing in-memory kernel data structures directly — for example, unlinking a process's `EPROCESS` entry from the doubly-linked list the OS walks to enumerate processes. The process keeps running; it just stops appearing in any list.

**Context.** DKOM works because the kernel trusts its own bookkeeping. It needs kernel-level execution to begin with (so it presupposes [[Privilege Escalation]], often via [[BYOVD]]), and it's exactly what modern defences target: [[HVCI]] stops unsigned kernel code loading, and kernel patch protection (PatchGuard) watches critical structures for tampering.

## See also

- [[Rootkit]]
- [[Kernel]]
- [[BYOVD]]
- [[HVCI]]
- [[Privilege Escalation]]

## Further reading

- [MITRE ATT&CK: Rootkit (T1014)](https://attack.mitre.org/techniques/T1014/)
