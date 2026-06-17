---
type: "term"
branch: "Networking"
aliases: ["Goodput"]
de: "Durchsatz"
tags: ["net", "fundamental"]
status: "developed"
---

# Throughput

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Goodput
> **German:** Durchsatz

The data rate actually achieved over a path, as opposed to the link's rated capacity. **Goodput** narrows it further to useful application data, after protocol overhead and retransmissions.

**Context.** Bandwidth is the pipe, throughput is the water: a gigabit link delivering 40 MB/s isn't broken, it's experiencing TCP's reality — window size, RTT, and loss set a hard ceiling (high latency throttles even fat pipes; that's the bandwidth-delay product). When users say 'the network is slow,' deciding whether the complaint is throughput or [[Latency]] is the first fork in the diagnosis.

## See also

- [[Bandwidth]]
- [[Latency]]
- [[TCP]]
- [[QUIC]]

## Often confused with

- [[Bandwidth]] — Bandwidth is the theoretical maximum of the link; throughput is what you measured. The gap between them is where troubleshooting lives.

## Further reading

- [Wikipedia: Network throughput](https://en.wikipedia.org/wiki/Network_throughput)
