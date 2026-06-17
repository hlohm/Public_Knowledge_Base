---
type: "term"
branch: "Computing Foundations"
de: "Prüfsumme"
tags: [foundations]
status: "developed"
---

# Checksum

> **Branch:** [[01 - Computing Foundations|Computing Foundations]]
> **German:** Prüfsumme

A small value computed from a block of data so that accidental corruption can be detected by recomputing and comparing.

**Context.** Checksums (CRC32, Adler-32) catch *random* errors cheaply but are not security — an attacker can forge a matching one. For tamper detection you need a cryptographic hash or MAC.

## See also

- [[Parity Bit]]
- [[Hash Function]]
- [[CRC]]

## Often confused with

- [[Hash Function]] — A checksum detects accidents; a cryptographic hash also resists deliberate forgery.

## Further reading

- [Wikipedia: Checksum](https://en.wikipedia.org/wiki/Checksum)
