---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["Credential Stuffing", "\"Dictionary Attack\""]
tags: ["threat"]
status: "note"
---

# Brute Force

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** Credential Stuffing, "Dictionary Attack"

Trying many passwords or keys. **Credential stuffing** uses leaked credentials from other breaches.

**Context.** Pure brute force is largely dead against well-built systems (lockouts, rate limits, slow hashes); the live variants route around those — credential stuffing reuses breach dumps, password spraying stays under lockout thresholds. The durable defenses are MFA, breached-password screening, and detection of distributed low-and-slow attempts rather than just per-account counters.

## See also

- [[Password Spraying]]
- [[MFA]]
