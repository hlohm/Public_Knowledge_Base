---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam"]
status: "note"
---

# Assertion

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

SAML's equivalent of a token: a signed XML statement about a subject.

**Context.** When SAML SSO breaks, the assertion is what you debug: grab it from browser dev tools (it's base64 in a form POST), decode it, and check NameID format, audience, conditions, and clock skew. Signature validation failures and attribute-mapping mismatches cover most tickets.

## See also

- [[SAML]]
- [[Claim]]
