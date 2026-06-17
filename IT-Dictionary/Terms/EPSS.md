---
type: "term"
branch: "Security"
domain: "Vulnerabilities & Exposure"
aliases: ["Exploit Prediction Scoring System"]
tags: ["vuln"]
status: "developed"
---

# EPSS

> **Domain:** [[09 - Vulnerabilities and Exposure|Vulnerabilities & Exposure]]
> **Also known as:** Exploit Prediction Scoring System

**E**xploit **P**rediction **S**coring **S**ystem. Probability a vuln will be exploited in the next 30 days. Pairs nicely with CVSS for prioritization.

**Context.** Answers the question CVSS can't: of the thousands of CVEs scored "high," which will actually be exploited soon? It's a data-driven probability, updated daily, and it cuts patch backlogs dramatically — the overwhelming majority of CVEs never see exploitation. Use it to triage *below* KEV: KEV says "exploited now, patch immediately," EPSS ranks the maybes.

## See also

- [[CVSS]]
- [[KEV]]

## Further reading

- [FIRST: EPSS](https://www.first.org/epss/)
