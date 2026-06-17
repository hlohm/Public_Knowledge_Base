---
type: "term"
branch: "Security"
domain: "Risk & Governance"
tags: ["resilience"]
status: "note"
---

# RTO

> **Domain:** [[02 - Risk and Governance|Risk & Governance]]

**R**ecovery **T**ime **O**bjective. Maximum acceptable downtime.

**Context.** RTO dictates the recovery *mechanism*: minutes require hot standby, hours allow restore-from-backup, days tolerate re-install-from-scratch. The painful, honest test: have you ever timed a full restore? The real RTO is that number, not the one in the document.

## See also

- [[RPO]]
- [[BCP and DRP]]
