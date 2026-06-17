---
type: "term"
branch: "Programming Languages"
tags: [pl, modern]
status: "developed"
---

# Memory Safety

> **Branch:** [[07 - Programming Languages|Programming Languages]]

The property that a program cannot access memory incorrectly — no buffer overflows, use-after-free, null dereferences, or data races on memory.

**Context.** Around 70% of serious security vulnerabilities in C/C++ codebases (per Microsoft and Google data) are memory-safety bugs — the reason for the industry-wide push toward Rust and for CISA's memory-safety roadmap. Achieved via GC, or via Rust's borrow checker at compile time with no runtime cost.

## See also

- [[Pointer]]
- [[Buffer Overflow]]
- [[Ownership]]
- [[Borrowing]]
- [[Use-after-free]]
- [[Garbage Collection]]

## Further reading

- [Wikipedia: Memory safety](https://en.wikipedia.org/wiki/Memory_safety)
- [CISA — The Urgent Need for Memory Safety](https://www.cisa.gov/news-events/news/urgent-need-memory-safety-software-products)
