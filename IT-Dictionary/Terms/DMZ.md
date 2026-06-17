---
type: "term"
branch: "Security"
domain: "Network Security"
tags: ["network"]
status: "note"
---

# DMZ

> **Domain:** [[05 - Network Security|Network Security]]

**D**e**M**ilitarized **Z**one. Network segment between internal and external networks, hosting public services. Somewhat dated terminology.

**Context.** The pattern outlives the name: anything reachable from the internet lives in a zone that is firewalled *from* the internal network, so a popped web server can't immediately reach AD. The classic sin is the convenient rule "DMZ may talk to internal database/domain controller" — every such rule is a bridge the attacker thanks you for.

## See also

- [[Network Segmentation]]
- [[Bastion Host]]
