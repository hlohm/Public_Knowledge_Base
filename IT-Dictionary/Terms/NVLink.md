---
type: "term"
branch: "Hardware & Architecture"
tags: ["hardware", "modern"]
status: "developed"
---

# NVLink

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]

NVIDIA's high-bandwidth interconnect that lets GPUs read and write each other's memory directly — far faster than PCIe — and, at rack scale, lets many GPUs share a single memory fabric.

**Context.** The technology actively pushing the "one computer" boundary outward: turning a node, or even a multi-chassis rack, into something a programmer can treat as one large GPU. A concrete example of the shared-memory domain migrating from the box up to the rack.

## See also

- [[RDMA]]
- [[Streaming Multiprocessor]]
- [[Shared Memory]]
- [[Cache Coherence]]

## Further reading

- [NVLink — Wikipedia](https://en.wikipedia.org/wiki/NVLink)
