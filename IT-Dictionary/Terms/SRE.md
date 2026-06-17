---
type: "term"
branch: "DevOps & SRE"
aliases: ["Site Reliability Engineering", "Site Reliability Engineer"]
tags: ["devops", "modern"]
status: "developed"
---

# SRE

> **Branch:** [[12 - DevOps & SRE|DevOps & SRE]]
> **Also known as:** Site Reliability Engineering, Site Reliability Engineer

**S**ite **R**eliability **E**ngineering — Google's formulation of operations as a software problem: engineers run production, automate away [[Toil]], and manage reliability quantitatively via SLOs and error budgets.

**Context.** The error budget is the intellectual core: pick a target (99.9%), and the allowed 0.1% of failure becomes a *budget* — spend it on shipping fast, freeze releases when it's exhausted. This converts the eternal dev-vs-ops fight into arithmetic. SRE is one concrete implementation of DevOps ideas; the free Google SRE book is the canon.

## See also

- [[SLO]]
- [[SLI]]
- [[Error Budget]]
- [[Toil]]
- [[DevOps]]
- [[Postmortem]]

## Further reading

- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
- [Wikipedia: Site reliability engineering](https://en.wikipedia.org/wiki/Site_reliability_engineering)
