---
type: "term"
branch: "Programming Languages"
de: "Rekursion"
tags: [pl, fundamental]
status: "developed"
---

# Recursion

> **Branch:** [[07 - Programming Languages|Programming Languages]]
> **German:** Rekursion

A function that solves a problem by calling itself on smaller subproblems, with a base case to stop. The natural expression of self-similar (recursive) structures like trees.

**Context.** Elegant for divide-and-conquer and tree traversal, but each call consumes stack — deep recursion overflows the stack unless the language does **tail-call optimisation**. Often equivalent to iteration, but some problems (tree walks, parsers) are far clearer recursively.

## See also

- [[Stack]]
- [[Tail Call]]
- [[Base Case]]
- [[Divide and Conquer]]
- [[Stack Overflow]]

## Further reading

- [Wikipedia: Recursion (computer science)](https://en.wikipedia.org/wiki/Recursion_(computer_science))
