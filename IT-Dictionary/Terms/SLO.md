---
type: "term"
branch: "DevOps & SRE"
aliases: ["Service Level Objective"]
tags: [devops, modern]
status: "developed"
---

# SLO

> **Branch:** [[12 - DevOps & SRE|DevOps & SRE]]
> **Also known as:** Service Level Objective

A target value for a reliability metric (an SLI) over a window — e.g. 99.9% of requests succeed within 300ms over 30 days. The internal goal that drives engineering decisions.

**Context.** The crucial SRE trio: an **SLI** is the measurement, the **SLO** is the target, the **SLA** is the contractual promise (with penalties) — usually set looser than the SLO so you have margin. The SLO defines your **error budget**: the allowed unreliability you can 'spend' on shipping faster.

## See also

- [[SLA]]
- [[SLI]]
- [[Error Budget]]
- [[SRE]]
- [[Reliability]]

## Often confused with

- [[SLA]] — SLI = the metric you measure; SLO = your internal target for it; SLA = the external contract with consequences. Tighten inward: SLA looser than SLO.

## Further reading

- [Wikipedia: Service-level objective](https://en.wikipedia.org/wiki/Service-level_objective)
