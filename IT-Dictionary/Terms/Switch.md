---
type: "term"
branch: "Networking"
aliases: ["Network Switch"]
tags: ["net", "fundamental"]
status: "developed"
---

# Switch

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Network Switch

A layer-2 device that learns which MAC address lives on which port (from source addresses of passing frames) and then forwards frames only to the right port, instead of repeating them everywhere like a hub.

**Context.** The MAC table is the whole trick — and also the attack surface: flood it (MAC flooding) and the switch fails open into hub behavior; lie in it (via [[ARP]] games) and traffic comes to you. Managed switches add the operational layer: VLANs, trunk ports, port security, spanning tree, and PoE for the phones and APs. L3 switches blur the line by routing between VLANs in hardware.

## See also

- [[MAC Address]]
- [[VLAN]]
- [[Ethernet]]
- [[Router]]
- [[ARP]]

## Further reading

- [Wikipedia: Network switch](https://en.wikipedia.org/wiki/Network_switch)
