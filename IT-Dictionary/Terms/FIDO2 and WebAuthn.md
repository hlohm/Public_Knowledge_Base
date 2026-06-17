---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["FIDO2", "\"WebAuthn\""]
tags: ["iam", "modern"]
status: "developed"
---

# FIDO2 and WebAuthn

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** FIDO2, "WebAuthn"

Modern open standards for passwordless and phishing-resistant authentication. FIDO2 is the spec family; WebAuthn is the browser API half of it.

**Context.** Phishing resistance comes from origin binding: the credential is cryptographically tied to the real domain, so a look-alike site receives nothing usable — a property no OTP code has. The private key never leaves the authenticator (security key, TPM, phone). For admin accounts, FIDO2 is the single strongest authentication upgrade available.

## See also

- [[Passkey]]
- [[Passwordless]]

## Further reading

- [WebAuthn (W3C)](https://www.w3.org/TR/webauthn-2/)
- [FIDO Alliance: FIDO2](https://fidoalliance.org/fido2/)
