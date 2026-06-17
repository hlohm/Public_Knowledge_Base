---
type: "term"
branch: "Algorithms & Data Structures"
aliases: ["Heap (Data Structure)", "Binary Heap"]
tags: ["algo", "fundamental"]
status: "developed"
---

# Priority Queue

> **Branch:** [[09 - Algorithms & Data Structures|Algorithms & Data Structures]]
> **Also known as:** Heap (Data Structure), Binary Heap

A collection that always yields its highest-priority element first, regardless of insertion order. Almost always implemented as a **binary heap**: O(log n) insert and extract-min, O(1) peek.

**Context.** Priority queues are infrastructure: [[Dijkstra's Algorithm]] and A* pull the nearest frontier node from one, OS schedulers and timer wheels are conceptually one, heapsort is one used in anger. Naming collision to keep straight: the heap *data structure* shares nothing but a name with the heap *memory region*.

## See also

- [[Heap]]
- [[Queue]]
- [[Dijkstra's Algorithm]]
- [[Tree]]
- [[Scheduler]]

## Further reading

- [Wikipedia: Priority queue](https://en.wikipedia.org/wiki/Priority_queue)
