---
type: "term"
branch: "DevOps & SRE"
aliases: ["Service Level Indicator"]
tags: ["devops", "modern"]
status: "developed"
---

# SLI

> **Branch:** [[12 - DevOps & SRE|DevOps & SRE]]
> **Also known as:** Service Level Indicator

**S**ervice **L**evel **I**ndicator. The measured quantity reliability is judged by — e.g. the fraction of requests served successfully under 300 ms. Good SLIs measure what *users* experience, not what servers feel.

**Context.** SLI → [[SLO]] → [[SLA]] is the chain: the metric, the internal target on the metric, the external contract with penalties. Most monitoring failure is SLI failure — measuring CPU and memory (causes) instead of success rate and latency (symptoms), then alerting on the wrong one.

## See also

- [[SLO]]
- [[SLA]]
- [[Error Budget]]
- [[Observability]]
- [[Monitoring]]

## Further reading

- [Google SRE Book: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)
