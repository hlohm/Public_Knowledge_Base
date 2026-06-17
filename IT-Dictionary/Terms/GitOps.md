---
type: "term"
branch: "DevOps & SRE"
tags: [devops, modern]
status: "developed"
---

# GitOps

> **Branch:** [[12 - DevOps & SRE|DevOps & SRE]]

An operational model where a Git repository is the single source of truth for declarative infrastructure and apps, and an agent continuously reconciles the live system to match it.

**Context.** Extends Infrastructure-as-Code with Git's review, audit, and rollback (revert the commit) as the deployment mechanism. The pull-based reconciliation (Argo CD, Flux) means the cluster converges to the repo state, and drift is detected and corrected automatically.

## See also

- [[Infrastructure as Code]]
- [[Declarative Configuration]]
- [[Kubernetes]]
- [[CI-CD|CI/CD]]
- [[Reconciliation Loop]]

## Further reading

- [Wikipedia: DevOps](https://en.wikipedia.org/wiki/DevOps)
