---
type: "term"
branch: "Networking"
aliases: ["Remote Direct Memory Access"]
tags: ["net"]
status: "developed"
---

# RDMA

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Remote Direct Memory Access

Network technology that lets one machine read or write another's memory directly, bypassing both CPUs and the OS networking stack.

**Context.** The fabric-level glue (InfiniBand, RoCE) that makes cross-node message passing fast enough for tightly-coupled workloads like distributed training. Extends shared-memory-style access across the machine boundary without providing true coherence.

## See also

- [[Message Passing]]
- [[InfiniBand]]
- [[Collective Communication]]
- [[NUMA]]

## Further reading

- [Remote direct memory access — Wikipedia](https://en.wikipedia.org/wiki/Remote_direct_memory_access)
