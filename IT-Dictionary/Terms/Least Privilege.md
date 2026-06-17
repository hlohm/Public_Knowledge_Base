---
type: "term"
branch: "Security"
domain: "Core Principles & Models"
aliases: ["PoLP", "\"Principle of Least Privilege\""]
de: "Minimalprinzip / Prinzip der geringsten Rechte"
tags: ["principle"]
status: "developed"
---

# Least Privilege

> **Domain:** [[01 - Core Principles|Core Principles & Models]]
> **Also known as:** PoLP, "Principle of Least Privilege"
> **German:** Minimalprinzip / Prinzip der geringsten Rechte

Give every user and process the minimum access required to do its job. The bedrock principle behind nearly every IAM and infrastructure decision.

**Context.** In practice this is a constant fight against entropy: permissions accumulate, nobody removes them, and "temporary" admin rights become permanent. Access reviews, JIT elevation, and role-based grants are the counterweights. When a request lands on the helpdesk, the right question is "what do you need to *do*", not "what access do you want".

## See also

- [[Need to Know]]
- [[RBAC]]
- [[JIT Access]]
- [[Separation of Duties]]

## Further reading

- [NIST Glossary: Least Privilege](https://csrc.nist.gov/glossary/term/least_privilege)
