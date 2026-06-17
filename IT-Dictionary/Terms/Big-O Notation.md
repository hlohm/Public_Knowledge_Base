---
type: "term"
branch: "Algorithms & Data Structures"
aliases: ["Asymptotic Notation"]
tags: [algo, fundamental]
status: "developed"
---

# Big-O Notation

> **Branch:** [[09 - Algorithms & Data Structures|Algorithms & Data Structures]]
> **Also known as:** Asymptotic Notation

A notation describing how an algorithm's resource use grows with input size *n*, ignoring constants and lower-order terms — the upper bound on growth rate.

**Context.** The lingua franca for comparing algorithms, but the constants it discards matter in practice: an O(n) algorithm with a huge constant can lose to O(n log n) at real sizes, and cache effects routinely upend the theory. Use it to spot scaling cliffs (the O(n²) loop), not to micro-optimise.

## See also

- [[Time Complexity]]
- [[Space Complexity]]
- [[Amortized Analysis]]
- [[Algorithm]]

## Further reading

- [Wikipedia: Big O notation](https://en.wikipedia.org/wiki/Big_O_notation)
