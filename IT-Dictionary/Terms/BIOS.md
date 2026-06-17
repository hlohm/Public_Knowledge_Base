---
type: "term"
branch: "Hardware & Architecture"
aliases: ["Basic Input/Output System", "Legacy BIOS"]
tags: ["hw", "deprecated"]
status: "developed"
---

# BIOS

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]
> **Also known as:** Basic Input/Output System, Legacy BIOS

**B**asic **I**nput/**O**utput **S**ystem. The original PC firmware: initialize hardware (POST), find a boot device, load the first sector (MBR), go. Replaced by [[UEFI]], though the name stuck to the setup screen.

**Context.** Legacy BIOS limits explain old machines' quirks: MBR's 2 TiB disk ceiling and four primary partitions, 16-bit real-mode beginnings, no signature checking of what it boots (hence classic MBR [[Bootkit]]s). 'BIOS settings' in modern usage almost always means the UEFI setup UI — CSM/legacy-boot mode is the compatibility shim on its way out.

## See also

- [[UEFI]]
- [[Firmware]]
- [[Boot Loader]]
- [[Secure Boot]]

## Further reading

- [Wikipedia: BIOS](https://en.wikipedia.org/wiki/BIOS)
