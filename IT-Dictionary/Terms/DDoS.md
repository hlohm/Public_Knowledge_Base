---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["DoS", "\"Denial of Service\""]
tags: ["threat"]
status: "developed"
---

# DDoS

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** DoS, "Denial of Service"

**D**istributed **D**enial of **S**ervice (or plain **DoS**). Overwhelming a service to make it unavailable. DDoS uses many sources, often a botnet.

**Context.** Three flavors to distinguish: volumetric (saturate the pipe — often amplified via DNS/NTP reflection), protocol (exhaust state, e.g. SYN floods), and application-layer (cheap requests that are expensive to serve). You don't out-buy a volumetric flood on your own link — mitigation means an upstream scrubbing service or CDN, arranged *before* the attack.

## See also

- [[Botnet]]
- [[CIA Triad]]

## Further reading

- [Cloudflare: What is a DDoS attack?](https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/)
