---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Authenticated Received Chain"]
tags: ["security", "network", "email"]
status: "developed"
---

# ARC

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Authenticated Received Chain

**A**uthenticated **R**eceived **C**hain — a way for an intermediary that must modify a message to seal the authentication results it observed, so a later hop can trust that testimony instead of re-deriving it from altered content.

**Context.** It exists for the legitimate middlemen — [[Mailing List]] servers, filtering gateways, forwarders — whose changes break [[DKIM]] and whose address breaks [[SPF]], leaving a message that fails [[DMARC]] through no fault of the author. Each participating intermediary adds three headers (`ARC-Authentication-Results`, `ARC-Message-Signature`, `ARC-Seal`) forming a chain that a receiver can validate back to the original hop. The critical property is that ARC proves nothing by itself: it is a mechanism for a party to *vouch*, and a receiver may honour a chain from an intermediary it already trusts or ignore it entirely. Its value is therefore reputational, not cryptographic — the signature only establishes who is making the claim.

## See also

- [[DMARC]]
- [[DKIM]]
- [[SPF]]
- [[Mailing List]]
- [[SRS]]
- [[Email Ecosystem]]

## Often confused with

- [[DKIM]] — DKIM signs the message as its author; ARC signs what an intermediary saw before changing it.

## Further reading

- [RFC 8617 — The Authenticated Received Chain](https://datatracker.ietf.org/doc/html/rfc8617)
