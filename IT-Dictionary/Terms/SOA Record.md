---
type: "term"
branch: "Networking"
aliases: ["Start of Authority"]
tags: [net]
status: "developed"
---

# SOA Record

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Start of Authority

The record at a zone apex carrying the zone's administrative parameters: primary nameserver, admin contact, serial number, and the refresh/retry/expire/negative-TTL timers.

**Context.** The **serial** is the version number secondaries compare to know when to transfer a fresh copy — bump it on every change (the `YYYYMMDDnn` convention is common). The final field sets the **negative-caching TTL**: how long resolvers may cache an [[NXDOMAIN]] for this zone, which is why a just-fixed missing record can keep failing briefly. Exactly one SOA exists per zone, at the apex.

## See also

- [[DNS Zone]]
- [[NS Record]]
- [[NXDOMAIN]]
- [[TTL]]

## Further reading

- [RFC 1035 — Domain Implementation and Specification](https://datatracker.ietf.org/doc/html/rfc1035)
