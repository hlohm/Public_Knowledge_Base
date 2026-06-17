---
type: "term"
branch: "Security"
domain: "Core Principles & Models"
aliases: ["SoD"]
de: "Funktionstrennung / Vier-Augen-Prinzip"
tags: ["principle"]
status: "note"
---

# Separation of Duties

> **Domain:** [[01 - Core Principles|Core Principles & Models]]
> **Also known as:** SoD
> **German:** Funktionstrennung / Vier-Augen-Prinzip

Split sensitive actions across multiple people (e.g. developer ≠ deployer, requester ≠ approver). Prevents fraud and limits insider damage.

**Context.** Shows up everywhere once you look: four-eyes approval on payments, PR review before merge, the firewall-change requester not being the implementer. In small teams where one person inevitably wears both hats, compensate with logging, peer review after the fact, and alerting on sensitive actions.

## See also

- [[Least Privilege]]
- [[PAM]]
