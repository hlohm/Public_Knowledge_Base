---
type: "term"
branch: "Software Engineering"
de: "Abhängigkeit"
tags: [se, fundamental]
status: "developed"
---

# Dependency

> **Branch:** [[08 - Software Engineering|Software Engineering]]
> **German:** Abhängigkeit

External code your project relies on. The dependency *graph* — your deps, their deps, transitively — is what package managers resolve and what you ultimately ship and trust.

**Context.** Every dependency is attack surface and maintenance burden (supply-chain attacks, left-pad, Log4Shell). Lockfiles pin exact versions for reproducibility; the cultural pendulum is swinging back toward fewer, more-trusted dependencies.

## See also

- [[Semantic Versioning]]
- [[Package Manager]]
- [[Supply Chain Attack]]
- [[Lockfile]]
- [[Transitive Dependency]]

## Further reading

- [Wikipedia: Coupling (computer programming)](https://en.wikipedia.org/wiki/Coupling_(computer_programming))
