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

**Context.** Email has two 'from's, and conflating them is the root of most authentication confusion. [[SPF]] and the [[SRS]] rewrite both act on the *envelope* sender; [[DKIM]] signs headers including the visible `From:`; and [[DMARC]] exists precisely to require *alignment* between the authenticated identity and that visible `From:`. Display-name spoofing works because nothing forces the envelope and header to match unless DMARC demands it.

**Return-Path.** The envelope sender exists only inside the SMTP conversation and vanishes when that conversation ends — so at final delivery the receiving server writes it into a `Return-Path:` header, and that header is the only way to recover it from a stored message afterwards. Two consequences worth holding on to: a `Return-Path:` disagreeing with `From:` is completely normal (every mailing list, forwarder and [[ESP]] produces one), and since the header is added by the *delivering* server, it is trustworthy for exactly the same reason [[Received Header|Received:]] lines are — because a system you control wrote it, not because the message said so.

## See also

- [[SPF]]
- [[DKIM]]
- [[DMARC]]
- [[SRS]]
- [[SMTP]]
- [[Received Header]]
- [[Bounce]]
- [[Email Ecosystem]]

## Further reading

- [RFC 5321 — Simple Mail Transfer Protocol](https://datatracker.ietf.org/doc/html/rfc5321)
