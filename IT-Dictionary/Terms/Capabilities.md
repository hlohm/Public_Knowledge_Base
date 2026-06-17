---
type: "term"
branch: "Operating Systems"
aliases: ["Linux Capabilities", "POSIX Capabilities"]
tags: ["os"]
status: "developed"
---

# Capabilities

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **Also known as:** Linux Capabilities, POSIX Capabilities

The decomposition of root's all-or-nothing power into discrete privileges — about forty units like `CAP_NET_BIND_SERVICE` (bind ports below 1024) or `CAP_SYS_TIME` (set the clock) — held and dropped per thread.

**Context.** The point is shedding: a service that needs one privileged act can hold one capability instead of full root, and *file capabilities* retire many [[setuid]]-root binaries (`ping` needs `CAP_NET_RAW`, not uid 0). [[Container]] runtimes drop most of the set by default. The catch every auditor learns: `CAP_SYS_ADMIN` became the junk drawer — so broad it's effectively "the new root," and granting it usually concedes the game. The name "POSIX capabilities" lingers from the never-ratified POSIX.1e draft. Orthogonal to [[Mandatory Access Control]]: capabilities gate privileged *operations*, MAC gates access to *objects* — a hardened service uses both, plus [[seccomp]] to shrink the syscall surface.

## See also

- [[Least Privilege]]
- [[setuid]]
- [[Container]]
- [[seccomp]]
- [[Privilege Escalation]]
- [[Kernel]]

## Often confused with

- [[Capability-Based Security]] — same word, unrelated model: Linux capabilities slice up root's privileges; object capabilities are unforgeable tokens granting access to specific objects.

## Further reading

- [man7: capabilities(7)](https://man7.org/linux/man-pages/man7/capabilities.7.html)
