---
type: "term"
branch: "Networking"
aliases: ["Nameserver Record", "Delegation"]
tags: [net, fundamental]
status: "developed"
---

# NS Record

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Nameserver Record, Delegation

The record naming the authoritative nameservers for a zone. Placed in the *parent* zone, it delegates a subtree to a child's servers.

**Context.** Delegation is how the hierarchy is stitched together: the `.de` registry holds NS records pointing `example.de` at your DNS host's nameservers, so a resolver walking down knows where to ask next. Changing where your zone is hosted is an NS change at the registrar — which is exactly why owning the domain (and thus controlling the NS) makes the DNS *host* a swappable commodity. If the nameserver's name is itself inside the delegated zone, you also need a [[Glue Record]] to break the chicken-and-egg.

## See also

- [[DNS Zone]]
- [[Glue Record]]
- [[Authoritative DNS Server]]
- [[DS Record]]

## Further reading

- [RFC 1034 — Domain Concepts and Facilities](https://datatracker.ietf.org/doc/html/rfc1034)
