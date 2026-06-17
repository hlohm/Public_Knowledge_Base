---
type: "term"
branch: "Algorithms & Data Structures"
tags: [algo, fundamental]
status: "developed"
---

# Linked List

> **Branch:** [[09 - Algorithms & Data Structures|Algorithms & Data Structures]]

A sequence of nodes where each holds a value and a pointer to the next (and maybe previous), so elements live scattered in memory.

**Context.** O(1) insertion/deletion at a known position, but O(n) access and terrible cache behaviour (pointer-chasing). The textbook favourite that's often a poor real-world choice precisely because of memory locality — arrays usually win unless you need cheap splicing.

## See also

- [[Array]]
- [[Pointer]]
- [[Stack]]
- [[Queue]]
- [[Locality of Reference]]

## Further reading

- [Wikipedia: Linked list](https://en.wikipedia.org/wiki/Linked_list)
