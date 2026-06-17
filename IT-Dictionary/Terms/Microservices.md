---
type: "term"
branch: "Software Engineering"
tags: [se, modern]
status: "developed"
---

# Microservices

> **Branch:** [[08 - Software Engineering|Software Engineering]]

An architectural style structuring an application as a suite of small, independently deployable services communicating over the network, each owning its data.

**Context.** Trades in-process simplicity for organisational scalability — independent teams, deploys, and scaling. But it converts every method call into a distributed-systems problem (latency, partial failure, eventual consistency, observability). 'You must be this tall to ride.' Many teams over-adopted and walked back to a 'modular monolith'.

## See also

- [[Monolith]]
- [[Service Mesh]]
- [[Distributed System]]
- [[API]]
- [[Bounded Context]]

## Often confused with

- [[Monolith]] — Microservices: many independently deployed services (operational complexity). Monolith: one deployable unit (simpler ops, harder to scale teams).

## Further reading

- [Wikipedia: Microservices](https://en.wikipedia.org/wiki/Microservices)
