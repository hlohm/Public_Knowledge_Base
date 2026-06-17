---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
tags: ["threat", "modern"]
status: "note"
---

# Supply Chain Attack

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]

Compromising a vendor, dependency, or build pipeline to reach downstream targets (SolarWinds, log4j, XZ Utils).

**Context.** Compromise one upstream — a build pipeline (SolarWinds), a ubiquitous library (Log4Shell, XZ backdoor), an npm/PyPI package — and inherit all its downstreams at once. The defensive frontier is provenance: SBOMs to know what you ship, dependency pinning and verification, and treating your CI/CD as tier-zero infrastructure. The XZ near-miss showed how patient and human these attacks have become.

## See also

- [[SBOM]]
- [[SCA]]
- [[TPRM]]
- [[Dependency Confusion]]
