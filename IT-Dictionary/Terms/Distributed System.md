---
type: "term"
branch: "Cloud & Infrastructure"
aliases: ["Distributed Computing"]
tags: ["cloud", "fundamental"]
status: "developed"
---

# Distributed System

> **Branch:** [[11 - Cloud & Infrastructure|Cloud & Infrastructure]]
> **Also known as:** Distributed Computing

Multiple machines cooperating over a network to act as one system. The defining properties are the unpleasant ones: partial failure, no shared clock, and messages that can be lost, delayed, or duplicated.

**Context.** Single-machine intuitions silently break here — that's the content of the 'fallacies of distributed computing' (the network is reliable, latency is zero, …) and the reason [[CAP Theorem]], consensus protocols, idempotent retries, and timeouts exist. Lamport's definition is the honest one: a system where your work can be ruined by the failure of a computer you've never heard of.

## See also

- [[CAP Theorem]]
- [[Eventual Consistency]]
- [[Replication]]
- [[Microservices]]
- [[Latency]]

## Further reading

- [Wikipedia: Distributed computing](https://en.wikipedia.org/wiki/Distributed_computing)
