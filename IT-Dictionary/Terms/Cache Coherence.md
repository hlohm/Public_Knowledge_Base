---
type: "term"
branch: "Hardware & Architecture"
tags: ["hardware", "fundamental"]
status: "developed"
---

# Cache Coherence

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]

The guarantee that, in a system where several caches sit over shared memory, every processor sees a consistent value for any given memory location.

**Context.** This is what makes shared memory usable: when one core writes a value another core has cached, a coherence protocol (MESI and its relatives) invalidates or updates the stale copy. The set of processors kept mutually coherent — the **coherence domain** — is effectively the hardware definition of one computer. Coherence traffic is also why shared-memory machines stop scaling past some socket/core count.

## See also

- [[Shared Memory]]
- [[NUMA]]
- [[Cache]]
- [[Multiprocessor]]

## Further reading

- [Cache coherence — Wikipedia](https://en.wikipedia.org/wiki/Cache_coherence)
