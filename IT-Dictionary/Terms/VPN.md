---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Virtual Private Network"]
tags: ["network"]
status: "developed"
---

# VPN

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Virtual Private Network

**V**irtual **P**rivate **N**etwork. Encrypted tunnel. Site-to-site, remote-access, or service VPNs. Increasingly displaced by ZTNA.

**Context.** Two operational realities: the network-level access a client VPN grants is exactly the lateral-movement surface ZTNA exists to remove, and VPN gateways themselves have become top exploitation targets (a steady stream of appliance CVEs in the KEV list) — patch them like crown jewels. WireGuard's small codebase made it the modern default for self-hosted tunnels.

## See also

- [[ZTNA]]
- [[WireGuard]]
- [[TLS]]

## Further reading

- [Wikipedia: Virtual private network](https://en.wikipedia.org/wiki/Virtual_private_network)
