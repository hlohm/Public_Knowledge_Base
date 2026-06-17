---
type: "term"
branch: "DevOps & SRE"
aliases: ["Service Level Agreement"]
tags: ["devops"]
status: "developed"
---

# SLA

> **Branch:** [[12 - DevOps & SRE|DevOps & SRE]]
> **Also known as:** Service Level Agreement

**S**ervice **L**evel **A**greement. The contractual promise about service levels — with defined measurement, exclusions, and consequences (typically service credits) when breached.

**Context.** The practitioner's rule: keep internal [[SLO]]s tighter than external SLAs, so your alarms ring before the lawyers do. Read SLAs cynically — '99.9% uptime' often excludes maintenance windows, measures per-month (43 minutes of allowed downtime), and remedies with credits that don't approach your actual loss.

## See also

- [[SLO]]
- [[SLI]]
- [[Error Budget]]

## Often confused with

- [[SLO]] — SLO is the internal engineering target; SLA is the external legal commitment. You miss an SLO and have a meeting; you miss an SLA and write refunds.

## Further reading

- [Wikipedia: Service-level agreement](https://en.wikipedia.org/wiki/Service-level_agreement)
