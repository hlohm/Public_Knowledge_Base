---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
tags: ["endpoint"]
status: "note"
---

# Application Allowlisting

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]

Only pre-approved binaries may execute. Strong control with high operational burden.

**Context.** Inverts the malware problem: instead of recognizing bad, only allow known-good — unsigned ransomware simply doesn't execute. Windows tooling: AppLocker, WDAC, Smart App Control. Honest scoping: superb on servers and kiosks where software changes rarely; on general workstations the exception-management workload is the price, and audit-mode-first is the only sane rollout.

## See also

- [[Hardening]]
- [[LotL]]
