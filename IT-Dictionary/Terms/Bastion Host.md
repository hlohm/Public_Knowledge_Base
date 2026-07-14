---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Jump Box"]
tags: ["network"]
status: "note"
---

# Bastion Host

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Jump Box

Hardened entry point used to reach internal systems. Also called a **jump box**.

**Context.** The design rules: it does exactly one job (SSH/RDP brokering), runs nothing else, requires MFA, and logs or records every session — it's the chokepoint where access becomes auditable. Cloud equivalents (Azure Bastion, AWS SSM Session Manager) remove even the public IP. A bastion that's also someone's utility server is a liability, not a control.

## See also

- [[SSH]]
- [[VPN]]
- [[ZTNA]]
- [[PAM]]
