---
type: "term"
branch: "Programming Languages"
aliases: ["Abstract Syntax Tree"]
tags: [pl]
status: "developed"
---

# AST

> **Branch:** [[07 - Programming Languages|Programming Languages]]
> **Also known as:** Abstract Syntax Tree

A tree representation of source code's structure, produced by the parser, abstracting away syntactic noise (parentheses, semicolons) into the essential grammar.

**Context.** The data structure nearly all code tooling operates on — compilers, linters, formatters (Prettier), refactoring tools, and codemods all walk the AST rather than raw text. Understanding it demystifies how 'magic' dev tools work.

## See also

- [[Compiler]]
- [[Parser]]
- [[Lexer]]
- [[Context-free Grammar]]

## Further reading

- [Wikipedia: Abstract syntax tree](https://en.wikipedia.org/wiki/Abstract_syntax_tree)
