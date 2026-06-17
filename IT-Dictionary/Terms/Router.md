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

## See also

- [[Switch]]
- [[Subnet]]
- [[IP]]
- [[NAT]]
- [[Firewall]]

## Often confused with

- [[Switch]] — A switch forwards frames by MAC *within* one network; a router forwards packets by IP *between* networks. The L2/L3 boundary in physical form.

## Further reading

- [Wikipedia: Router (computing)](https://en.wikipedia.org/wiki/Router_(computing))
