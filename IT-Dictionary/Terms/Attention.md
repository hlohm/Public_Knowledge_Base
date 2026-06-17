---
type: "term"
branch: "AI & Machine Learning"
aliases: ["Self-attention"]
tags: [ai, modern]
status: "developed"
---

# Attention

> **Branch:** [[13 - AI & Machine Learning|AI & Machine Learning]]
> **Also known as:** Self-attention

A mechanism letting a model weigh the relevance of different input elements to each other when producing each output — dynamically focusing on what matters for the current token.

**Context.** The core innovation of the transformer. Intuitively, for each word it asks 'which other words should I look at to understand this one?' and weights them accordingly. The cost is quadratic in sequence length, which is why long-context efficiency is an active research front.

## See also

- [[Transformer]]
- [[LLM]]
- [[Token]]
- [[Context Window]]
- [[Embedding]]

## Further reading

- [Wikipedia: Attention (machine learning)](https://en.wikipedia.org/wiki/Attention_(machine_learning))
