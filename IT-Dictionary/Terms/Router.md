---
type: "term"
branch: "Networking"
tags: ["net", "fundamental"]
status: "developed"
---

# Router

> **Branch:** [[04 - Networking|Networking]]

A layer-3 device that forwards packets *between* networks, choosing the next hop per destination from its routing table (longest prefix match) and decrementing TTL on the way.

**Context.** The router is where subnets meet — and therefore where filtering naturally lives, which is why home 'routers' are really router+switch+AP+firewall in one box. The default route (`0.0.0.0/0`) is the 'everything else goes here' entry; 'no route to host' and TTL-exceeded (the mechanism traceroute exploits) are its characteristic error signatures.

From a host's point of view, that next-hop router is its **default gateway** — "gateway" there is a *role* a router fills, not a separate device (see [[Gateway]]). And routing is orthogonal to filtering: a box can forward without a single rule, while a [[Firewall]] can filter without routing at all (transparent or host-based). They usually ride together in one appliance, which is exactly why router, gateway and firewall blur in everyday speech.

## See also

- [[Switch]]
- [[Subnet]]
- [[IP]]
- [[NAT]]
- [[Firewall]]
- [[Gateway]]

## Often confused with

- [[Switch]] — A switch forwards frames by MAC *within* one network; a router forwards packets by IP *between* networks. The L2/L3 boundary in physical form.
- [[Gateway]] — A default gateway *is* a router (the next hop off your subnet); "gateway" also names a higher-layer protocol translator. Router is the function; gateway is a role/word layered on top of it.

## Further reading

- [Wikipedia: Router (computing)](https://en.wikipedia.org/wiki/Router_(computing))
