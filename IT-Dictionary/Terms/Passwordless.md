---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam", "modern"]
status: "note"
---

# Passwordless

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

Authentication without a password, typically using biometrics + a cryptographic device.

**Context.** Eliminates the entire password-attack class — phishing, spraying, stuffing, reuse — rather than mitigating it. Mainstream implementations: Windows Hello for Business, FIDO2 keys, passkeys. The honest hard parts are account recovery (which becomes the weakest link) and the legacy systems that still demand a password somewhere.

## See also

- [[FIDO2 and WebAuthn]]
- [[Passkey]]
- [[MFA]]
