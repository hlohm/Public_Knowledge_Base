---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["End-to-End Correlation", "Traffic Confirmation"]
tags: ["anonymity", "attack", "privacy"]
status: "developed"
---

# Traffic Correlation Attack

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** End-to-End Correlation, Traffic Confirmation

Deanonymising a low-latency network like [[Tor]] by observing traffic *entering* it (from the client) and *leaving* it (toward the destination) and matching the two on timing and volume — without ever breaking the encryption.

**Context.** This is the attack [[Onion Routing]] structurally *cannot* stop: Tor hides the linkage between hops but preserves end-to-end timing, so an adversary who sees both ends correlates the patterns. Hence the textbook limitation — Tor does not defend against a *global passive adversary* who can watch a large share of the network. Your choice of first hop doesn't help, either: the correlation is between your uplink and the exit/destination, so fronting Tor with your own VPN changes nothing here — the tunnel sits *before* the entry, not between entry and exit.

## See also

- [[Tor]]
- [[Onion Routing]]
- [[Entry Guard]]

## Often confused with

- [[MITM]] — a man-in-the-middle actively *intercepts and can alter* traffic; correlation is *passive observation* of both ends, never touching the contents.

## Further reading

- [Wikipedia: Traffic analysis](https://en.wikipedia.org/wiki/Traffic_analysis)
