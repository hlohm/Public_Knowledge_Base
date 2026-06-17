---
type: "term"
branch: "Algorithms & Data Structures"
tags: [algo]
status: "developed"
---

# Quicksort

> **Branch:** [[09 - Algorithms & Data Structures|Algorithms & Data Structures]]

A divide-and-conquer sort that picks a pivot, partitions elements around it, and recurses — O(n log n) average, O(n²) worst case.

**Context.** Usually the fastest comparison sort in practice thanks to good cache behaviour and in-place operation, despite the quadratic worst case (mitigated by randomised or median-of-three pivots). Real standard libraries often use introsort (quicksort that falls back to heapsort) or Timsort.

## See also

- [[Merge Sort]]
- [[Sorting]]
- [[Divide and Conquer]]
- [[Pivot]]
- [[Time Complexity]]

## Further reading

- [Wikipedia: Quicksort](https://en.wikipedia.org/wiki/Quicksort)
