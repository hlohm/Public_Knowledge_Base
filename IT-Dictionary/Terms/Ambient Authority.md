---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam", "principle"]
status: "developed"
---

# Ambient Authority

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

Authority a program exercises *implicitly*, just by being who it is — every action is checked against the identity's total permissions rather than against an explicit grant presented with the request. The Unix model is the canonical example: any process you run can touch anything *you* can touch.

**Context.** Ambient authority is the enabling condition for the [[Confused Deputy Problem]]: when a program's requests are honored on the strength of its identity, anyone who can influence *what* it requests inherits its whole permission set. The alternative is passing explicit, unforgeable grants with each request — [[Capability-Based Security]] — so influence over a request only ever yields the authority deliberately attached to it. The concept has new teeth with [[AI Agent]] deployments: an agent running as your user account holds your entire ambient authority (dotfiles, keys, tokens, network position), and [[Prompt Injection]] is an influence-the-request attack. Sandboxing an agent is, in access-control terms, stripping ambient authority down to an explicit, enumerated grant.

## See also

- [[Capability-Based Security]]
- [[Confused Deputy Problem]]
- [[Least Privilege]]
- [[Discretionary Access Control]]

## Further reading

- [Wikipedia: Ambient authority](https://en.wikipedia.org/wiki/Ambient_authority)
