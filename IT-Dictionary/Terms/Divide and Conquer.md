---
type: "term"
branch: "Algorithms & Data Structures"
tags: ["algo", "fundamental"]
status: "developed"
---

# Divide and Conquer

> **Branch:** [[09 - Algorithms & Data Structures|Algorithms & Data Structures]]

The strategy of splitting a problem into independent subproblems, solving them (usually recursively), and combining the results. [[Quicksort]], mergesort, and [[Binary Search]] are the canonical instances.

**Context.** The signature is the recurrence T(n) = aT(n/b) + f(n), solved by the Master Theorem — halving plus linear merge gives the ubiquitous O(n log n). Distinct from [[Dynamic Programming]] by independence: D&C subproblems don't overlap; when they do, you memoize and you're doing DP.

## See also

- [[Recursion]]
- [[Quicksort]]
- [[Binary Search]]
- [[Dynamic Programming]]
- [[Big-O Notation]]

## Often confused with

- [[Dynamic Programming]] — D&C: independent subproblems, solve each once naturally. DP: overlapping subproblems, store solutions to avoid recomputation.

## Further reading

- [Wikipedia: Divide-and-conquer algorithm](https://en.wikipedia.org/wiki/Divide-and-conquer_algorithm)
