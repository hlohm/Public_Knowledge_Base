---
type: "term"
branch: "Security"
domain: "Cryptography"
tags: ["security", "crypto", "pki"]
status: "developed"
---

# Code Signing

> **Domain:** [[03 - Cryptography|Cryptography]]

Digitally signing executables, drivers, scripts, or packages so the OS or user can verify publisher identity and integrity before running them.

**Context.** Code signing is the trust anchor for software distribution — SmartScreen, driver loading, macOS Gatekeeper, package repositories all rest on it. That makes signing keys a prime target: stolen or abused certificates are a recurring element of supply-chain attacks ([[BYOVD]] abuses *legitimately* signed vulnerable drivers). Signing proves *who* shipped the code and that it's unmodified — not that it's safe.

## See also

- [[Digital Signature]]
- [[Supply Chain Attack]]
- [[BYOVD]]
- [[Chain of Trust]]
- [[X.509]]

## Further reading

- [Wikipedia: Code signing](https://en.wikipedia.org/wiki/Code_signing)
