---
type: "term"
branch: "Hardware & Architecture"
tags: ["hardware", "modern"]
status: "note"
---

# Warp

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]

The fixed-size group of GPU threads (32 on NVIDIA hardware) that execute one instruction in lockstep under the SIMT model. AMD's equivalent is the *wavefront*.

**Context.** The real unit of GPU scheduling — the hardware issues and tracks work per warp, not per thread. Hiding memory latency means keeping many warps resident so the scheduler always has a ready one to switch to. When threads inside a warp take different branches, the warp serialises those paths with the off-path lanes masked, wasting throughput (branch divergence).

## See also

- [[SIMT]]
- [[Streaming Multiprocessor]]
- [[Branch Divergence]]
- [[Latency Hiding]]
