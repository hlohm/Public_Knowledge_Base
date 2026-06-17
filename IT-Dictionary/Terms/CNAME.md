---
type: "term"
branch: "Networking"
aliases: ["Canonical Name", "CNAME Record", "DNS Alias"]
tags: [net]
status: "developed"
---

# CNAME

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Canonical Name, CNAME Record, DNS Alias

A record that aliases one name to another *name* (its canonical name); the resolver then continues resolving the target.

**Context.** Use it to point `www` at `app.example.com` so one address change updates everywhere. Two hard rules trip people up: a CNAME can't coexist with any other record for the same name, so it's **illegal at a zone apex** (which must carry SOA/NS) — hence registrar 'ALIAS/ANAME' flattening hacks for `example.com` → some CDN. And chains of CNAMEs cost extra lookups. When you just want several labels for one host, parallel [[A Record|A records]] are usually simpler.

## See also

- [[A Record]]
- [[DNS Zone]]
- [[DNS]]

## Often confused with

- [[A Record]] — CNAME points name → name; A points name → address. Apex names can't be CNAMEs.

## Further reading

- [RFC 1034 — Domain Concepts and Facilities](https://datatracker.ietf.org/doc/html/rfc1034)
