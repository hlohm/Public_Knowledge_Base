---
type: "term"
branch: "Computing Foundations"
tags: [foundations, fundamental]
status: "developed"
---

# Idempotent

> **Branch:** [[01 - Computing Foundations|Computing Foundations]]

An operation that has the same effect whether applied once or many times. Setting x = 5 is idempotent; incrementing x is not.

**Context.** Crucial for reliability: if a network request might be retried after a timeout, making it idempotent (e.g. via an idempotency key) means a duplicate can't double-charge or double-create.

## See also

- [[Idempotency Key]]
- [[PUT]]
- [[Safe (HTTP)]]

## Further reading

- [Wikipedia: Idempotence](https://en.wikipedia.org/wiki/Idempotence)
