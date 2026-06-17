---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["AuthN"]
de: "Authentifizierung"
tags: ["iam", "fundamental"]
status: "note"
---

# Authentication

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** AuthN
> **German:** Authentifizierung

Proving you are who you claim to be. Often abbreviated **AuthN**.

**Context.** The AuthN/AuthZ split sounds academic until you troubleshoot: a 401 is an authentication problem, a 403 is authorization. Modern authentication strength is graded by phishing resistance — passwords < SMS codes < authenticator apps < FIDO2 — and attackers have moved to stealing the *session* after authentication, which is why token protection matters as much as login.

## See also

- [[Authorization]]
- [[MFA]]
- [[Factor]]
- [[Passwordless]]

## Often confused with

- [[Authorization]] — AuthN = 'who are you?'; AuthZ = 'what can you do?' AuthN first, then AuthZ.
