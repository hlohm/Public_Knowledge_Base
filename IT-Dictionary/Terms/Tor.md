---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["The Onion Router"]
tags: ["anonymity", "privacy", "network"]
status: "developed"
---

# Tor

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** The Onion Router

A volunteer-run anonymity network that wraps traffic in layered encryption and bounces it through three relays via [[Onion Routing]], so no single relay knows both your identity and your destination.

**Context.** Running a relay and using Tor as a client are separate functions: a relay carries *other people's* traffic and strengthens the whole network's anonymity, while your own client builds its own circuits and by default does **not** route through your relay. Tor gives anonymity, not invisibility — it hides *who* talks to *whom*, but a [[Traffic Correlation Attack]] by an adversary who can watch both ends still threatens it, and the first hop (your [[Entry Guard]]) always sees your real IP. The famous failures (e.g. Silk Road) came from operator [[Compartmentalization]] and metadata mistakes, never from breaking the crypto.

## See also

- [[Onion Routing]]
- [[Entry Guard]]
- [[Traffic Correlation Attack]]
- [[Pluggable Transport]]

## Often confused with

- [[VPN]] — a VPN routes through one provider you must trust and that sees everything; Tor distributes trust across three independent relays so no single one links source to destination.

## Further reading

- [Wikipedia: Tor (network)](https://en.wikipedia.org/wiki/Tor_(network))
