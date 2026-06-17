---
type: "term"
branch: "DevOps & SRE"
tags: ["devops", "fundamental"]
status: "developed"
---

# Monitoring

> **Branch:** [[12 - DevOps & SRE|DevOps & SRE]]

Collecting and watching predefined signals — metrics, logs, health checks — and alerting when they cross thresholds. The classic 'is it broken?' machinery, as distinct from [[Observability]]'s 'why?'.

**Context.** The craft is in what you alert on: symptoms users feel (error rate, latency — the [[SLI]]s), not every cause you can measure, because cause-based alerting is how teams drown in [[Alert Fatigue|noise]] and miss the real page. The Google SRE 'four golden signals' (latency, traffic, errors, saturation) remain the best starting checklist.

## See also

- [[Observability]]
- [[SLI]]
- [[SLO]]
- [[SIEM]]

## Often confused with

- [[Observability]] — Monitoring asks known questions of known failure modes; observability instruments richly enough to ask new questions about failures you didn't predict.

## Further reading

- [Google SRE Book: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
