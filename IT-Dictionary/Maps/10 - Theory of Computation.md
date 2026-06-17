---
type: "map"
tags: [map, theory]
---

# Theory of Computation

> What is computable, how hard problems are, and the formal machines behind it all.

## Terms in this branch (15)

- [[Chomsky Hierarchy]] — A four-level classification of formal grammars by expressive power: regular ⊂ context-free ⊂ context-sensitive ⊂ recursively enumerable, each recognised by a more powerful machine.
- [[Church-Turing Thesis]] — The hypothesis that any function 'effectively computable' by any means is computable by a Turing machine — equating the intuitive notion of computation with the formal one.
- [[Computability]] — The study of what can be computed at all, resources aside.
- [[Context-free Grammar]] — A set of production rules powerful enough to describe nested, recursive structure (balanced brackets, arithmetic expressions) — recognised by a pushdown automaton.
- [[Decidability]] — A problem is decidable if an algorithm exists that always halts with a correct yes/no answer; undecidable if no such algorithm can exist for all inputs.
- [[Finite State Machine]] — A computational model with a finite number of states and transitions triggered by inputs — no memory beyond the current state.
- [[Halting Problem]] — The problem of deciding, for an arbitrary program and input, whether it will eventually halt or run forever — proven by Turing to be undecidable: no general algorithm can solve it for all cases.
- [[Lambda Calculus]] — A formal system of computation built entirely from function definition and application — Turing-complete using nothing but anonymous functions.
- [[NP-complete]] — The hardest problems in NP: in NP themselves, and every NP problem reduces to them — so a fast solution to one would solve them all (and prove P = NP).
- [[NP-hard]] — Problems at least as hard as the hardest problems in NP — every NP problem reduces to them — but not necessarily in NP themselves.
- [[P vs NP]] — The open question of whether every problem whose solution can be verified quickly (NP) can also be solved quickly (P) — i.e.
- [[Pushdown Automaton]] — A finite state machine plus an unbounded stack — exactly the power needed to recognize [[Context-free Grammar|context-free languages]].
- [[Regular Expression]] — A pattern language describing sets of strings, formally equivalent to a finite automaton — and in practice the everyday tool for text matching.
- [[Rice's Theorem]] — Every non-trivial question about what a program does (its semantic behavior) — 'does it ever output X?', 'is it malware?', 'are these two programs equivalent?' — is undecidable.
- [[Turing Machine]] — An abstract machine — an infinite tape, a head that reads/writes symbols, and a state table — that formalises what it means to 'compute'.

---
← Back to [[_Home]]
