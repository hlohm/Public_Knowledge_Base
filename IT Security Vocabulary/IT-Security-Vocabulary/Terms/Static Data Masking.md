---
domain: "Application Security"
aliases: ["SDM", "Static Masking"]
tags: [appsec, data, privacy]
---

# Static Data Masking

> **Domain:** [[08 - Application Security|Application Security]]
> **Also known as:** SDM

Permanently replacing sensitive data with realistic but fake values to produce a safe, **non-production copy** — so developers, testers, and analysts can work with data that looks and behaves like the real thing without ever touching actual PII. The masking happens once, up front, and the real values are gone from the resulting dataset.

**Context.** Where [[DDM]] disguises live production data *at read time* (the real values still sit underneath), SDM creates a *separate, sanitized dataset* from which the originals can't be recovered. That makes it the right tool for anything that leaves production: dev and test environments, training data, demos, analytics sandboxes, data handed to third parties — all frequent sources of breaches when real data ends up somewhere poorly guarded. The driver is usually privacy and compliance — [[Data Classification|classify]] what's sensitive, then keep it out of lower environments. Worth knowing but not yet worth memorizing: good masking has to preserve *referential integrity and statistical shape* so the fake data stays useful — that's the genuinely hard part, and a detail for the day you actually configure it.

Conceptually it's *not* a fourth "axis" of the live table the way [[RLS]] / [[CLS]] / [[DDM]] are — those three control access to production data in place. SDM steps off the table entirely and manufactures a different dataset.

## See also

- [[DDM]]
- [[CLS]]
- [[RLS]]
- [[Data Classification]]
- [[GDPR]]
- [[DLP]]
- [[SDLC]]
- [[Need to Know]]

## Often confused with

- [[DDM]] — Both "mask" sensitive fields, but DDM works on live production data at query time (real values remain underneath); SDM produces a permanently sanitized duplicate for use outside production. Dynamic = disguise in place; static = sanitize a copy.

## Further reading

- [Wikipedia: Data masking](https://en.wikipedia.org/wiki/Data_masking)
