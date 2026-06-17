---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam"]
status: "note"
---

# Federation

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

Trust relationship across organizational boundaries enabling SSO between them.

**Context.** Federation moves authentication to where the identity is mastered: partner users log in with *their* IdP and your apps trust the result — no shadow accounts to provision and forget. The trust is technical (signing certificates, metadata) and contractual; expired federation certs are a classic everything-is-down-at-9am outage.

## See also

- [[SSO]]
- [[SAML]]
- [[OIDC]]
