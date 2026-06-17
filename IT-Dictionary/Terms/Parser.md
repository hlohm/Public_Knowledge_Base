---
type: "term"
branch: "Programming Languages"
aliases: ["Parsing", "Syntax Analysis"]
tags: ["pl"]
status: "developed"
---

# Parser

> **Branch:** [[07 - Programming Languages|Programming Languages]]
> **Also known as:** Parsing, Syntax Analysis

The compiler stage that assembles the lexer's token stream into a structured [[AST]] according to the language's grammar — and reports syntax errors when the stream doesn't fit.

**Context.** Parsers are where the [[Chomsky Hierarchy]] earns its keep: programming languages are designed to be context-free (parseable by recursive descent or generated LR parsers) precisely so this stage stays tractable. The security angle: hand-rolled parsers for file formats and protocols are a perennial vulnerability source — parsing untrusted input is dangerous work ('langsec' is the field that studies why).

## See also

- [[Lexer]]
- [[AST]]
- [[Compiler]]
- [[Context-free Grammar]]
- [[Input Validation]]

## Further reading

- [Wikipedia: Parsing](https://en.wikipedia.org/wiki/Parsing)
