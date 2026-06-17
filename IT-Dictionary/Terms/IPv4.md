---
type: "term"
branch: "Networking"
tags: ["net", "fundamental"]
status: "developed"
---

# IPv4

> **Branch:** [[04 - Networking|Networking]]

The 32-bit version of IP that built the internet: ~4.3 billion addresses in dotted-quad notation (`203.0.113.7`), long since exhausted and kept usable by NAT and private ranges (RFC 1918: `10/8`, `172.16/12`, `192.168/16`).

**Context.** Address exhaustion shaped modern networking more than any standard: NAT everywhere, carrier-grade NAT, and the slow IPv6 transition are all downstream of 32 bits not being enough. The RFC 1918 ranges plus loopback (`127.0.0.0/8`) and APIPA (`169.254/16`) are the special blocks worth knowing cold — recognizing them instantly is half of network troubleshooting.

## See also

- [[IP]]
- [[IPv6]]
- [[NAT]]
- [[CIDR]]
- [[Subnet]]

## Further reading

- [RFC 791 — Internet Protocol](https://datatracker.ietf.org/doc/html/rfc791)
- [Wikipedia: IPv4](https://en.wikipedia.org/wiki/IPv4)
