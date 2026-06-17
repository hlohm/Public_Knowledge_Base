---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
tags: [threat, modern]
status: "developed"
---

# Golden SAML

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]

The federation-layer equivalent of a [[Golden Ticket]]: by stealing the token-signing private key from an identity provider (such as AD FS), an attacker forges valid [[SAML]] assertions and authenticates to any connected service provider as anyone — bypassing passwords and [[MFA]] entirely.

**Context.** This is how on-prem compromise turns into durable cloud [[Persistence]] (it featured in the SolarWinds intrusions). Because the [[IdP and SP|service provider]] trusts anything signed by the IdP's key, the forged tokens look completely legitimate and survive cloud password resets. It targets the [[Federation]] trust itself, which is why protecting and rotating the token-signing key — and monitoring the IdP — matters so much.

## See also

- [[SAML]]
- [[Federation]]
- [[IdP and SP]]
- [[Golden Ticket]]
- [[Persistence]]
- [[OIDC]]

## Further reading

- [MITRE ATT&CK: Forge Web Credentials — SAML Tokens (T1606.002)](https://attack.mitre.org/techniques/T1606/002/)
