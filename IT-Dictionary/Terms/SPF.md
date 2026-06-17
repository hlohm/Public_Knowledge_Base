---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Sender Policy Framework"]
tags: ["security", "network", "email"]
status: "developed"
---

# SPF

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Sender Policy Framework

**S**ender **P**olicy **F**ramework. A DNS TXT record listing which mail servers may send email for a domain. Receiving servers check the connecting IP against the record.

**Context.** SPF authenticates the *envelope sender* (SMTP `MAIL FROM`), not the From: header the user sees — which is why it can't stop display-name spoofing on its own and needs [[DMARC]] for alignment. Classic operational gotchas: the 10-DNS-lookup limit, forgetting to add a new sending service (the scan-to-email printer, the newsletter tool) and silently landing in spam, and the `~all` (softfail) vs `-all` (hardfail) decision.

## See also

- [[DKIM]]
- [[DMARC]]
- [[SMTP]]
- [[DNS]]
- [[Phishing]]

## Often confused with

- [[DKIM]] — SPF validates the sending *server's IP* via DNS; DKIM validates the *message content* via a cryptographic signature.

## Further reading

- [RFC 7208 — Sender Policy Framework](https://datatracker.ietf.org/doc/html/rfc7208)
- [Wikipedia: Sender Policy Framework](https://en.wikipedia.org/wiki/Sender_Policy_Framework)
