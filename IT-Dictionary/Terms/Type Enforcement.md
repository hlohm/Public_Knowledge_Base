---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
aliases: ["TE", "Domain Type Enforcement"]
tags: ["endpoint"]
status: "developed"
---

# Type Enforcement

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]
> **Also known as:** TE, Domain Type Enforcement

The [[Mandatory Access Control]] model at [[SELinux]]'s core: every subject and object carries a *type* label, and a global policy whitelists which types may perform which operations on which other types. Anything not explicitly allowed is denied.

**Context.** One rule shape does most of the work — `allow httpd_t httpd_sys_content_t:file { open read getattr };` — the web server's *domain* (a type applied to processes) may read web content and nothing it wasn't granted. Processes change domain only through policy-controlled [[Domain Transition]]s on `exec`, so privilege boundaries are themselves part of the policy rather than ad-hoc. The payoff over per-object lists: the policy is a closed, queryable artifact — "what can ever write to anything labeled `shadow_t`?" has a complete answer (`sesearch`), which is what makes label-based MAC analyzable in a way per-file [[ACL]]s never are.

## See also

- [[SELinux]]
- [[Mandatory Access Control]]
- [[Access Control Matrix]]

## Further reading

- [Wikipedia: Type enforcement](https://en.wikipedia.org/wiki/Type_enforcement)
