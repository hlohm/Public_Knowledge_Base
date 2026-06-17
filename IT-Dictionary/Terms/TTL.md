---
type: "term"
branch: "Networking"
aliases: ["Time to Live"]
tags: [net]
status: "developed"
---

# TTL

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Time to Live

In DNS, the number of seconds a record may be cached by resolvers before it must be re-fetched. (The term also names the IP hop-count field — unrelated.)

**Context.** TTL is the dial behind 'DNS propagation': there is no push: changes simply take effect as cached copies expire. Lower it (to e.g. 300 s) *before* a planned IP change so the cutover is quick, then raise it afterwards to cut query load. Negative answers ([[NXDOMAIN]]) are cached too, bounded by the [[SOA Record|SOA]] minimum/negative-TTL — which is why a fixed typo can keep failing for a while.

## See also

- [[NXDOMAIN]]
- [[SOA Record]]
- [[Recursive Resolver]]
- [[Dynamic DNS]]

## Often confused with

- [[Packet]] — DNS TTL is a cache lifetime in seconds; the IP header TTL is a hop counter that stops routing loops.

## Further reading

- [RFC 2181 — Clarifications to the DNS Specification](https://datatracker.ietf.org/doc/html/rfc2181)
