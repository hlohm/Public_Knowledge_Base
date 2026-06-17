---
type: "term"
branch: "Programming Languages"
aliases: ["Lexical Analyzer", "Tokenizer", "Scanner"]
tags: ["pl"]
status: "developed"
---

# Lexer

> **Branch:** [[07 - Programming Languages|Programming Languages]]
> **Also known as:** Lexical Analyzer, Tokenizer, Scanner

The first stage of a compiler: turns the raw character stream into **tokens** (identifier `count`, operator `+=`, literal `42`), discarding whitespace and comments.

**Context.** Lexing is regular-language territory ([[Regular Expression]]s / finite automata suffice), which is exactly why it's split from the [[Parser]] — separating the easy character-level problem from the harder structural one. Syntax highlighting is approximately a lexer in your editor; 'unexpected token' errors are the lexer/parser boundary speaking to you.

## See also

- [[Parser]]
- [[Compiler]]
- [[Regular Expression]]
- [[Finite State Machine]]
- [[AST]]

## Further reading

- [Wikipedia: Lexical analysis](https://en.wikipedia.org/wiki/Lexical_analysis)
