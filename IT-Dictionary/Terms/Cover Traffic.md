---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Chaff Traffic", "Dummy Traffic"]
tags: ["anonymity", "network"]
status: "note"
---

# Cover Traffic

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Chaff Traffic, Dummy Traffic

Fake messages injected into a network purely to hide the pattern of the real ones. If a link always carries traffic at a constant rate, an observer can't tell when a genuine message is sent — defeating the timing- and volume-analysis that endpoint-hiding alone leaves exposed.

**Context.** It's the defence [[Onion Routing]] omits and a [[Mixnet]] embraces: mixnets have each node emit periodic dummy packets ("loops") so the network looks uniformly busy regardless of real load. The cost is bandwidth — constant-rate cover traffic means paying for capacity you don't visibly "use" — which is why low-latency systems ration it. The same idea appears as padding in TLS/QUIC and as chaff against a [[Traffic Correlation Attack]].

## See also

- [[Mixnet]]
- [[Traffic Correlation Attack]]
- [[Onion Routing]]
