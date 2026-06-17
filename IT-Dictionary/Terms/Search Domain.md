---
type: "term"
branch: "Networking"
aliases: ["DNS Search List", "Search List", "Domain Suffix"]
tags: [net]
status: "developed"
---

# Search Domain

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** DNS Search List, Search List, Domain Suffix

A suffix (or list of them) the resolver appends to a *single-label* name before querying, so `grafana` becomes `grafana.lan.example`.

**Context.** Only bare single-label names get the suffix appended; a multi-label name is treated as already-qualified and queried as-is. That asymmetry is exactly why bare-name bugs bite while [[FQDN]] queries stay clean. With more than one link contributing a search domain (a VPN plus a tunnel, say), a single label can produce several candidate FQDNs across different resolvers — and a non-intended one can win the race, e.g. a tailnet's `*.ts.net` answer beating your `*.lan.example` answer. Tell from the resolver output which link and suffix actually answered.

## See also

- [[FQDN]]
- [[Stub Resolver]]
- [[Split-horizon DNS]]

## Often confused with

- [[FQDN]] — A search domain is appended only to bare names; an FQDN is already complete and skips the search list entirely.

## Further reading

- [RFC 1535 — A Security Problem with DNS Search Lists](https://datatracker.ietf.org/doc/html/rfc1535)
