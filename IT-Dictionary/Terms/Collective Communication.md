---
type: "term"
branch: "Networking"
aliases: ["Collective Operation"]
tags: ["net", "ai"]
status: "developed"
---

# Collective Communication

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Collective Operation

Communication patterns that involve a whole group of processes at once — broadcast, scatter, gather, reduce, all-reduce — as opposed to point-to-point messages.

**Context.** The backbone of distributed training: after each step, every node's gradients are combined and redistributed via **all-reduce** so all replicas stay in sync. Tuning these collectives to the interconnect topology is much of what makes large-scale training tractable.

## See also

- [[Message Passing]]
- [[RDMA]]
- [[MPI]]
- [[Distributed Training]]

## Further reading

- [Collective operation — Wikipedia](https://en.wikipedia.org/wiki/Collective_operation)
