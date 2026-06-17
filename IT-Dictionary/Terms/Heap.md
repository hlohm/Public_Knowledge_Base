---
type: "term"
branch: "Algorithms & Data Structures"
tags: [algo, fundamental]
status: "developed"
---

# Heap

> **Branch:** [[09 - Algorithms & Data Structures|Algorithms & Data Structures]]

A tree-based structure maintaining the heap property (parent ≤ children for a min-heap), giving O(1) access to the min/max and O(log n) insert/extract.

**Context.** The standard backing for a priority queue, and the heart of heapsort and Dijkstra's algorithm. Usually stored compactly in an array (no pointers — parent/child by index arithmetic). Distinct from 'the heap', the region of dynamically-allocated memory.

## See also

- [[Priority Queue]]
- [[Heapsort]]
- [[Tree]]
- [[Dijkstra's Algorithm]]

## Further reading

- [Wikipedia: Heap (data structure)](https://en.wikipedia.org/wiki/Heap_(data_structure))
