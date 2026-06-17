---
type: "term"
branch: "DevOps & SRE"
tags: [devops, modern]
status: "developed"
---

# Canary Release

> **Branch:** [[12 - DevOps & SRE|DevOps & SRE]]

Rolling out a change to a small subset of users first, monitoring it, then gradually expanding if healthy — limiting the blast radius of a bad release.

**Context.** Named after canaries in coal mines. The progressive, risk-managed counterpart to blue-green's all-at-once flip. Pairs naturally with automated rollback triggered by error/latency metrics, and with feature flags for fine-grained control.

## See also

- [[Blue-green Deployment]]
- [[Feature Flag]]
- [[Observability]]
- [[Rollback]]
- [[Blast Radius]]

## Further reading

- [Wikipedia: Feature toggle](https://en.wikipedia.org/wiki/Feature_toggle)
