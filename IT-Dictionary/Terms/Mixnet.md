---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Mix Network"]
tags: ["anonymity", "network", "cryptography"]
status: "developed"
---

# Mixnet

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Mix Network

An anonymity network that routes each message through a chain of relays ("mixes"), where every mix batches, reorders, and delays the messages it forwards so an observer cannot link a message going in to one coming out. Unlike low-latency [[Onion Routing]], a mixnet deliberately trades latency for resistance to traffic analysis.

**Context.** Onion routing (Tor) hides *who talks to whom* but preserves packet timing, which a global observer can exploit with a [[Traffic Correlation Attack]]; a mixnet attacks that timing channel directly by reordering and padding traffic, typically with constant-rate [[Cover Traffic]] so the network always looks equally busy. Modern designs (Loopix, Nym) fix every packet to a uniform size with the [[Sphinx Packet Format]] and add per-hop delay. The price is real latency, so mixnets suit metadata-resistant messaging and payments more than web browsing.

## See also

- [[Onion Routing]]
- [[Cover Traffic]]
- [[Sphinx Packet Format]]
- [[Traffic Correlation Attack]]
- [[Unlinkability]]

## Further reading

- [Wikipedia: Mix network](https://en.wikipedia.org/wiki/Mix_network)
