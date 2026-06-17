---
type: "term"
branch: "Hardware & Architecture"
tags: ["hardware"]
status: "note"
---

# Latency Hiding

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]

Keeping execution units busy during long-latency operations (chiefly memory access) by having other independent work ready to run, instead of by making the slow operation itself faster.

**Context.** The deepest divide between CPU and GPU design. A CPU hides latency for *one* thread with caches, prefetching and out-of-order execution; a GPU hides it by oversubscribing each core with many warps and switching instantly to one that's ready. Same goal, opposite strategy — latency-cleverness versus parallel slack.

## See also

- [[Out-of-Order Execution]]
- [[SIMT]]
- [[Warp]]
- [[Throughput]]
- [[Cache]]
