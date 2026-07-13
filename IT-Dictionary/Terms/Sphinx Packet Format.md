---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Sphinx"]
tags: ["anonymity", "cryptography", "network"]
status: "note"
---

# Sphinx Packet Format

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Sphinx

A cryptographic packet format for [[Mixnet|mix networks]] in which every packet is a fixed size and carries layered ("onion") encryption so each hop learns only the next hop. Its design goals are bitwise unlinkability between a packet's incoming and outgoing forms, resistance to replay and tagging attacks, and support for anonymous replies via [[SURB|reply blocks]].

**Context.** Fixed size is the whole point: if packets never change length, an observer can't correlate them across a hop by size, and padding to a constant size closes a channel that plain [[Onion Routing]] leaves open. Each layer is independently authenticated so an attacker can't "tag" a packet and recognise it downstream. Sphinx (Danezis & Goldberg, 2009) underpins the Loopix and Nym mixnets.

## See also

- [[Mixnet]]
- [[SURB]]
- [[Onion Routing]]
