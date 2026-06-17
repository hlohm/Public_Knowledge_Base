---
type: "term"
branch: "Operating Systems"
aliases: ["Device Driver"]
de: "Treiber"
tags: ["os", "fundamental"]
status: "developed"
---

# Driver

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **Also known as:** Device Driver
> **German:** Treiber

The kernel-side translator between the OS's generic device interfaces and one piece of hardware's actual registers, queues, and quirks.

**Context.** Drivers are most of a modern kernel by line count and most of its crashes by cause — third-party code running with full kernel privilege. That's why Windows requires signed drivers, why [[BYOVD]] (bring your own vulnerable driver) is a thing, and why the printer subsystem is a security story of its own. Helpdesk reality: 'update/roll back the driver' resolves an absurd share of hardware tickets.

## See also

- [[Kernel]]
- [[Kernel Space]]
- [[BYOVD]]
- [[Firmware]]
- [[Interrupt]]

## Further reading

- [Wikipedia: Device driver](https://en.wikipedia.org/wiki/Device_driver)
