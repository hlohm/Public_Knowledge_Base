---
type: "term"
branch: "Software Engineering"
aliases: ["EDA"]
tags: ["se", "modern"]
status: "developed"
---

# Event-driven Architecture

> **Branch:** [[08 - Software Engineering|Software Engineering]]
> **Also known as:** EDA

Systems built around producers emitting **events** (facts: 'order placed') that interested consumers react to asynchronously, usually via a broker — instead of services calling each other directly.

**Context.** The win is decoupling: producers don't know consumers exist, so adding a new reaction means adding a subscriber, not editing the producer. The bill arrives as eventual consistency, duplicate delivery (consumers must be [[Idempotent]]), ordering questions, and debugging-by-archaeology across async hops — hence tracing and the event-sourcing/outbox pattern family.

## See also

- [[Message Queue]]
- [[Microservices]]
- [[Eventual Consistency]]
- [[Idempotent]]
- [[Coupling]]

## Further reading

- [Wikipedia: Event-driven architecture](https://en.wikipedia.org/wiki/Event-driven_architecture)
