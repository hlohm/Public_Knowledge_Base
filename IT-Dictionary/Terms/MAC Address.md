---
type: "term"
branch: "Networking"
aliases: ["Media Access Control Address", "Hardware Address"]
tags: ["net", "fundamental"]
status: "developed"
---

# MAC Address

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Media Access Control Address, Hardware Address

The 48-bit link-layer address burned into (or assigned to) a network interface, written as six hex pairs (`a4:5e:60:…`). The first half is the vendor OUI; frames on a LAN are delivered by MAC, not IP.

**Context.** MACs only matter within one L2 segment — routers strip and replace them at every hop, which is the cleanest way to see the L2/L3 split. Operationally they show up in DHCP reservations, port security, and NAC; forensically they're weak identifiers because they're trivially spoofed, and modern OSes randomize them on Wi-Fi for privacy, which quietly breaks MAC-based allowlists.

## See also

- [[Ethernet]]
- [[ARP]]
- [[Switch]]
- [[DHCP]]
- [[NAC]]

## Further reading

- [Wikipedia: MAC address](https://en.wikipedia.org/wiki/MAC_address)
