---
type: "term"
branch: "Software Engineering"
aliases: ["IoC", "Hollywood Principle"]
tags: ["se"]
status: "developed"
---

# Inversion of Control

> **Branch:** [[08 - Software Engineering|Software Engineering]]
> **Also known as:** IoC, Hollywood Principle

Flipping who calls whom: instead of your code driving and calling libraries, a framework drives and calls *your* code at defined points. 'Don't call us, we'll call you.'

**Context.** IoC is what distinguishes a framework from a [[Library]] — and [[Dependency Injection]] is its most common concrete form (the container constructs and wires your objects rather than you `new`-ing them). The payoff is pluggability and testability; the cost is that control flow lives in the framework, which is why stack traces in Spring or React feel like someone else's program.

## See also

- [[Dependency Injection]]
- [[Framework]]
- [[Library]]
- [[Coupling]]

## Further reading

- [Fowler: Inversion of Control Containers and the DI pattern](https://martinfowler.com/articles/injection.html)
- [Wikipedia: Inversion of control](https://en.wikipedia.org/wiki/Inversion_of_control)
