---
type: "term"
branch: "Theory of Computation"
tags: ["theory"]
status: "developed"
---

# Rice's Theorem

> **Branch:** [[10 - Theory of Computation|Theory of Computation]]

Every non-trivial question about what a program *does* (its semantic behavior) — 'does it ever output X?', 'is it malware?', 'are these two programs equivalent?' — is undecidable. The Halting Problem, generalized to everything.

**Context.** Rice's theorem is why static analysis can never be both sound and complete, why antivirus is heuristics rather than proof, and why compiler warnings hedge. The escape hatches define real tooling: restrict the language (non-Turing-complete configs), accept approximation (false positives/negatives), or analyze *syntax* rather than behavior — syntactic properties remain fair game.

## See also

- [[Halting Problem]]
- [[Decidability]]
- [[Computability]]
- [[SAST]]

## Further reading

- [Wikipedia: Rice's theorem](https://en.wikipedia.org/wiki/Rice%27s_theorem)
