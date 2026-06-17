---
type: "term"
branch: "Networking"
tags: ["net", "fundamental"]
status: "developed"
---

# IPv6

> **Branch:** [[04 - Networking|Networking]]

The 128-bit successor to IPv4: colon-hex notation (`2001:db8::1`), address space vast enough that every device gets a globally unique address, killing the *need* for NAT. Hosts can self-configure via **SLAAC**; ARP is replaced by NDP.

**Context.** The mental shift: scarcity thinking dies (a standard LAN gets a /64 — more addresses than the whole IPv4 internet), and 'private = NAT = safe' dies with it; in v6 the firewall alone does the job NAT accidentally did. Operationally, dual stack is the norm and the classic blind spot: v6 is often *on by default* and unfiltered while all the security rules watch v4 — attackers noticed long ago.

## See also

- [[IPv4]]
- [[IP]]
- [[NAT]]
- [[Firewall]]
- [[Subnet]]

## Further reading

- [RFC 8200 — IPv6 Specification](https://datatracker.ietf.org/doc/html/rfc8200)
- [Wikipedia: IPv6](https://en.wikipedia.org/wiki/IPv6)
