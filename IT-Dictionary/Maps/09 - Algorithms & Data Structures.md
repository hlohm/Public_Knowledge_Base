---
type: "map"
tags: [map, algo]
---

# Algorithms & Data Structures

> The reusable shapes of computation and the structures that make them fast.

## Terms in this branch (26)

- [[Array]] — A contiguous block of memory holding elements of the same type, indexed in O(1) by position.
- [[Big-O Notation]] — A notation describing how an algorithm's resource use grows with input size n, ignoring constants and lower-order terms — the upper bound on growth rate.
- [[Binary Search]] — Finding an element in a sorted array in O(log n) by repeatedly halving the search interval.
- [[Binary Search Tree]] — A binary tree maintaining the invariant: left subtree keys < node key < right subtree keys — giving O(log n) search, insert, delete when balanced.
- [[Bloom Filter]] — A space-efficient probabilistic structure that tests set membership with possible false positives but no false negatives — 'definitely not present' or 'probably present'.
- [[Breadth-First Search]] — A graph traversal exploring all neighbours at the current depth before going deeper, using a queue.
- [[Depth-First Search]] — A graph traversal that explores as far as possible down one branch before backtracking, using a stack or recursion.
- [[Dijkstra's Algorithm]] — Finds the shortest path from a source to all vertices in a graph with non-negative edge weights, using a priority queue to always expand the nearest unvisited vertex.
- [[Divide and Conquer]] — The strategy of splitting a problem into independent subproblems, solving them (usually recursively), and combining the results.
- [[Dynamic Programming]] — Solving a problem by breaking it into overlapping subproblems and storing their solutions (memoisation or tabulation) to avoid recomputation.
- [[Graph]] — A set of vertices connected by edges (directed or undirected, weighted or not) — the general model for networks and relationships.
- [[Greedy Algorithm]] — An algorithm that makes the locally optimal choice at each step, hoping to reach a global optimum.
- [[Hash Table]] — A structure mapping keys to values with average O(1) lookup, insert, and delete, by hashing the key to a bucket index.
- [[Heap]] — A tree-based structure maintaining the heap property (parent ≤ children for a min-heap), giving O(1) access to the min/max and O(log n) insert/extract.
- [[Linked List]] — A sequence of nodes where each holds a value and a pointer to the next (and maybe previous), so elements live scattered in memory.
- [[Memoization]] — Caching a function's results keyed by its arguments, so repeated calls with the same inputs return instantly instead of recomputing.
- [[Priority Queue]] — A collection that always yields its highest-priority element first, regardless of insertion order.
- [[Queue]] — A FIFO (first-in, first-out) collection: enqueue at the back, dequeue from the front.
- [[Quicksort]] — A divide-and-conquer sort that picks a pivot, partitions elements around it, and recurses — O(n log n) average, O(n²) worst case.
- [[Sorting]] — Arranging elements by a comparison key.
- [[Space Complexity]] — How an algorithm's memory use scales with input size, in Big-O terms.
- [[Stack]] — A LIFO (last-in, first-out) collection: push to add, pop to remove from the same end.
- [[Time Complexity]] — How an algorithm's running time scales with input size, expressed in Big-O — O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ)…
- [[Topological Sort]] — An ordering of a directed acyclic graph's nodes such that every edge points forward — dependencies before dependents.
- [[Tree]] — A hierarchical structure of nodes with a single root, where each node has children but exactly one parent — no cycles.
- [[Trie]] — A tree where each path from the root spells a string, sharing common prefixes — lookup is O(length of key), independent of how many keys are stored.

---
← Back to [[_Home]]
