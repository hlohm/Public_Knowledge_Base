---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["OAuth"]
tags: [iam, protocol]
status: "developed"
---

# OAuth 2.0

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** OAuth

Authorization framework letting an app act on a user's behalf without seeing their password.

**Context.** OAuth is for **authorization**, not authentication — using it for AuthN without OIDC on top is a classic mistake.

## See also

- [[OIDC]]
- [[Scope]]
- [[Token]]
- [[Bearer Token]]

## Often confused with

- [[OIDC]] — OAuth = delegated authorization; OIDC = authentication built on top of OAuth.

## Further reading

- [RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749)
