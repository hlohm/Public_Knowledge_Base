---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Egress Control", "Outbound Filtering"]
tags: ["network"]
status: "developed"
---

# Egress Filtering

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Egress Control, Outbound Filtering

Restricting what traffic may *leave* a network or host, rather than what may enter. The default posture almost everywhere is inbound-strict, outbound-anything — which is exactly what [[Exfiltration]], C2 callbacks, and malware staging rely on.

**Context.** The workhorse of containment design: a compromised host that can't reach out is a much smaller problem than one that can. In practice it splits into two different jobs that shouldn't be conflated — blocking *lateral* destinations (deny RFC1918 from an untrusted segment, so a popped box can't pivot inward) and constraining *internet* destinations (domain or IP allowlists, typically via a [[Proxy]], so data can't flow to arbitrary endpoints). Rule order is the classic footgun: a deny-internal rule must sit above the pass-any, or the pass shadows it. Limits worth naming: DNS itself is an egress channel (tunneling), and a domain allowlist that doesn't terminate TLS trusts the client-supplied hostname — broad allowed domains (big cloud or code-hosting platforms) remain viable exfil paths. Egress control is the load-bearing wall of AI-agent sandboxes: the allowlist is what stands between [[Prompt Injection]] and [[Exfiltration]].

## See also

- [[Firewall]]
- [[Exfiltration]]
- [[Network Segmentation]]
- [[Proxy]]
- [[DLP]]
- [[Lethal Trifecta]]

## Further reading

- [Wikipedia: Egress filtering](https://en.wikipedia.org/wiki/Egress_filtering)
