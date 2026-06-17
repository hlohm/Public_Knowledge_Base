---
type: "term"
branch: "Security"
domain: "Application Security"
aliases: ["Software Composition Analysis"]
tags: ["appsec"]
status: "note"
---

# SCA

> **Domain:** [[08 - Application Security|Application Security]]
> **Also known as:** Software Composition Analysis

**S**oftware **C**omposition **A**nalysis. Scanning third-party dependencies for known vulns.

**Context.** Since most application code is now third-party dependencies, this is where most of your known vulnerabilities live — and it's the highest-ROI scan to run first. The traps: transitive dependencies (the vuln is three levels deep), and alert fatigue from vulnerable-but-unreachable code, which reachability analysis in newer tools tries to cut. Dependabot/Renovate close the loop by automating the bump.

## See also

- [[SBOM]]
- [[Supply Chain Attack]]
- [[Vulnerability Management]]
- [[Dependency Confusion]]
