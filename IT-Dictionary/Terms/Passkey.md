---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam", "modern"]
status: "note"
---

# Passkey

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

Consumer-friendly name for a FIDO2 credential, often synced via cloud (iCloud Keychain, Google Password Manager).

**Context.** Syncing is the consumer trade-off: credentials escape the single device (recoverable when your phone dies) but inherit the security of the cloud account and its recovery flow. Enterprise policy can require device-bound credentials instead. Either way, the phishing resistance of FIDO2 is intact — the leap from passwords is enormous regardless of flavor.

## See also

- [[FIDO2 and WebAuthn]]
- [[Passwordless]]
