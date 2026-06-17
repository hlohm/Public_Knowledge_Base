---
type: "term"
branch: "Algorithms & Data Structures"
de: "Feld"
tags: [algo, fundamental]
status: "developed"
---

# Array

> **Branch:** [[09 - Algorithms & Data Structures|Algorithms & Data Structures]]
> **German:** Feld

A contiguous block of memory holding elements of the same type, indexed in O(1) by position.

**Context.** The most cache-friendly structure there is — contiguity means the CPU prefetcher loves it, often beating 'better' Big-O structures in practice. The cost: insertion/deletion in the middle is O(n), and fixed-size arrays need copying to grow (the dynamic-array doubling trick).

## See also

- [[Dynamic Array]]
- [[Linked List]]
- [[Cache]]
- [[Locality of Reference]]
- [[Big-O Notation]]

## Often confused with

- [[Linked List]] — Array: contiguous, O(1) random access, costly insert. Linked list: scattered nodes, O(1) insert at a known node, O(n) access, cache-hostile.

## Further reading

- [Wikipedia: Array (data structure)](https://en.wikipedia.org/wiki/Array_(data_structure))
