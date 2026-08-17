---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["Reflection Attack", "DRDoS", "Reflected DDoS"]
tags: [threat, net]
status: "developed"
---

# Amplification Attack

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** Reflection Attack, DRDoS, Reflected DDoS

A volumetric [[DDoS]] assembled from two tricks used together. **Reflection:** forge the victim's address as the source of a request, so an innocent third party delivers the reply to the victim. **Amplification:** choose a service whose reply is far larger than the request, so every byte the attacker sends arrives at the victim multiplied.

**Context.** The recipe needs a connectionless transport — [[UDP]], where a source address can be forged because nothing handshakes — plus a service that answers strangers with something bulky. Open DNS resolvers, NTP `monlist`, memcached, SSDP, and [[Portmapper|RPC portmappers]] on port 111 have all served. The *amplification factor* is the number that matters and it varies enormously: memcached reached the thousands, most others sit in the tens. Defence works at two ends and neither party is the attacker: operators close or filter their reflectors (national CERTs mail abuse notices to exactly these hosts), and networks deploy source-address validation — [BCP 38](https://www.rfc-editor.org/info/bcp38) — so forged packets never leave the origin network. Note the asymmetry that makes this persist: the reflector's owner suffers almost nothing, so the incentive to fix it is entirely external.

## See also

- [[DDoS]]
- [[UDP]]
- [[Portmapper]]
- [[Attack Surface]]
- [[Defense in Depth]]

## Often confused with

- [[DDoS]] — amplification is one technique for building a volumetric denial of service, not a separate class of attack.

## Further reading

- [Wikipedia: Denial-of-service attack](https://en.wikipedia.org/wiki/Denial-of-service_attack)
- [RFC 2827 (BCP 38): Network Ingress Filtering](https://www.rfc-editor.org/info/bcp38)
