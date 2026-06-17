---
type: "term"
branch: "Networking"
aliases: ["Address Resolution Protocol"]
tags: ["net", "fundamental"]
status: "developed"
---

# ARP

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Address Resolution Protocol

**A**ddress **R**esolution **P**rotocol. How a host on a LAN learns which MAC address owns an IP: broadcast 'who has 192.168.1.1?', cache the answer.

**Context.** ARP has zero authentication — any host can answer for any IP, which is **ARP spoofing/poisoning**, the classic way to become a LAN [[MITM]]. Defenses: dynamic ARP inspection on switches, or just accepting that L2 adjacency means trust. `arp -a` (the neighbor cache) is a first-rate troubleshooting tool: a wrong or missing entry explains many 'it pings sometimes' mysteries. IPv6 replaces ARP with NDP — same job, same spoofing problem.

## See also

- [[MAC Address]]
- [[Switch]]
- [[MITM]]
- [[IPv4]]
- [[VLAN]]

## Further reading

- [RFC 826 — ARP](https://datatracker.ietf.org/doc/html/rfc826)
- [Wikipedia: Address Resolution Protocol](https://en.wikipedia.org/wiki/Address_Resolution_Protocol)
