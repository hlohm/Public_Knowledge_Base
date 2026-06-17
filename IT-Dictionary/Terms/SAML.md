---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam", "protocol"]
status: "note"
---

# SAML

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

**S**ecurity **A**ssertion **M**arkup **L**anguage. XML-based SSO protocol, dominant in enterprise. Older but still everywhere.

**Context.** Old but load-bearing: most enterprise SSO integrations are still "configure SAML", and the setup ritual — exchange metadata, map attributes, agree on NameID — is a recurring helpdesk-adjacent task. XML signature handling has produced famous vulnerabilities (signature wrapping, round-trip parsing bugs), one reason new builds prefer OIDC.

## See also

- [[OIDC]]
- [[SSO]]
- [[Assertion]]
- [[Federation]]
