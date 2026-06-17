---
type: "term"
branch: "Security"
domain: "Network Security"
tags: ["network"]
status: "note"
---

# East-West vs North-South Traffic

> **Domain:** [[05 - Network Security|Network Security]]

**North-south** = client ↔ data center (external); **east-west** = server ↔ server (internal). Internal traffic is the historically under-monitored one.

**Context.** The perimeter firewall sees only north-south; the lateral movement that turns one compromised workstation into a domain-wide incident is pure east-west. Closing that blind spot is the sales pitch of microsegmentation, internal NetFlow monitoring, and EDR network telemetry — pick at least one.

## See also

- [[Microsegmentation]]
- [[Service Mesh]]
