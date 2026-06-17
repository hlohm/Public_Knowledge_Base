---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["CRL", "\"OCSP\""]
tags: ["crypto"]
status: "note"
---

# CRL and OCSP

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** CRL, "OCSP"

Mechanisms to check if a certificate has been **revoked**. CRL = list, OCSP = online query. OCSP stapling reduces privacy/latency issues.

**Context.** Revocation is PKI's weak joint: browsers soft-fail when OCSP is unreachable, CRLs grow stale, and the practical fixes are short-lived certificates (the Let's Encrypt model — 90 days and shrinking) and OCSP stapling. For an internal PKI, decide the revocation story *before* issuing — bolting it on later is painful.

## See also

- [[Certificate Authority]]
- [[X.509]]
