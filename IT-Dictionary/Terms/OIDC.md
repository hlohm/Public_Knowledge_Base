---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["OpenID Connect"]
tags: ["iam", "protocol"]
status: "developed"
---

# OIDC

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** OpenID Connect

**O**pen**ID** **C**onnect. An authentication layer built on top of OAuth 2.0. Adds an **ID token** (a JWT) that proves *who* the user is.

**Context.** The default choice for anything new: JSON and REST where SAML is XML and SOAP, with first-class support for mobile and SPA flows. The current best practice is authorization code flow with PKCE for public clients. SAML persists in legacy enterprise apps; OIDC is everywhere else.

## See also

- [[OAuth 2.0]]
- [[JWT]]
- [[Token]]
- [[SAML]]

## Often confused with

- [[OAuth 2.0]] — OAuth is authorization; OIDC adds authentication on top.
- [[SAML]] — Both do federated SSO. SAML = older, XML, enterprise-heavy. OIDC = newer, JSON/JWT, mobile/API-friendly.

## Further reading

- [OpenID Connect specifications](https://openid.net/developers/specs/)
