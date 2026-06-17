---
type: "term"
branch: "Networking"
aliases: ["Classless Inter-Domain Routing", "CIDR Notation"]
tags: ["net", "fundamental"]
status: "developed"
---

# CIDR

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Classless Inter-Domain Routing, CIDR Notation

**C**lassless **I**nter-**D**omain **R**outing. Address blocks of any power-of-two size written as prefix length: `10.0.0.0/8`, `192.168.1.0/24`. Replaced the rigid class A/B/C scheme in 1993.

**Context.** The /N is the number of fixed prefix bits; the rest are host bits, so a /24 holds 2⁸−2 usable addresses and each extra prefix bit halves the block. CIDR math (does this IP fall in that range? do these routes aggregate?) is daily bread for firewall rules, route tables, and cloud VPC design — and 'longest prefix match' is how every router picks among overlapping routes.

## See also

- [[Subnet]]
- [[IP]]
- [[IPv4]]
- [[IPv6]]
- [[NAT]]

## Further reading

- [RFC 4632 — CIDR](https://datatracker.ietf.org/doc/html/rfc4632)
- [Wikipedia: Classless Inter-Domain Routing](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing)
