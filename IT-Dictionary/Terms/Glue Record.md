---
type: "term"
branch: "Networking"
aliases: ["Glue", "Glue A Record"]
tags: [net]
status: "note"
---

# Glue Record

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Glue, Glue A Record

An [[A Record|A/AAAA]] record for a nameserver, served by the *parent* zone, to resolve a circular dependency where the nameserver's name lives inside the zone it serves.

**Context.** If `example.com` is served by `ns1.example.com`, a resolver can't ask `ns1.example.com` for its address without already knowing `example.com`'s servers — deadlock. The parent (`.com`) breaks it by publishing the glue: the IP of `ns1.example.com` directly alongside the [[NS Record|NS]] delegation. You only need glue when nameservers are *in-bailiwick* (inside the zone they serve); using a third-party DNS host whose servers are under its own domain sidesteps glue entirely.

## See also

- [[NS Record]]
- [[DNS Zone]]
- [[Authoritative DNS Server]]
