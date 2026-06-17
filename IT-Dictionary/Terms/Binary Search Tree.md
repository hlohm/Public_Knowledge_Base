---
type: "term"
branch: "Algorithms & Data Structures"
aliases: ["BST"]
tags: [algo, fundamental]
status: "developed"
---

# Binary Search Tree

> **Branch:** [[09 - Algorithms & Data Structures|Algorithms & Data Structures]]
> **Also known as:** BST

A binary tree maintaining the invariant: left subtree keys < node key < right subtree keys — giving O(log n) search, insert, delete when balanced.

**Context.** Degenerates to a linked list (O(n)) if you insert sorted data without balancing — which is why self-balancing variants (red-black, AVL) exist and back most ordered-map implementations. The in-order traversal yields sorted output for free.

## See also

- [[Tree]]
- [[Red-Black Tree]]
- [[B-tree]]
- [[Binary Search]]
- [[Self-balancing Tree]]

## Further reading

- [Wikipedia: Binary search tree](https://en.wikipedia.org/wiki/Binary_search_tree)
