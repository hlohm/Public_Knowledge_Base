---
type: "term"
branch: "Internet & Web"
aliases: ["Simple Mail Transfer Protocol"]
tags: ["web", "net", "email", "fundamental"]
status: "developed"
---

# SMTP

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** Simple Mail Transfer Protocol

**S**imple **M**ail **T**ransfer **P**rotocol. The protocol that moves email between servers — a plain-text dialogue of `HELO/EHLO`, `MAIL FROM`, `RCPT TO`, `DATA`. Submission and relay are the two distinct jobs it does.

**Context.** The port tells you the role: **25** is server-to-server relay (and unauthenticated device relay like scan-to-email), **587** is authenticated client submission with STARTTLS, **465** is implicit TLS submission. SMTP predates security entirely — sender identity is just an unverified string, which is the original sin that [[SPF]], [[DKIM]], and [[DMARC]] exist to patch. The envelope (`MAIL FROM`) vs header (From:) split is the detail that makes all of email authentication make sense.

## See also

- [[SPF]]
- [[DKIM]]
- [[DMARC]]
- [[DNS]]
- [[TLS]]

## Further reading

- [RFC 5321 — SMTP](https://datatracker.ietf.org/doc/html/rfc5321)
- [Wikipedia: Simple Mail Transfer Protocol](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol)
