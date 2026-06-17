---
type: "term"
branch: "Networking"
aliases: ["DNS Forwarder", "Conditional Forwarding"]
tags: [net]
status: "developed"
---

# DNS Forwarding

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** DNS Forwarder, Conditional Forwarding

Configuring a resolver to hand queries (all of them, or just for certain domains) to a specified upstream resolver instead of recursing from the root itself.

**Context.** *Conditional* forwarding is the useful variant: send only `corp.example` to the internal AD nameserver, recurse everything else normally. The tradeoff vs full recursion is dependency — a forwarder is only as available and trustworthy as its upstream, and a forwarded query leaves your network. The opposite design choice (be authoritative locally and never forward for a name) is what a `static` local-zone gives you: undefined names fail locally instead of leaking to the forwarder.

## See also

- [[Recursive Resolver]]
- [[Authoritative DNS Server]]
- [[Split-horizon DNS]]

## Often confused with

- [[Recursive Resolver]] — Forwarding delegates the lookup to another resolver; recursion does the root-down walk in-house.
