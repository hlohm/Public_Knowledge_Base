---
type: "term"
branch: "Networking"
aliases: ["Dynamic Host Configuration Protocol"]
tags: ["net", "fundamental"]
status: "developed"
---

# DHCP

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Dynamic Host Configuration Protocol

**D**ynamic **H**ost **C**onfiguration **P**rotocol. Hands a joining host its IP address, mask, gateway, and DNS servers automatically, as a time-limited **lease**. The handshake: **D**iscover → **O**ffer → **R**equest → **A**ck ('DORA').

**Context.** When a machine sits on a 169.254.x.x APIPA address, DHCP failed — the most common 'no network' diagnosis there is. Reservations (fixed IP by MAC) are how printers and servers get stable addresses without manual config. Security-wise, DHCP is unauthenticated broadcast: a **rogue DHCP server** can hand out itself as gateway/DNS and silently MITM a subnet; DHCP snooping on switches is the countermeasure.

## See also

- [[IP]]
- [[Subnet]]
- [[MAC Address]]
- [[DNS]]
- [[MITM]]

## Further reading

- [RFC 2131 — DHCP](https://datatracker.ietf.org/doc/html/rfc2131)
- [Wikipedia: Dynamic Host Configuration Protocol](https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol)
