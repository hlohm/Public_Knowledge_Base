---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam"]
status: "note"
---

# Secret

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

Anything that authenticates a workload: API key, DB password, token, cert private key.

**Context.** The failure modes are mundane: secrets committed to git, baked into images, pasted in wikis and ticket comments, or living for years because rotation is scary. Scanning (gitleaks, trufflehog) finds them; a secrets manager prevents them. Treat "where do our secrets live?" as an inventory question with a written answer.

## See also

- [[Secrets Manager]]
- [[Hardcoded Secret]]
