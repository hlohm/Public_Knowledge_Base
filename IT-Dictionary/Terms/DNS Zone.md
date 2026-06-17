---
type: "term"
branch: "Networking"
aliases: ["Zone", "Zone Apex", "Zone Cut"]
tags: [net, fundamental]
status: "developed"
---

# DNS Zone

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Zone, Zone Apex, Zone Cut

A contiguous portion of the DNS namespace administered as a unit — one [[SOA Record]], a set of records, and a single authority. The *apex* is the zone's top name; a *cut* is where a child zone is delegated away.

**Context.** A zone is the administrative atom: `example.com` is a zone, and delegating `lab.example.com` to a different nameserver creates a zone cut, after which the parent only holds an [[NS Record|NS]] pointing down (and maybe a [[Glue Record]]). The apex is special — it can't be a [[CNAME]], and it carries the SOA and NS records. Split-horizon works by having two different authorities serve the *same* zone name to different audiences.

## See also

- [[SOA Record]]
- [[NS Record]]
- [[Glue Record]]
- [[Authoritative DNS Server]]
- [[Split-horizon DNS]]

## Further reading

- [RFC 1034 — Domain Concepts and Facilities](https://datatracker.ietf.org/doc/html/rfc1034)
