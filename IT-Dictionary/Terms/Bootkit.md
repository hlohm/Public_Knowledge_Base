---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
tags: [threat]
status: "developed"
---

# Bootkit

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]

A [[Rootkit]] that infects the boot process so it executes *before* the operating system loads — and therefore before the OS's own defences (driver signing, anti-tampering) come online. Legacy bootkits infected the [[MBR]] or VBR on disk; modern ones live in the [[EFI System Partition]] boot loader or, deepest of all, in the [[UEFI]] firmware image on [[SPI Flash]].

**Context.** Position is everything: whoever runs first controls everything that loads after, and can lie to it. Disk-level bootkits survive an OS reinstall; firmware-level implants survive even disk replacement, so you can't "reinstall your way out." The mainstream answer is to verify the boot chain ([[Secure Boot]]) and *measure* it ([[Measured Boot]]) so tampering is detected even when verification is bypassed. ATT&CK technique **T1542.003**, under Pre-OS Boot (T1542).

## See also

- [[Rootkit]]
- [[Persistence]]
- [[Firmware]]
- [[UEFI]]
- [[Secure Boot]]
- [[Chain of Trust]]

## Often confused with

- [[Rootkit]] — a rootkit hides at OS or firmware level once running; a bootkit specifically subverts the *boot* sequence to seize control first.

## Further reading

- [MITRE ATT&CK: Bootkit (T1542.003)](https://attack.mitre.org/techniques/T1542/003/)
