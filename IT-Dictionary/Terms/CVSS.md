---
type: "term"
branch: "Security"
domain: "Vulnerabilities & Exposure"
tags: ["vuln"]
status: "developed"
---

# CVSS

> **Domain:** [[09 - Vulnerabilities and Exposure|Vulnerabilities & Exposure]]

**C**ommon **V**ulnerability **S**coring **S**ystem. Severity score 0.0–10.0. Components: base, temporal, environmental. v3.1 widespread; v4.0 newer.

**Context.** Useful and routinely misused: most orgs patch off the *base* score and ignore temporal/environmental, treating an abstract 9.8 the same whether or not it's exploited or even reachable in their environment. The fix is to combine it — CVSS for inherent severity, KEV for "is it being exploited," EPSS for "will it be," plus your own asset context. v4.0 refined the metrics; the prioritization discipline matters more than the version.

## See also

- [[CVE]]
- [[EPSS]]
- [[KEV]]

## Further reading

- [FIRST: CVSS](https://www.first.org/cvss/)
