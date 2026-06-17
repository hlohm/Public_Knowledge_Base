---
type: "term"
branch: "Programming Languages"
tags: [pl]
status: "developed"
---

# Side Effect

> **Branch:** [[07 - Programming Languages|Programming Languages]]

Any observable change a function makes beyond returning a value — mutating state, I/O, network calls, writing to a database.

**Context.** Not bad, but the source of most complexity in reasoning about code: a function with side effects can't be understood in isolation. Functional programming's whole project is isolating and controlling them (monads, effect systems) so the rest stays pure and predictable.

## See also

- [[Pure Function]]
- [[Referential Transparency]]
- [[Monad]]
- [[State]]

## Further reading

- [Wikipedia: Side effect (computer science)](https://en.wikipedia.org/wiki/Side_effect_(computer_science))
