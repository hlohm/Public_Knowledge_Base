---
type: "term"
branch: "Theory of Computation"
aliases: ["Regex", "Regexp"]
tags: [theory, fundamental]
status: "developed"
---

# Regular Expression

> **Branch:** [[10 - Theory of Computation|Theory of Computation]]
> **Also known as:** Regex, Regexp

A pattern language describing sets of strings, formally equivalent to a finite automaton — and in practice the everyday tool for text matching.

**Context.** The theory (regular languages = FSM-recognisable) explains the famous limits: classic regex can't match nested structures, so 'don't parse HTML with regex'. Real-world engines add backreferences (beyond regular) at the cost of catastrophic backtracking — a genuine ReDoS attack vector.

## See also

- [[Finite State Machine]]
- [[Context-free Grammar]]
- [[Chomsky Hierarchy]]
- [[Lexer]]
- [[ReDoS]]

## Further reading

- [Wikipedia: Regular expression](https://en.wikipedia.org/wiki/Regular_expression)
