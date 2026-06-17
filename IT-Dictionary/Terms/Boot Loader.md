---
type: "term"
branch: "Operating Systems"
aliases: ["Bootloader"]
tags: ["os"]
status: "developed"
---

# Boot Loader

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **Also known as:** Bootloader

The small program that bridges firmware and OS: loaded by UEFI/BIOS, it loads the kernel (plus initramfs/drivers) and hands over control. GRUB and the Windows Boot Manager are the ones you'll meet.

**Context.** The boot loader is a link in the [[Chain of Trust]] — [[Secure Boot]] exists largely to stop tampered loaders ([[Bootkit]]s), since whoever runs before the OS owns the OS. Operationally it's where dual-boot lives, where 'bootmgr is missing' comes from, and what you repair after an OS install steals the boot entry.

## See also

- [[UEFI]]
- [[Secure Boot]]
- [[Bootkit]]
- [[Kernel]]
- [[Chain of Trust]]

## Further reading

- [Wikipedia: Bootloader](https://en.wikipedia.org/wiki/Bootloader)
