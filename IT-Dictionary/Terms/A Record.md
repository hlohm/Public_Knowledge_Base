---
type: "term"
branch: "Networking"
aliases: ["AAAA Record", "Address Record"]
tags: [net, fundamental]
status: "developed"
---

# A Record

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** AAAA Record, Address Record

The DNS record mapping a name to an IP address — **A** for IPv4, **AAAA** for IPv6.

**Context.** The most basic forward record and the one most host entries are. Note that giving a host several names by pointing multiple A records at the same IP is *not* a [[CNAME]] — each is an independent address record (which, unlike a CNAME, is legal at a zone apex and alongside other record types). Multiple A records for one name is also the crudest form of load distribution (round-robin DNS).

## See also

- [[AAAA Record]]
- [[CNAME]]
- [[PTR Record]]
- [[DNS Zone]]

## Often confused with

- [[CNAME]] — An A record holds an address; a CNAME aliases one name to another name (which is then resolved further).

## Further reading

- [RFC 1035 — Domain Implementation and Specification](https://datatracker.ietf.org/doc/html/rfc1035)
