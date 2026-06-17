---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["Remote Code Execution"]
tags: ["threat", "vuln"]
status: "note"
---

# RCE

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** Remote Code Execution

**R**emote **C**ode **E**xecution. The crown jewel of vulnerabilities: attacker runs arbitrary code on your system.

**Context.** Tops severity scales because it usually chains straight into everything else — foothold, then lateral movement, then objectives. The high-profile ones get names (Log4Shell, ProxyLogon) and immediate mass scanning. Operationally: anything internet-facing with an RCE is a drop-everything patch, and it's the bug class most likely to land in CISA KEV within days.

## See also

- [[Exploit]]
- [[Buffer Overflow]]
- [[Injection Attacks]]
- [[KEV]]
