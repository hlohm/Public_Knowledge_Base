---
type: "term"
branch: "Programming Languages"
tags: [pl]
status: "developed"
---

# Pure Function

> **Branch:** [[07 - Programming Languages|Programming Languages]]

A function whose output depends only on its inputs and which has no side effects — same input always yields same output, and nothing observable changes outside it.

**Context.** The cornerstone of functional programming and the reason pure code is trivially testable, cacheable (memoisable), and parallelisable. Real programs need side effects somewhere; the discipline is pushing them to the edges and keeping the core pure.

## See also

- [[Side Effect]]
- [[Referential Transparency]]
- [[Functional Programming]]
- [[Memoization]]
- [[Idempotent]]

## Often confused with

- [[Idempotent]] — Pure: no side effects at all. Idempotent: a side effect that's safe to repeat (calling twice == calling once).

## Further reading

- [Wikipedia: Pure function](https://en.wikipedia.org/wiki/Pure_function)
