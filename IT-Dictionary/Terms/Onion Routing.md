---
type: "term"
branch: "Security"
domain: "Network Security"
tags: ["anonymity", "cryptography", "network"]
status: "developed"
---

# Onion Routing

> **Domain:** [[05 - Network Security|Network Security]]

Wrapping a message in successive layers of encryption — one per relay on the path — so each relay peels only its own layer to learn the next hop, never the whole route. [[Tor]] is its best-known implementation.

**Context.** The layering is what splits knowledge across the path: the entry relay knows your IP but not your destination, the exit knows the destination but not your IP, the middle knows neither. That property is the source of the anonymity *and* its limit — it conceals the linkage between endpoints but cannot hide traffic *timing*, which is exactly what a [[Traffic Correlation Attack]] exploits. Builds on [[Asymmetric Encryption]] and a per-hop [[Key Exchange]].

## See also

- [[Tor]]
- [[Mixnet]]
- [[Forward Secrecy]]
- [[Proxy]]

## Further reading

- [Wikipedia: Onion routing](https://en.wikipedia.org/wiki/Onion_routing)
