---
type: "term"
branch: "Software Engineering"
aliases: ["DI", "IoC"]
tags: [se]
status: "developed"
---

# Dependency Injection

> **Branch:** [[08 - Software Engineering|Software Engineering]]
> **Also known as:** DI, IoC

Supplying a component's dependencies from outside (via constructor or setter) rather than having it construct them itself — a form of inversion of control.

**Context.** Decouples a class from *which* concrete implementation it uses, making it testable (inject a mock) and configurable. Frameworks (Spring, .NET DI) automate the wiring, sometimes to the point of magic; the core idea works fine by hand.

## See also

- [[Inversion of Control]]
- [[Coupling]]
- [[SOLID]]
- [[Mock]]
- [[Interface]]

## Further reading

- [Wikipedia: Dependency injection](https://en.wikipedia.org/wiki/Dependency_injection)
