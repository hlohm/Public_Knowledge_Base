---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam", "fundamental"]
status: "developed"
---

# Bearer Token

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

A credential whose mere possession grants access — like cash. The server checks that the token is *valid*, not *who* presents it, so anyone holding a copy is indistinguishable from the legitimate owner. Session [[Cookie]]s, OAuth access [[Token]]s, and [[JWT]]s are all bearer tokens by default.

**Context — why this is the structural weak point.** Bearer semantics are the reason credential theft is the dominant web attack: steal the token and you *are* the user, with no further challenge, until it expires — and this sails straight past [[MFA]], because the second factor was already spent when the session was minted. A stolen live session cookie is worth more than a password. The exposure is broad: tokens leak through [[XSS]], logs, URLs, and referer headers, and — the case the `HttpOnly`/`Secure` flags can't touch — local malware reading the browser's cookie store ([[Session Hijacking]] by infostealer). The standard defences only *narrow the window*: short lifetimes with refresh tokens, never putting tokens in URLs or logs, and TLS everywhere. To remove the weakness rather than shrink it, the token has to stop being bearer — see [[Proof of Possession]], the sender-constrained model (mTLS-bound tokens, DPoP) whose cookie-specific form is [[DBSC]]. Worth memorising: a bearer token is cash; a sender-constrained token is a cheque that clears only with your signature.

## See also

- [[Token]]
- [[Proof of Possession]]
- [[DBSC]]
- [[Session]]
- [[OAuth 2.0]]
- [[mTLS]]

## Often confused with

- [[Proof of Possession]] — a bearer token is honoured on possession alone; a proof-of-possession (sender-constrained) token also requires proving you hold a bound key.

## Further reading

- [RFC 6750: OAuth 2.0 Bearer Token Usage](https://datatracker.ietf.org/doc/html/rfc6750)
