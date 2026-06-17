---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam"]
status: "note"
---

# Consent

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

The user's explicit approval for an app to access scoped resources.

**Context.** Consent phishing weaponizes this: a malicious app requests plausible-sounding scopes, one user clicks accept, and the attacker reads mail through a legitimate, MFA-immune OAuth grant. In M365, restricting user consent and routing app approvals through admin consent workflow is one of the highest-value tenant settings.

## See also

- [[OAuth 2.0]]
- [[Scope]]
