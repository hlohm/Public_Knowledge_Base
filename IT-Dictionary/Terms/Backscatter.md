---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["outscatter", "misdirected bounce", "collateral spam"]
tags: ["security", "net", "email", "anti-pattern"]
status: "developed"
---

# Backscatter

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** outscatter, collateral spam

Bounce messages sent to an innocent third party, because a server accepted a message with a forged sender and only afterwards discovered it could not deliver it. The bounce goes to the forged address, so the victim receives mail they never sent a message to provoke.

**Context.** The cause is always the same structural mistake: **accept first, decide later.** A server that takes custody of a message and then finds the recipient does not exist is obliged by [[SMTP]] to notify the [[Envelope Sender|envelope sender]] — which spam has forged. The fix is to reject *during* the SMTP transaction, while the sending server is still connected, so the rejection is that server's problem and no new message is created; in Postfix that means recipient validation (`reject_unlisted_recipient`) and [[Milter]]-time checks rather than post-queue filtering. This is precisely why a naive "backup MX" or store-and-forward spooler is a liability rather than insurance: it accepts mail for a domain whose valid recipients it does not know, and becomes a backscatter source the moment the primary is down. Emitting backscatter gets you listed on dedicated blocklists, so it damages the sender as well as the victim.

## See also

- [[SMTP]]
- [[Envelope Sender]]
- [[Open Relay]]
- [[Milter]]
- [[Greylisting]]

## Further reading

- [Wikipedia: Backscatter (email)](https://en.wikipedia.org/wiki/Backscatter_(email))
