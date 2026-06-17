---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["Bring Your Own Vulnerable Driver"]
tags: [threat, modern]
status: "developed"
---

# BYOVD

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** Bring Your Own Vulnerable Driver

An attacker ships a *legitimately signed* but vulnerable kernel [[Driver]], loads it, and exploits its flaw to gain kernel-level execution — without ever needing their own code to be signed. It is the standard route from administrator to [[Kernel]] (Ring 0) on modern Windows.

**Context.** BYOVD defeats driver-signing ([[Code Signing]]) by abusing trust that was legitimately granted: the driver's signature is real, only the *behaviour* is the problem. Once in the kernel an attacker can disable [[EDR]], install a [[Rootkit]], or run [[DKOM]]. Mitigations are blocklists of known-bad drivers (Microsoft's Vulnerable Driver Blocklist) and [[HVCI]]; the canonical catalogue of abusable drivers is the LOLDrivers project.

## See also

- [[Driver]]
- [[Kernel]]
- [[Rootkit]]
- [[DKOM]]
- [[HVCI]]
- [[Privilege Escalation]]

## Further reading

- [LOLDrivers — Living Off The Land Drivers](https://www.loldrivers.io/)
