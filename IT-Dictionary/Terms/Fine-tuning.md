---
type: "term"
branch: "AI & Machine Learning"
tags: [ai, modern]
status: "developed"
---

# Fine-tuning

> **Branch:** [[13 - AI & Machine Learning|AI & Machine Learning]]

Further training a pre-trained model on a smaller, task- or domain-specific dataset to specialise it, rather than training from scratch.

**Context.** A form of transfer learning that reuses the expensive general pre-training and adapts cheaply. Efficient variants (LoRA, adapters) tune only a small fraction of parameters. The practical question is usually fine-tuning vs. RAG vs. prompting — fine-tuning changes *behaviour/style*, RAG supplies *knowledge*.

## See also

- [[LLM]]
- [[Transfer Learning]]
- [[Training]]
- [[RAG]]
- [[LoRA]]
- [[Pre-training]]

## Often confused with

- [[RAG]] — Fine-tuning bakes new behaviour/style into the weights; RAG injects fresh knowledge at query time without changing the model.

## Further reading

- [Wikipedia: Fine-tuning (deep learning)](https://en.wikipedia.org/wiki/Fine-tuning_(deep_learning))
