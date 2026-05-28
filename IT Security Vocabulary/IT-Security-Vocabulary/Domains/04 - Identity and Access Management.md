---
type: "domain"
tags: [domain]
---

# Identity & Access Management

> IAM is the load-bearing wall of the cloud era. The same words (`token`, `claim`, `assertion`) recur across protocols with related-but-distinct meanings — once you grok the IAM family, half the cloud world snaps into focus.

## Terms in this domain

- [[ABAC]] — Attribute-Based Access Control.
- [[Active Directory]] — Microsoft's directory and identity service for enterprise networks.
- [[Assertion]] — SAML's equivalent of a token: a signed XML statement about a subject.
- [[Authentication]] — Proving you are who you claim to be.
- [[Authorization]] — Determining what an authenticated principal is allowed to do.
- [[Bearer Token]] — Whoever holds the token can use it — like cash.
- [[Claim]] — A piece of information about a principal inside a token (e.g.
- [[Column-Level Security]] — Database access control, restricts columns a user can read.
- [[Consent]] — The user's explicit approval for an app to access scoped resources.
- [[Dynamic Data Masking]] —A data-protection technique that returns obfuscated values for sensitive columns at query time
- [[Factor]] — Something you know (password), have (token, phone), are (biometric), or are located (geo/IP).
- [[Federation]] — Trust relationship across organizational boundaries enabling SSO between them.
- [[FIDO2 and WebAuthn]] — Modern open standards for passwordless and phishing-resistant authentication.
- [[IAM]] — Identity and Access Management.
- [[Identity]] — A digital representation of a user, service, or device.
- [[IdP and SP]] — Identity Provider and Service Provider.
- [[JIT Access]] — Just-In-Time access.
- [[JWT]] — JSON Web Token.
- [[Kerberos]] — Ticket-based authentication protocol; backbone of Windows domain logon.
- [[LDAP]] — Lightweight Directory Access Protocol.
- [[MFA]] — Multi-Factor Authentication.
- [[OAuth 2.0]] — Authorization framework letting an app act on a user's behalf without seeing their password.
- [[OIDC]] — OpenID Connect.
- [[PAM]] — Privileged Access Management.
- [[Passkey]] — Consumer-friendly name for a FIDO2 credential, often synced via cloud (iCloud Keychain, Google Password Manager).
- [[Passwordless]] — Authentication without a password, typically using biometrics + a cryptographic device.
- [[Principal]] — The entity making a request (user, service, role).
- [[Privilege Escalation]] — Going from low-privilege access to high.
- [[RBAC]] — Role-Based Access Control.
- [[RLS]] - Row-Level Security.
- [[SAML]] — Security Assertion Markup Language.
- [[Scope]] — Granular permission requested by an OAuth client (`read:email`, `write:files`).
- [[Secret]] — Anything that authenticates a workload: API key, DB password, token, cert private key.
- [[Secrets Manager]] — Tool that stores and rotates secrets (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault).
- [[Service Account]] — Non-human identity used by applications.
- [[SSO]] — Single Sign-On.
- [[Token]] — Access token: short-lived, presented to APIs.

---
← Back to [[_Home]]