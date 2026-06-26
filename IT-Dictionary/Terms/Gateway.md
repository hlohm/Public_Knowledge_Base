---
type: "term"
branch: "Networking"
de: "Standardgateway"
tags: ["net", "fundamental"]
status: "developed"
---

# Gateway

> **Branch:** [[04 - Networking|Networking]]
> **German:** Standardgateway

An overloaded term with two distinct senses. (1) The **default gateway** — the next-hop [[Router]] a host sends any packet whose destination falls outside its own [[Subnet]]; on a home LAN, that's your router's address. (2) A **protocol gateway** — a device that *translates* between otherwise-incompatible protocols or systems, often up to the application layer: a VoIP gateway bridging PSTN and SIP, a mail or IoT gateway, an API gateway.

**Context.** Sense (1) is why the word blurs into [[Router]]: a default gateway *is* a router — "gateway" names the role (your exit toward everything not local), not a separate box. German Windows makes this the everyday meaning, labelling the network field **Standardgateway**. The confusion is older than the products: early Internet RFCs called what we now call routers "gateways", and the term only later narrowed. Sense (2) is the one with its own substance — translation — and at layer 7 it overlaps with the [[Proxy]] and application-[[Firewall]] families. Either way a gateway is a *role / translation function*, not a security control: it marks where the boundary and the protocol change, but decides nothing about whether traffic is *allowed* — that judgement belongs to the [[Firewall]].

*How router, firewall and gateway sit on the OSI layers — and why one edge box blurs all three:*

![[router-firewall-gateway-osi.svg|583]]

## See also

- [[Router]]
- [[Firewall]]
- [[NAT]]
- [[Proxy]]
- [[Subnet]]
- [[DHCP]]

## Often confused with

- [[Router]] — A default gateway *is* a router (the next hop off your subnet). "Router" is the layer-3 forwarding function; "gateway" is the role a host points at, or — in the other sense — a higher-layer translator.
- [[Firewall]] — A gateway marks *where* the boundary/translation is; a firewall decides *whether* traffic may cross it. An edge box is both at once, but the functions are independent.
- [[Proxy]] — A proxy terminates and re-originates a connection to *represent* one side; an application gateway is that same pattern used to *translate* between protocols at the boundary. Overlapping ideas, different emphasis.

## Further reading

- [Wikipedia: Gateway (telecommunications)](https://en.wikipedia.org/wiki/Gateway_(telecommunications))
- [Wikipedia: Default gateway](https://en.wikipedia.org/wiki/Default_gateway)
