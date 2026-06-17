---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["IdP", "\"SP\"", "\"Identity Provider\"", "\"Service Provider\""]
tags: ["iam"]
status: "note"
---

# IdP and SP

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** IdP, "SP", "Identity Provider", "Service Provider"

**I**dentity **P**rovider and **S**ervice **P**rovider. IdP authenticates the user; SP is the app the user wants to access.

**Context.** The mental model for every SSO flow: the SP never sees a password; it redirects to the IdP and trusts the signed result. Flows can be SP-initiated (user starts at the app) or IdP-initiated (user starts at a portal) — knowing which one is in play is half of SSO troubleshooting.

## See also

- [[SSO]]
- [[SAML]]
- [[OIDC]]
