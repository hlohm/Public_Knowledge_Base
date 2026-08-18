---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Honeypot address", "Spamtrap"]
tags: ["security", "network", "email"]
status: "developed"
---

# Spam Trap

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Honeypot address, Spamtrap

An email address that exists only to receive unwanted mail, so that anything arriving at it is evidence the sender did not obtain consent.

**Context.** Two kinds matter. *Pristine* traps were never used by a person and never published anywhere a legitimate sender could find them, so any mail to them was harvested or guessed. *Recycled* traps are real addresses that were abandoned, left to hard-bounce for a long period, then reactivated as traps — which means they punish exactly the practice of never pruning a list. Hitting either is a fast route onto a [[DNSBL]], and there is no way to identify traps in your own list because that would defeat the purpose. The only defence is the boring one: confirmed opt-in, prompt removal of hard bounces, and dropping addresses that have not engaged in a long time. This is why buying a list is self-defeating — it is a trap field by construction.

## See also

- [[DNSBL]]
- [[Deliverability]]
- [[IP Reputation]]
- [[Bounce]]
- [[Email Ecosystem]]

## Further reading

- [Wikipedia: Spamtrap](https://en.wikipedia.org/wiki/Spamtrap)
