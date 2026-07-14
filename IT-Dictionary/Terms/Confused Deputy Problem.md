---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["Confused Deputy"]
tags: ["iam", "principle"]
status: "developed"
---

# Confused Deputy Problem

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** Confused Deputy

A privileged program tricked into misusing its *own* legitimate authority on an attacker's behalf. The attacker never gains privileges — they borrow the deputy's.

**Context.** Norm Hardy's 1988 formulation: a compiler with permission to write its billing file is handed that file's name as an "output path" by a user who couldn't write it themselves. The pattern recurs wherever a service holds more authority than the request that reaches it: [[CSRF]] (the browser is the deputy, wielding your cookies), [[SSRF]] (the server is the deputy, wielding its network position), setuid binaries, cloud metadata abuse via [[IMDS]]. The structural fix is making authority travel *with* designation instead of ambiently — the core argument for [[Capability-Based Security]] over [[Ambient Authority]]. The newest deputy is the [[AI Agent]]: it holds its operator's file, network, and connector authority, and [[Prompt Injection]] is precisely the trick that redirects that authority — which is why agent containment is access-control design, not prompt engineering.

## See also

- [[Capability-Based Security]]
- [[Ambient Authority]]
- [[CSRF]]
- [[SSRF]]
- [[Prompt Injection]]
- [[Least Privilege]]

## Further reading

- [Wikipedia: Confused deputy problem](https://en.wikipedia.org/wiki/Confused_deputy_problem)
