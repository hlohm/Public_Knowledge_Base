---
type: "term"
branch: "Software Engineering"
aliases: ["PBT", "Generative Testing", "Property Testing"]
tags: [se, testing]
status: "developed"
---

# Property-Based Testing

> **Branch:** [[08 - Software Engineering|Software Engineering]]
> **Also known as:** PBT, Generative Testing, Property Testing

Testing that asserts *invariants* over whole classes of input instead of checking hand-picked examples: the framework generates hundreds of random inputs, verifies the stated property holds for each, and on failure automatically **shrinks** the input to a minimal counterexample.

**Context.** The canonical property is the round-trip: `parse(serialize(x)) == x` — one line that subsumes an unbounded family of example tests, and the standard way to prove a parser/serializer pair loses nothing. Shrinking is the killer feature: instead of a 400-line failing input you get the three-character core of the bug. Born as Haskell's QuickCheck, now everywhere (proptest/quickcheck in Rust, Hypothesis in Python, fast-check in JS). Failing cases worth keeping graduate into a fixed regression corpus — generated tests find the bug, example tests pin it.

## See also

- [[Unit Test]]
- [[Fuzzing]]
- [[TDD]]

## Often confused with

- [[Fuzzing]] — fuzzing hurls malformed input at a program hunting crashes, usually coverage-guided and security-motivated; PBT checks *stated semantic properties* against structured generated input inside the test suite.

## Further reading

- [Wikipedia: QuickCheck](https://en.wikipedia.org/wiki/QuickCheck)
- [Hypothesis documentation: What is property-based testing?](https://hypothesis.works/articles/what-is-property-based-testing/)
