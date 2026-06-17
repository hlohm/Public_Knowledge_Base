---
type: "term"
branch: "Networking"
aliases: ["Subnetwork", "Subnet Mask"]
de: "Subnetz"
tags: ["net", "fundamental"]
status: "developed"
---

# Subnet

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Subnetwork, Subnet Mask
> **German:** Subnetz

A contiguous block of IP addresses sharing a prefix, defined by a **subnet mask** / prefix length (`255.255.255.0` = `/24`). Hosts in the same subnet talk directly; anything else goes via the gateway.

**Context.** The subnet decision — 'is the destination local?' — is made independently by every host by ANDing addresses with its mask, which is why a wrong mask produces the signature asymmetric failure (A reaches B, B can't answer). Subnets are also the natural unit of network *design*: one per VLAN, per site, per security zone, with the firewall sitting between them.

## See also

- [[CIDR]]
- [[IP]]
- [[VLAN]]
- [[Network Segmentation]]
- [[Router]]

## Often confused with

- [[VLAN]] — A VLAN is L2 (one broadcast domain on shared switches); a subnet is L3 (an IP range). In practice mapped 1:1, but they're different layers and can diverge.

## Further reading

- [Wikipedia: Subnet](https://en.wikipedia.org/wiki/Subnet)
