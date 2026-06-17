---
type: "term"
branch: "Security"
domain: "Risk & Governance"
tags: ["resilience"]
status: "note"
---

# RPO

> **Domain:** [[02 - Risk and Governance|Risk & Governance]]

**R**ecovery **P**oint **O**bjective. Maximum acceptable data loss, measured in time (e.g. 15 minutes).

**Context.** RPO dictates backup frequency: a 15-minute RPO means continuous replication or very frequent snapshots; a 24-hour RPO permits a nightly job. State it per system — the ERP database and the wiki do not deserve the same number.

## See also

- [[RTO]]
- [[BCP and DRP]]

## Often confused with

- [[RTO]] — RPO = data loss tolerance; RTO = downtime tolerance.
