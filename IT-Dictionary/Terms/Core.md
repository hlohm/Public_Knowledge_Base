---
type: "term"
branch: "Hardware & Architecture"
aliases: ["CPU Core", "Multi-core"]
tags: ["hw", "fundamental"]
status: "developed"
---

# Core

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]
> **Also known as:** CPU Core, Multi-core

One independent processing unit on a CPU die — its own ALUs, registers, L1/L2 cache, instruction stream. A modern 'CPU' is a package of many cores sharing L3 and a memory controller.

**Context.** Multi-core is what happened when clock speeds hit the power wall (~2005): the free single-thread lunch ended and parallelism became software's problem. Wrinkles worth knowing: SMT/hyperthreading makes one core appear as two (sharing execution resources — also the substrate of several side-channel attacks), and big.LITTLE/P+E designs mix fast and efficient cores, making 'core count' a fuzzier spec than it looks.

## See also

- [[CPU]]
- [[Thread]]
- [[Parallelism]]
- [[Cache Coherence]]
- [[Moore's Law]]

## Further reading

- [Wikipedia: Multi-core processor](https://en.wikipedia.org/wiki/Multi-core_processor)
