---
type: "term"
branch: "Hardware & Architecture"
aliases: ["SM"]
tags: ["hardware", "modern"]
status: "developed"
---

# Streaming Multiprocessor

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]
> **Also known as:** SM

The core building block of an NVIDIA GPU: a self-contained processor with its own warp schedulers, register file, execution units and L1/shared memory. A high-end GPU has many dozens of them.

**Context.** The reason a GPU is better understood as a cluster-on-a-die than as a single processor. Each SM runs many warps concurrently and interleaves them to hide latency; the whole GPU is a chip-level multiprocessor. AMD's analogue is the Compute Unit, Intel's the Xe-core.

## See also

- [[Warp]]
- [[SIMT]]
- [[GPU]]
- [[Latency Hiding]]

## Further reading

- [Graphics processing unit — Wikipedia](https://en.wikipedia.org/wiki/Graphics_processing_unit)
