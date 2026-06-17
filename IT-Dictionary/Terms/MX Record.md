---
type: "term"
branch: "Networking"
aliases: ["Mail Exchange", "Mail Exchanger"]
tags: [net, email]
status: "developed"
---

# MX Record

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Mail Exchange, Mail Exchanger

The DNS record naming the mail servers that accept email for a domain, each with a **preference** number (lower = tried first).

**Context.** Mail delivery starts with an MX lookup on the recipient's domain; the sending server tries hosts in preference order, falling back on failure. Because the whole routing decision is a DNS record, *moving your mail* — or putting a forwarder in front of your real mailbox — is just an MX change, which is the lever the whole 'own the domain, swap the provider' email-resilience plan pulls. If a domain has no MX, senders fall back to its [[A Record|A]] record (implicit MX), but relying on that is fragile.

## See also

- [[SMTP]]
- [[SPF]]
- [[PTR Record]]
- [[DANE]]

## Further reading

- [RFC 5321 — Simple Mail Transfer Protocol](https://datatracker.ietf.org/doc/html/rfc5321)
