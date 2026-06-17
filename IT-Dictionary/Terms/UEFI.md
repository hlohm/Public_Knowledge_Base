---
type: "term"
branch: "Hardware & Architecture"
aliases: ["Unified Extensible Firmware Interface"]
tags: [hardware]
status: "developed"
---

# UEFI

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]
> **Also known as:** Unified Extensible Firmware Interface

The modern replacement for legacy BIOS: the [[Firmware]] interface that initialises hardware and hands control to an operating-system [[Boot Loader]]. Unlike BIOS it understands partitions and file systems, loading signed `.efi` boot applications from the [[EFI System Partition]].

**Context.** UEFI is a small operating environment in its own right — drivers, a shell, a network stack — which makes it powerful and a rich attack surface. Its security model rests on [[Secure Boot]] (signature verification of each stage) anchored in a hardware root of trust ([[TPM]], [[Boot Guard]]). Compromise the firmware itself and you sit beneath the OS permanently — see [[Bootkit]].

## See also

- [[Firmware]]
- [[BIOS]]
- [[Secure Boot]]
- [[EFI System Partition]]
- [[Boot Loader]]

## Further reading

- [Wikipedia: UEFI](https://en.wikipedia.org/wiki/UEFI)
