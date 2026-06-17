---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam"]
status: "note"
---

# Scope

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

Granular permission requested by an OAuth client (`read:email`, `write:files`).

**Context.** Scopes are least privilege for API access: request the minimum, because every granted scope is standing capability if the token leaks. Reviewing which scopes third-party apps hold against your M365 tenant (Graph permissions like `Mail.Read` on all mailboxes) is a worthwhile periodic exercise — consent phishing banks on nobody looking.

## See also

- [[OAuth 2.0]]
- [[Authorization]]
- [[Consent]]
