---
type: "term"
branch: "Security"
domain: "Network Security"
de: "Firewall"
tags: ["network"]
status: "developed"
---

# Firewall

> **Domain:** [[05 - Network Security|Network Security]]
> **German:** Firewall

Filters traffic based on rules. Generations: packet-filter (L3/L4) → stateful → NGFW (application-aware) → WAF (web-specific).

**Context.** A firewall is a *policy* control, not a kind of router — forwarding and filtering are independent axes that happen to co-reside. It can run **routed** (its own IP per interface, routing between zones as it filters — the common perimeter case), **transparent / bridge** (an invisible layer-2 bump-in-the-wire that filters without an IP of its own), or **host-based** (`nftables`, `pf`, Windows Defender Firewall on a single machine, with no second network in sight). That orthogonality is the thing people get wrong: a [[Gateway]] marks *where* the boundary is, a [[Router]] decides *where* a packet goes, the firewall decides *whether* it may — and [[NAT]]'s inbound-blocking is a side effect, not an access policy.

Rulebases rot: a decade of "temporary" any-any rules, objects nobody dares delete, and shadowed rules that never match. Periodic review with hit counters, a default-deny stance both directions, and logging denies at the edges keep a firewall a control rather than furniture. Egress filtering is the chronically neglected half — C2 and exfiltration ride unrestricted outbound.

## See also

- [[Router]]
- [[Gateway]]
- [[NAT]]
- [[Proxy]]
- [[NGFW]]
- [[WAF]]
- [[IDS and IPS]]

## Often confused with

- [[Router]] — A router decides *where* a packet goes; a firewall decides *whether* it may. They share a box but answer different questions — forwarding versus policy.
- [[NAT]] — NAT rewrites addresses so private hosts share one public IP; that unsolicited inbound traffic then has nowhere to land is a by-product, not a rule set. Don't mistake it for a firewall.

## Further reading

- [Wikipedia: Firewall (computing)](https://en.wikipedia.org/wiki/Firewall_(computing))
