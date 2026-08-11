---
type: "term"
branch: "Operating Systems"
aliases: ["Runtime PM"]
tags: [os]
status: "developed"
---

# Runtime Power Management

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **Also known as:** Runtime PM

The kernel framework that suspends *individual devices* to low-power states while the system keeps running, waking them transparently on access — as opposed to system-wide suspend. The headline case is a laptop's discrete GPU dropping to D3cold (power gated off) whenever nothing uses it.

**Context.** On Linux the knobs live in sysfs (`/sys/.../power/control`, `auto` vs `on`), and a single device stuck active can cost several watts of battery. The dGPU is the classic patient: the driver stack (nouveau/nvidia + PCIe port PM) must all agree before the card powers down, and *verifying* it's down means reading its runtime status without touching the device — because reading the wrong file wakes it up, the observer effect in miniature. Bringing a gated device back cleanly can require unbinding consumers or a PCI rescan, which is why "GPU on/off" toggle scripts exist.

## See also

- [[Driver]]
- [[Kernel]]
- [[GPU]]

## Further reading

- [Linux kernel documentation: Runtime PM](https://www.kernel.org/doc/html/latest/power/runtime_pm.html)
