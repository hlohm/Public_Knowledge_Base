---
type: "term"
branch: "Security"
domain: "Vulnerabilities & Exposure"
aliases: ["Common Vulnerabilities and Exposures"]
tags: ["vuln"]
status: "developed"
---

# CVE

> **Domain:** [[09 - Vulnerabilities and Exposure|Vulnerabilities & Exposure]]
> **Also known as:** Common Vulnerabilities and Exposures

**C**ommon **V**ulnerabilities and **E**xposures. Unique ID per publicly known vulnerability: `CVE-2024-12345`. Managed by MITRE.

**Context.** The universal join key for vulnerabilities — every scanner, advisory, and patch note references the same `CVE-2024-12345`, which is the whole point. Worth knowing the ecosystem around it: NVD adds CVSS scores and metadata (with recent backlog troubles), CISA KEV flags the actively-exploited subset, and EPSS predicts which ones will be. A CVE ID alone says "a flaw exists," nothing about urgency.

## See also

- [[CWE]]
- [[CVSS]]
- [[KEV]]
- [[Vulnerability]]
- [[EPSS]]

## Often confused with

- [[CWE]] — CVE = specific instance (one bug in one product). CWE = the weakness *category* (e.g. improper input validation).

## Further reading

- [cve.org](https://www.cve.org/)
- [CVE Program](https://www.cve.org/)
