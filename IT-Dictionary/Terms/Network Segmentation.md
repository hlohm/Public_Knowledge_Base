---
type: "term"
branch: "Security"
domain: "Network Security"
de: "Netzwerksegmentierung"
tags: ["network"]
status: "note"
---

# Network Segmentation

> **Domain:** [[05 - Network Security|Network Security]]
> **German:** Netzwerksegmentierung

Splitting networks into zones so a breach in one doesn't spread.

**Context.** The control that turns "one phished laptop" into a contained incident instead of encrypted-everything: clients, servers, management interfaces, OT, and guests in separate zones with deny-by-default between them. Start coarse — even three zones beat one flat /16 — and remember segmentation without enforced inter-zone rules is just addressing.

## See also

- [[Microsegmentation]]
- [[VLAN]]
- [[Blast Radius]]
- [[Lateral Movement]]
