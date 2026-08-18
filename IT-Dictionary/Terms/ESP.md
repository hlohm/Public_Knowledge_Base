---
type: "term"
branch: "Internet & Web"
aliases: ["Email Service Provider"]
tags: ["web", "net", "email"]
status: "developed"
---

# ESP

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** Email Service Provider

**E**mail **S**ervice **P**rovider — a service that sends mail on your behalf at volume: marketing campaigns, receipts, password resets and other transactional messages.

**Context.** You delegate authentication to them — an [[SPF]] `include`, [[DKIM]] keys published as CNAMEs into their zone, often a custom return-path subdomain — and in exchange inherit the reputation of their sending pools. Shared pools are cheap and expose you to other customers' behaviour; dedicated addresses are yours to warm up and yours to ruin. The discipline worth learning is separation: a distinct subdomain per traffic stream, so that a marketing campaign that draws complaints cannot damage the reputation carrying your password-reset mail. Since 2024 the large mailbox providers enforce bulk-sender rules — authentication, one-click unsubscribe, complaint rates below roughly 0.3 % — which turned all of this from best practice into a gate.

## See also

- [[SPF]]
- [[DKIM]]
- [[DMARC]]
- [[Deliverability]]
- [[Feedback Loop]]
- [[IP Reputation]]
- [[Email Ecosystem]]

## Further reading

- [RFC 8058 — One-Click Unsubscribe](https://datatracker.ietf.org/doc/html/rfc8058)
