---
type: "term"
branch: "Algorithms & Data Structures"
tags: [algo]
status: "developed"
---

# Memoization

> **Branch:** [[09 - Algorithms & Data Structures|Algorithms & Data Structures]]

Caching a function's results keyed by its arguments, so repeated calls with the same inputs return instantly instead of recomputing.

**Context.** The top-down face of dynamic programming, and a clean optimisation for any expensive *pure* function. Trades memory for time. Only safe when the function is pure (same inputs → same output, no side effects) — otherwise you cache stale or wrong results.

## See also

- [[Dynamic Programming]]
- [[Pure Function]]
- [[Cache]]
- [[Recursion]]

## Further reading

- [Wikipedia: Memoization](https://en.wikipedia.org/wiki/Memoization)
