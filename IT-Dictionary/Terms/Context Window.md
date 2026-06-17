---
type: "term"
branch: "AI & Machine Learning"
aliases: ["Context Length"]
tags: ["ai", "modern"]
status: "note"
---

# Context Window

> **Branch:** [[13 - AI & Machine Learning|AI & Machine Learning]]
> **Also known as:** Context Length

The maximum number of tokens an [[LLM]] can attend to at once — its entire working memory. Everything the model 'knows' about your conversation lives here; outside it, nothing exists.

**Context.** The window is the binding constraint of LLM application design: [[RAG]], summarization chains, and 'memory' systems are all engineering around its limits. Self-[[Attention]] cost grows with length (classically quadratically), which is why long context was hard-won — and a long window still isn't uniform recall: models attend unevenly across it ('lost in the middle').

## See also

- [[LLM]]
- [[Attention]]
- [[RAG]]
- [[Transformer]]
- [[Embedding]]
