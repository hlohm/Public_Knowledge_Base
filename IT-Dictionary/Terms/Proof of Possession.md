---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["PoP", "Sender-Constrained Token", "Proof-of-Possession Token", "Holder-of-Key"]
tags: [iam, modern]
status: "developed"
---

# Proof of Possession

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** PoP, Sender-Constrained Token, Holder-of-Key

A credential model where presenting the token isn't enough: the holder must also prove possession of a bound private key, so a stolen token alone is worthless. The direct answer to the [[Bearer Token]] weakness.

**Context.** Bind the token to a key at issuance, then require a fresh signature with that key on each use, and have the server check both. Now theft of the token — from logs, [[XSS]], a sniffed connection, a copied cookie store — gains nothing without the key, which never leaves the holder. The cash-versus-cheque framing captures it: bearer is cash; sender-constrained is a cheque that clears only with your signature. The model appears under several names: *mTLS-bound* access tokens (bound to the client's TLS certificate), *DPoP* (Demonstrating Proof-of-Possession — an application-layer signature for OAuth tokens used by public clients), and, for browser session cookies specifically, [[DBSC]]. The same idea underlies [[FIDO2 and WebAuthn]] at login. The cost is complexity and key management, which is why [[Bearer Token]]s, despite the risk, still dominate.

## See also

- [[Bearer Token]]
- [[DBSC]]
- [[mTLS]]
- [[Token]]
- [[FIDO2 and WebAuthn]]

## Often confused with

- [[Bearer Token]] — possession of a bearer token *is* the authority; a proof-of-possession token is inert without the bound key.

## Further reading

- [RFC 9449: OAuth 2.0 Demonstrating Proof of Possession (DPoP)](https://datatracker.ietf.org/doc/html/rfc9449)
