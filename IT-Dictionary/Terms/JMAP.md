---
type: "term"
branch: "Internet & Web"
aliases: ["JSON Meta Application Protocol"]
tags: ["web", "net", "email"]
status: "developed"
---

# JMAP

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** JSON Meta Application Protocol

**J**SON **M**eta **A**pplication **P**rotocol — a modern JSON-over-HTTPS alternative to [[IMAP]], designed for batched requests, efficient synchronisation and mobile networks.

**Context.** JMAP rides ordinary HTTPS on 443, so it inherits the web's infrastructure — proxies, load balancers, certificates, connection handling that mobile stacks already optimise. Clients fetch a state token and ask only for what changed, batching several operations into one round trip, which removes IMAP's per-folder chatter. Push arrives over standard web mechanisms rather than a held-open connection. Adoption is real but partial: it is implemented by a handful of providers and clients rather than being the default anywhere, so IMAP remains the protocol you must support. Worth knowing as the direction of travel, and as evidence that email's message model outlived the protocols built to access it.

## See also

- [[IMAP]]
- [[POP3]]
- [[HTTPS]]
- [[MUA]]
- [[Email Ecosystem]]

## Further reading

- [RFC 8620 — The JSON Meta Application Protocol](https://datatracker.ietf.org/doc/html/rfc8620)
- [jmap.io](https://jmap.io/)
