---
type: "term"
branch: "Data & Databases"
de: "Normalisierung"
tags: [data]
status: "developed"
---

# Normalization

> **Branch:** [[06 - Data & Databases|Data & Databases]]
> **German:** Normalisierung

Structuring a relational schema to eliminate redundancy by decomposing tables so each fact is stored exactly once, governed by a series of **normal forms** (1NF, 2NF, 3NF, BCNF…).

**Context.** Normalise for write integrity (no update anomalies); *denormalise* deliberately for read performance once you've measured a problem. 3NF is the usual practical target. 'Normalise till it hurts, denormalise till it works.'

## See also

- [[RDBMS]]
- [[Join]]
- [[Denormalization]]
- [[Foreign Key]]
- [[Primary Key]]

## Often confused with

- [[Denormalization]] — Normalization removes redundancy for integrity; denormalization reintroduces it on purpose for read speed.

## Further reading

- [Wikipedia: Database normalization](https://en.wikipedia.org/wiki/Database_normalization)
