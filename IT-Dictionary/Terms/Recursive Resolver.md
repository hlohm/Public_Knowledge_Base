---
type: "term"
branch: "Networking"
aliases: ["Recursive DNS", "Recursing Resolver", "Caching Resolver"]
tags: [net, fundamental]
status: "developed"
---

# Recursive Resolver

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Recursive DNS, Recursing Resolver, Caching Resolver

A resolver that answers a client's query in full by chasing the delegation chain itself — root → TLD → authoritative — and caching each answer by its TTL.

**Context.** This is the workhorse: when your machine asks for `example.com`, a recursive resolver (your ISP's, Quad9, or a local Unbound) does the legwork and hands back a final answer. It caches aggressively, which is why DNS changes seem to 'propagate' — you're waiting out TTLs in resolvers worldwide. Distinct from a [[DNS Forwarding|forwarder]], which punts the recursion to an upstream resolver instead of doing it.

## See also

- [[Authoritative DNS Server]]
- [[DNS Forwarding]]
- [[Stub Resolver]]
- [[TTL]]
- [[NXDOMAIN]]

## Often confused with

- [[DNS Forwarding]] — A recursive resolver walks the tree itself from the root; a forwarder hands the whole question to another resolver.

## Further reading

- [Wikipedia: Name server](https://en.wikipedia.org/wiki/Name_server)
