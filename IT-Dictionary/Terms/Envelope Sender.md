---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Return-Path", "MAIL FROM", "Envelope From", "Bounce Address"]
tags: ["network", "email"]
status: "developed"
---

# Envelope Sender

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Return-Path, MAIL FROM, Envelope From, Bounce Address

The address given in the SMTP `MAIL FROM` command — the transport-level sender, where bounces go — as opposed to the `From:` header the recipient actually sees.

**Context.** Email has two 'from's, and conflating them is the root of most authentication confusion. [[SPF]] and the [[SRS]] rewrite both act on the *envelope* sender; [[DKIM]] signs headers including the visible `From:`; and [[DMARC]] exists precisely to require *alignment* between the authenticated identity and that visible `From:`. The envelope address is recorded as the `Return-Path:` header by the receiving server. Display-name spoofing works because nothing forces the envelope and header to match unless DMARC demands it.

## See also

- [[SPF]]
- [[DKIM]]
- [[DMARC]]
- [[SRS]]
- [[SMTP]]

## Further reading

- [RFC 5321 — Simple Mail Transfer Protocol](https://datatracker.ietf.org/doc/html/rfc5321)
