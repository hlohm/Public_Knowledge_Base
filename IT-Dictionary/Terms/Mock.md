---
type: "term"
branch: "Software Engineering"
aliases: ["Mocking", "Test Double", "Stub"]
tags: ["se", "testing"]
status: "developed"
---

# Mock

> **Branch:** [[08 - Software Engineering|Software Engineering]]
> **Also known as:** Mocking, Test Double, Stub

A stand-in test object replacing a real dependency (database, API, clock) so a unit test runs fast, deterministic, and isolated. Umbrella term: **test double**; a **stub** returns canned data, a **mock** additionally verifies how it was called.

**Context.** Mocks decide what your test *means*: stub-style tests assert state ('the result is X'), mock-style assert interaction ('it called save() once') — the latter couples tests to implementation and turns refactoring into test-rewriting when overused. The standing advice: mock at architectural boundaries (network, disk, time), not between your own classes.

## See also

- [[Unit Test]]
- [[Dependency Injection]]
- [[TDD]]

## Further reading

- [Fowler: Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)
- [Wikipedia: Mock object](https://en.wikipedia.org/wiki/Mock_object)
