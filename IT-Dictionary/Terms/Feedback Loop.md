---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["FBL", "Complaint Feedback Loop"]
tags: ["security", "network", "email"]
status: "developed"
---

# Feedback Loop

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** FBL, Complaint Feedback Loop

An arrangement by which a mailbox provider reports back to a sender that one of its users marked a message as spam.

**Context.** Senders register with each provider that offers one; reports arrive in a structured format (ARF) and are expected to be acted on immediately by suppressing that recipient — continuing to mail someone who has complained is the single clearest signal of a sender not worth trusting. Complaint rate is now an explicit threshold rather than a soft signal: Gmail publishes roughly 0.3 % as the line not to cross, and consistently exceeding it degrades delivery for everything you send. The related obligation is making complaint unnecessary in the first place, via a working `List-Unsubscribe` header and one-click unsubscribe (RFC 8058) — a user who cannot find the unsubscribe button will use the junk button instead.

## See also

- [[Deliverability]]
- [[IP Reputation]]
- [[ESP]]
- [[Spam Trap]]
- [[Email Ecosystem]]

## Further reading

- [RFC 5965 — An Extensible Format for Email Feedback Reports](https://datatracker.ietf.org/doc/html/rfc5965)
