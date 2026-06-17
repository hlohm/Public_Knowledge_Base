---
type: "term"
branch: "Algorithms & Data Structures"
aliases: ["Sorting Algorithm"]
tags: ["algo", "fundamental"]
status: "developed"
---

# Sorting

> **Branch:** [[09 - Algorithms & Data Structures|Algorithms & Data Structures]]
> **Also known as:** Sorting Algorithm

Arranging elements by a comparison key. Comparison sorts bottom out at O(n log n) — provably — with [[Quicksort]], mergesort, and heapsort as the classic trio; counting/radix sorts beat the bound by not comparing.

**Context.** The properties that matter in practice: **stability** (equal elements keep their order — essential for multi-key sorts), in-place vs extra memory, and worst-case behavior. Real standard libraries ship hybrids (Timsort in Python/Java, introsort in C++) precisely because no single classic wins everywhere. 'Just sort it first' simplifies a remarkable number of problems.

## See also

- [[Quicksort]]
- [[Big-O Notation]]
- [[Binary Search]]
- [[Divide and Conquer]]

## Further reading

- [Wikipedia: Sorting algorithm](https://en.wikipedia.org/wiki/Sorting_algorithm)
