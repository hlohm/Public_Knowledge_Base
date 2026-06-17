---
type: "term"
branch: "Computing Foundations"
tags: ["foundations"]
status: "developed"
---

# Message Passing

> **Branch:** [[01 - Computing Foundations|Computing Foundations]]

A parallelism model in which processes with separate, private memories cooperate by explicitly sending and receiving messages.

**Context.** The model that takes over at the machine boundary: once processors no longer share an address space, they must ship bytes over a link. This is the world of MPI, RPC and distributed training. The line between shared memory and message passing is the most principled answer to "where does one computer end?" — inside it you reason in threads and locks, across it in sends and receives. **Often confused with:** [[Shared Memory]] — see the Shared Memory note for the contrast.

## See also

- [[Shared Memory]]
- [[RDMA]]
- [[MPI]]
- [[Distributed System]]
- [[Collective Communication]]

## Further reading

- [Message passing — Wikipedia](https://en.wikipedia.org/wiki/Message_passing)
