---
type: "term"
branch: "Networking"
aliases: ["Split-brain DNS", "Split DNS"]
tags: [net]
status: "developed"
---

# Split-horizon DNS

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Split-brain DNS, Split DNS

Serving different answers for the same name depending on who's asking — typically an internal view (private IPs, internal-only hostnames) and a public view, from two separate authorities.

**Context.** The internal view is served by a local resolver to trusted clients and is never present in public DNS; the public view lives on the authoritative zone and exposes only what you mean to. The classic break isn't on the server — it's a *client-side shadow* answering a bare name before your intended resolver is consulted: a leftover `/etc/hosts` entry (synthetic), or a VPN's MagicDNS holding a record for the same short name and winning the search-domain race. The fix is to give every alternate path its own label and reserve the bare name for the canonical resolver. Querying the explicit [[FQDN]] bypasses both shadows and tells you whether the fault is the resolver path or the record.

## See also

- [[DNS Zone]]
- [[Search Domain]]
- [[Stub Resolver]]
- [[FQDN]]
- [[DNS Forwarding]]

## Further reading

- [Wikipedia: Split-horizon DNS](https://en.wikipedia.org/wiki/Split-horizon_DNS)
