---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["Emergency Access", "Break Glass"]
tags: ["iam"]
status: "note"
---

# Break-Glass Access

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** Emergency Access, Break Glass

A pre-provisioned emergency credential or path — normally sealed and unused — for regaining control when the usual access route is gone: SSO down, the admin locked out, the primary management plane offline. Named for the fire-alarm "break glass in emergency": using it is deliberately conspicuous and audited.

**Context.** The design tension is availability versus attack surface. The credential must work when everything else has failed, so it cannot depend on the systems it exists to recover — no circular recovery dependency. Yet a standing, all-powerful account is exactly what an attacker wants, so the control is inverted from routine [[JIT Access]]: the credential exists permanently, but its *use* is alarmed — monitor the account so any activation raises an alert, since a real break-glass event is rare and an illegitimate one is an incident. Contrast [[PAM]] and [[JIT Access]], which govern *routine* elevation.

## See also

- [[JIT Access]]
- [[PAM]]
- [[Least Privilege]]
