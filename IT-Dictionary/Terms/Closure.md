---
type: "term"
branch: "Programming Languages"
tags: [pl, fundamental]
status: "developed"
---

# Closure

> **Branch:** [[07 - Programming Languages|Programming Languages]]

A function bundled together with the variables it captured from its surrounding scope — it 'closes over' that environment and can use those variables later, even after the enclosing function has returned.

**Context.** The mechanism behind callbacks, decorators, and most functional patterns. The capture semantics — by value or by reference — are a frequent source of bugs (the classic 'loop variable captured by reference' surprise). Closures are how functions become genuinely first-class.

## See also

- [[First-class Function]]
- [[Scope]]
- [[Lambda]]
- [[Higher-order Function]]
- [[Lexical Scope]]

## Further reading

- [Wikipedia: Closure (computer programming)](https://en.wikipedia.org/wiki/Closure_(computer_programming))
