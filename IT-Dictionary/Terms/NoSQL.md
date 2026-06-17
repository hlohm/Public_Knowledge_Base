---
type: "term"
branch: "Data & Databases"
aliases: ["Not Only SQL"]
tags: [data]
status: "developed"
---

# NoSQL

> **Branch:** [[06 - Data & Databases|Data & Databases]]
> **Also known as:** Not Only SQL

An umbrella for non-relational stores — key-value, document, column-family, and graph — that trade the relational model and often strict consistency for scale, flexible schemas, or specific access patterns.

**Context.** Born from web-scale needs the relational model served awkwardly. The name is a misnomer: it's a grab-bag of very different tools (Redis, MongoDB, Cassandra, Neo4j) whose only shared trait is 'not a classic RDBMS'. Pick by access pattern, not by hype.

## See also

- [[Database]]
- [[CAP Theorem]]
- [[Eventual Consistency]]
- [[Key-Value Store]]
- [[Document Database]]

## Often confused with

- [[RDBMS]] — Not a replacement but a different toolset; most systems use both, relational for the source of truth and NoSQL for caches, search, or specific workloads.

## Further reading

- [Wikipedia: NoSQL](https://en.wikipedia.org/wiki/NoSQL)
