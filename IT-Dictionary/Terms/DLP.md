---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
aliases: ["Data Loss Prevention"]
tags: ["endpoint", "data"]
status: "note"
---

# DLP

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]
> **Also known as:** Data Loss Prevention

**D**ata **L**oss **P**revention. Stops sensitive data from leaving (USB, email, upload). Endpoint, network, or cloud-delivered.

**Context.** DLP is only as smart as the data classification feeding it — without labels it's regex for credit-card numbers and a flood of false positives. Start in monitor mode to learn actual data flows, block only the unambiguous (e.g. unencrypted customer lists to private mail), and expect the policy debates to be organizational, not technical. In M365, Purview is the native implementation.

## See also

- [[Data Classification]]
- [[CASB]]
