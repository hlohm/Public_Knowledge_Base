---
type: "term"
branch: "Theory of Computation"
aliases: ["PDA"]
tags: ["theory"]
status: "developed"
---

# Pushdown Automaton

> **Branch:** [[10 - Theory of Computation|Theory of Computation]]
> **Also known as:** PDA

A finite state machine plus an unbounded stack — exactly the power needed to recognize [[Context-free Grammar|context-free languages]]. The stack is what lets it count and match nesting.

**Context.** The PDA is the formal reason your editor can match brackets but a [[Regular Expression]] can't: balanced parentheses require remembering unbounded depth, which finite states lack and one stack provides. It's the middle rung of the [[Chomsky Hierarchy]] — and the abstract shape of every recursive-descent [[Parser]].

## See also

- [[Finite State Machine]]
- [[Context-free Grammar]]
- [[Chomsky Hierarchy]]
- [[Turing Machine]]
- [[Parser]]

## Further reading

- [Wikipedia: Pushdown automaton](https://en.wikipedia.org/wiki/Pushdown_automaton)
