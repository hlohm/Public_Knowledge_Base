---
type: "term"
branch: "AI & Machine Learning"
aliases: ["Retrieval-Augmented Generation"]
tags: [ai, modern]
status: "developed"
---

# RAG

> **Branch:** [[13 - AI & Machine Learning|AI & Machine Learning]]
> **Also known as:** Retrieval-Augmented Generation

An LLM technique that retrieves relevant documents (usually by embedding similarity) and feeds them into the prompt as context, so answers are grounded in a specific knowledge base.

**Context.** The standard remedy for two LLM weaknesses at once: stale training knowledge and hallucination. By grounding generation in retrieved, citable source text, it lets a general model answer over private or current data without retraining. Retrieval quality is usually the bottleneck, not the model.

## See also

- [[LLM]]
- [[Embedding]]
- [[Vector Database]]
- [[Hallucination]]
- [[Context Window]]

## Further reading

- [Wikipedia: Retrieval-augmented generation](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
