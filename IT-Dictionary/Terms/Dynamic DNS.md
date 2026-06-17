---
type: "term"
branch: "Networking"
aliases: ["DynDNS", "DDNS"]
tags: [net]
status: "developed"
---

# Dynamic DNS

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** DynDNS, DDNS

Keeping a DNS record automatically updated as a host's IP changes — typically a client that pushes its current address to the DNS provider on a schedule or on change.

**Context.** The classic use is a home/residential connection with a rotating IP: a small client (ddclient, a router feature, a provider's updater) refreshes an A record so a stable name keeps pointing at you. There are two flavours: provider-specific HTTP update endpoints (DuckDNS, deSEC's dedyn.io) and the standards-based DNS UPDATE protocol (RFC 2136). Reserving a static IP where you can is simpler than running DDNS at all.

## See also

- [[A Record]]
- [[TTL]]
- [[DNS]]

## Further reading

- [RFC 2136 — Dynamic Updates in the DNS](https://datatracker.ietf.org/doc/html/rfc2136)
