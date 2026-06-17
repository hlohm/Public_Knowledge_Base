---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Guard Node", "Guard Relay"]
tags: ["anonymity", "network"]
status: "developed"
---

# Entry Guard

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Guard Node, Guard Relay

The first relay in a [[Tor]] circuit — chosen from a small, persistent set rather than freshly at random, because the entry point is the one hop that sees your real IP.

**Context.** The guard set is deliberately small and slow to rotate: cycling through many entries would, over time, almost guarantee an adversary eventually lands on one they control, so a stable handful *lowers* that probability. Two operator mistakes follow from missing this — pinning your *own* relay as your guard (via `EntryNodes`) makes your entry static, publicly listed, and identity-linked, throwing away the rotation protection; and the guard seeing your IP is by design, not a leak, which is why hiding the *fact* you use Tor is a job for a [[Pluggable Transport]] or [[Tor Bridge]], not for path-tweaking.

## See also

- [[Tor]]
- [[Tor Bridge]]
- [[Onion Routing]]

## Often confused with

- [[Tor Bridge]] — a guard is a *public, listed* relay used as a normal first hop; a bridge is an *unlisted* entry whose purpose is to hide that you're reaching Tor at all.

## Further reading

- [Tor specification: Guard relays](https://spec.torproject.org/guard-spec)
