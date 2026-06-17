---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["Workload Identity"]
de: "Dienstkonto"
tags: ["iam"]
status: "note"
---

# Service Account

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** Workload Identity
> **German:** Dienstkonto

Non-human identity used by applications. The hardest identities to manage well.

**Context.** Hardest because nobody owns them: passwords set once in 2014, interactive logon nobody disabled, and permissions sized for whatever the vendor demanded. Hygiene list: an owner per account, no interactive logon, gMSAs on Windows where possible, and monitoring for service accounts doing human-shaped things.

## See also

- [[Secret]]
- [[Secrets Manager]]
- [[CIEM]]
