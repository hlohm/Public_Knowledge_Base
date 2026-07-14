---
type: "term"
branch: "Security"
domain: "Core Principles & Models"
tags: ["principle", "anti-pattern"]
status: "developed"
---

# Security through Obscurity

> **Domain:** [[01 - Core Principles|Core Principles & Models]]

Relying on secrets *about the design* rather than secrets *within the design* (keys). Generally derided as a sole strategy; acceptable as one defensive layer.

**Context.** Kerckhoffs's principle is the formal version: a system should stay secure even if everything but the key is public. Moving SSH off port 22 cuts log noise but stops no targeted attacker. Treat obscurity as seasoning, never the meal — if a measure collapses the moment its existence is known, it isn't a control.

## See also

- [[Defense in Depth]]
- [[Hardening]]
- [[Attack Surface]]
- [[Least Privilege]]

## Further reading

- [Wikipedia: Kerckhoffs's principle](https://en.wikipedia.org/wiki/Kerckhoffs%27s_principle)
