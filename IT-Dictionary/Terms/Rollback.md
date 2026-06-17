---
type: "term"
branch: "DevOps & SRE"
aliases: ["Roll Back"]
tags: ["devops"]
status: "note"
---

# Rollback

> **Branch:** [[12 - DevOps & SRE|DevOps & SRE]]
> **Also known as:** Roll Back

Reverting a deployment to the previous known-good version — the primary mitigation when a release goes bad, valued because it's fast and requires no diagnosis.

**Context.** 'Roll back first, debug later' is the incident-response default: restore service, then investigate at leisure. The catch is state — code rolls back in seconds; a database migration that dropped a column doesn't. Hence expand-and-contract migration patterns and the habit of keeping schema changes backward-compatible for at least one release. If rollback is scary, that itself is the finding.

## See also

- [[Deployment]]
- [[Canary Release]]
- [[Blue-green Deployment]]
- [[Incident Response]]
