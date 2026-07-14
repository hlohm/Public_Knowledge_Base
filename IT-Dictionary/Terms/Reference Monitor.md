---
type: "term"
branch: "Security"
domain: "Core Principles & Models"
tags: ["principle"]
status: "developed"
---

# Reference Monitor

> **Domain:** [[01 - Core Principles|Core Principles & Models]]

The idealized enforcement point through which *every* access by every subject to every object is mediated. To count as a reference monitor it must be **always invoked** (no bypass path), **tamper-proof**, and **small enough to be verified** by analysis and testing.

**Context.** From the 1972 Anderson report, this is the abstract ideal that the [[Trusted Computing Base]] is built to satisfy — the reference monitor is the *concept*, its concrete implementation is the "security kernel", and the TCB is everything that kernel depends on. The three properties are a design checklist you can hold any enforcement mechanism against: *complete mediation* (can any access route around it? an off-path cache or a `TOCTOU` window fails this), *tamper-proof* (can a subject modify the monitor or its policy? — the reason an agent's sandbox policy must live outside the agent's own write set), and *verifiable* (is it small and simple enough to actually reason about? — the argument for a minimal TCB). Real systems only approximate it: the Linux [[LSM]] framework with [[SELinux]] or [[AppArmor]] is a reference-monitor-shaped hook layer sitting on the kernel's access path; a [[Hypervisor]] plays the role for VM isolation. Nothing in commodity computing is fully verifiable, which is precisely why the ideal is a yardstick rather than a product.

## See also

- [[Trusted Computing Base]]
- [[Access Control Matrix]]
- [[Mandatory Access Control]]
- [[LSM]]
- [[Least Privilege]]

## Further reading

- [Wikipedia: Reference monitor](https://en.wikipedia.org/wiki/Reference_monitor)