---
type: "term"
branch: "Security"
domain: "SecOps, Detection & Response"
aliases: ["Indicator of Attack"]
tags: ["secops"]
status: "note"
---

# IOA

> **Domain:** [[11 - SecOps Detection and Response|SecOps, Detection & Response]]
> **Also known as:** Indicator of Attack

**I**ndicator **o**f **A**ttack. Behavior pattern indicating attack in progress. More resilient than IOCs.

**Context.** Behavior over artifacts: "a Word process spawned PowerShell that contacted a new domain" holds even when the hash, IP, and domain all change — which is exactly why IOAs sit higher on the Pyramid of Pain. The shift from IOC-matching to IOA/behavioral detection is the core idea behind modern EDR.

## See also

- [[IOC]]
- [[MITRE ATT&CK]]
- [[TTPs]]
- [[Pyramid of Pain]]
