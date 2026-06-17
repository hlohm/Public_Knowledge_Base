---
type: "term"
branch: "Security"
domain: "Application Security"
tags: ["appsec", "modern"]
status: "note"
---

# Dependency Confusion

> **Domain:** [[08 - Application Security|Application Security]]

Tricking a package manager into installing the attacker's public package instead of your private one.

**Context.** A 2021 disclosure that earned bounties at dozens of major companies: publish a *public* package matching the name of a company's *private* one with a higher version, and misconfigured installers grab yours. The fix is registry hygiene — scoped/namespaced packages, explicit private-registry pinning, and refusing public fallback for internal names.

## See also

- [[Supply Chain Attack]]
- [[Typosquatting]]
