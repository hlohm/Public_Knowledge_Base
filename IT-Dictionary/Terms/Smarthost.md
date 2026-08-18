---
type: "term"
branch: "Internet & Web"
aliases: ["Relay host"]
tags: ["web", "net", "email"]
status: "developed"
---

# Smarthost

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** Relay host

A designated server that other machines hand all their outbound mail to, instead of each delivering to the internet itself.

**Context.** Centralising outbound has several payoffs at once: one IP with one reputation to maintain, one place holding submission credentials, one queue to inspect when mail goes missing, and one set of authentication records to keep correct. The counterpart on each sending machine is a [[Null Client]] — no listener, no local delivery, everything relayed onward. The alternative, a full [[MTA]] on every host, spreads reputation across addresses nobody is watching and multiplies the chances that one of them is misconfigured into an [[Open Relay]].

## See also

- [[Null Client]]
- [[MTA]]
- [[MSA]]
- [[Open Relay]]
- [[IP Reputation]]
- [[Email Ecosystem]]

## Often confused with

- [[Null Client]] — the null client is the sender; the smarthost is what it sends to.

## Further reading

- [Wikipedia: Smart host](https://en.wikipedia.org/wiki/Smart_host)
