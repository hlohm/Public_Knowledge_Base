---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
tags: ["threat"]
status: "note"
---

# Rootkit

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]

Malware that hides itself and other malware at deep OS or firmware level.

**Context.** Defined by stealth: it hooks the OS (or lives below it) to hide processes, files, and network connections from the tools you'd use to find it. The deeper it sits the worse it gets — bootkits and UEFI/firmware implants survive OS reinstalls, which is the whole point of Secure Boot and measured boot. If you suspect kernel/firmware-level compromise, trust nothing the live OS reports.

## See also

- [[Persistence]]
- [[Malware]]
- [[Secure Boot]]
- [[Remote Attestation]]
