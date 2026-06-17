---
type: "term"
branch: "Security"
domain: "Network Security"
de: "Firewall"
tags: ["network"]
status: "developed"
---

# Firewall

> **Domain:** [[05 - Network Security|Network Security]]
> **German:** Firewall

Filters traffic based on rules. Generations: packet-filter (L3/L4) → stateful → NGFW (application-aware) → WAF (web-specific).

**Context.** Rulebases rot: a decade of "temporary" any-any rules, objects nobody dares delete, and shadowed rules that never match. Periodic review with hit counters, a default-deny stance both directions, and logging denies at the edges keep a firewall a control rather than furniture. Egress filtering is the chronically neglected half — C2 and exfiltration ride unrestricted outbound.

## See also

- [[NGFW]]
- [[WAF]]
- [[IDS and IPS]]

## Further reading

- [Wikipedia: Firewall (computing)](https://en.wikipedia.org/wiki/Firewall_(computing))
