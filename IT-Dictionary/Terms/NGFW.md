---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Next-Generation Firewall"]
tags: ["network"]
status: "note"
---

# NGFW

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Next-Generation Firewall

**N**ext-**G**eneration **F**ire**w**all. Firewall + IPS + app awareness + often TLS inspection.

**Context.** The consolidation point of network security: app-aware rules ("block file sharing apps" instead of port lists), user-based policy via directory integration, IPS, and URL filtering in one box. The honest caveats: every enabled inspection feature costs throughput, and the TLS-inspection decision dominates how much the IPS actually sees.

## See also

- [[Firewall]]
- [[IDS and IPS]]
- [[TLS Inspection]]
