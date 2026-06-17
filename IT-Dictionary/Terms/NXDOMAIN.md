---
type: "term"
branch: "Networking"
aliases: ["Non-Existent Domain", "RCODE 3"]
tags: [net]
status: "developed"
---

# NXDOMAIN

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Non-Existent Domain, RCODE 3

The DNS response code meaning *this name does not exist* (no records of any type, and no such name). Distinct from NODATA — the name exists but has no record of the type you asked for.

**Context.** NXDOMAIN vs NODATA is a real distinction: `host.example` returning NXDOMAIN means the label is unknown; returning an empty answer for an AAAA query while the A exists is NODATA (RCODE 0, zero answers). Where the NXDOMAIN comes from matters too — a `static` local-zone produces it *locally* and instantly for undefined names, whereas a `transparent` zone falls through and the NXDOMAIN comes back from upstream after a full round-trip. RFC 8020 ('NXDOMAIN means there's nothing below') lets resolvers cache the negative for the whole subtree.

## See also

- [[DNS Zone]]
- [[TTL]]
- [[Recursive Resolver]]

## Further reading

- [RFC 8020 — NXDOMAIN: There Really Is Nothing Underneath](https://datatracker.ietf.org/doc/html/rfc8020)
