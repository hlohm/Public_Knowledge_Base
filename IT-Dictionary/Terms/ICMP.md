---
type: "term"
branch: "Networking"
aliases: ["Internet Control Message Protocol"]
tags: ["net", "fundamental"]
status: "developed"
---

# ICMP

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Internet Control Message Protocol

**I**nternet **C**ontrol **M**essage **P**rotocol. IP's control channel: echo request/reply (ping), destination unreachable, TTL exceeded (traceroute), fragmentation needed.

**Context.** ICMP is diagnostics *and* plumbing: path-MTU discovery depends on 'fragmentation needed' messages, so the reflexive firewall habit of blocking *all* ICMP causes the infamous black-hole symptom — small packets pass, big transfers hang. Block what you must (echo from the internet, redirects), but let the error types through. Ping answering says only that ICMP is allowed; ping failing proves almost nothing about the service you actually care about.

## See also

- [[IP]]
- [[Firewall]]
- [[Latency]]
- [[Router]]

## Further reading

- [RFC 792 — ICMP](https://datatracker.ietf.org/doc/html/rfc792)
- [Wikipedia: Internet Control Message Protocol](https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol)
