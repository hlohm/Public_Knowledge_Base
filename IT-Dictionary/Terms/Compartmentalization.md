---
type: "term"
branch: "Security"
domain: "Core Principles & Models"
aliases: ["Compartmentation"]
tags: ["principle", "opsec", "privacy"]
status: "developed"
---

# Compartmentalization

> **Domain:** [[01 - Core Principles|Core Principles & Models]]
> **Also known as:** Compartmentation

Keeping identities, activities, and infrastructure separated so a compromise or correlation in one compartment doesn't expose the others — the operational-security counterpart to [[Need to Know]] and [[Least Privilege]].

**Context.** In an anonymity setting the decisive risk is rarely the cryptography but the *metadata graph* — the web of reused handles, shared devices, billing details, and identity-linked infrastructure that quietly ties a "private" activity back to a person. The canonical lesson is the Silk Road takedown: [[Tor]] was never broken; the operator was undone by an early forum post linking a pseudonym to his real email, a server misconfiguration leaking the true IP, and finally physical surveillance — every failure in the compartmentalization layer, none in the crypto. Practical form: a clean device, an unrelated network, no account or handle reuse, and never routing sensitive activity through systems registered in your real name.

## See also

- [[Need to Know]]
- [[Least Privilege]]
- [[Defense in Depth]]
- [[Traffic Correlation Attack]]

## Often confused with

- [[Least Privilege]] — least privilege limits *what one identity is allowed to do*; compartmentalization limits *what one identity reveals about another* by keeping them apart.

## Further reading

- [Wikipedia: Compartmentalization (information security)](https://en.wikipedia.org/wiki/Compartmentalization_(information_security))
