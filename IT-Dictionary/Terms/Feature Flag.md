---
type: "term"
branch: "Software Engineering"
aliases: ["Feature Toggle", "Feature Switch"]
tags: ["se", "modern"]
status: "developed"
---

# Feature Flag

> **Branch:** [[08 - Software Engineering|Software Engineering]]
> **Also known as:** Feature Toggle, Feature Switch

A runtime conditional that turns functionality on or off without redeploying — per user, percentage, or environment. Decouples *deploying* code from *releasing* it.

**Context.** Flags enable trunk-based development (merge unfinished work, dark), canary-style gradual rollouts, instant kill switches, and A/B tests — at the price of combinatorial test surface and dead-flag debt. Fowler's taxonomy (release/experiment/ops/permission toggles) and a deletion discipline keep it sane.

## See also

- [[Deployment]]
- [[Canary Release]]
- [[Trunk-based Development]]
- [[Technical Debt]]

## Further reading

- [Fowler: Feature Toggles](https://martinfowler.com/articles/feature-toggles.html)
- [Wikipedia: Feature toggle](https://en.wikipedia.org/wiki/Feature_toggle)
