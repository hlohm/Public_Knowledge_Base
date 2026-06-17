---
type: "term"
branch: "AI & Machine Learning"
tags: [ai, fundamental]
status: "developed"
---

# Gradient Descent

> **Branch:** [[13 - AI & Machine Learning|AI & Machine Learning]]

The optimisation algorithm that trains most models: iteratively adjust parameters in the direction that most reduces a loss function, step by step downhill.

**Context.** The engine of nearly all neural-net training. The **learning rate** (step size) is the critical knob — too big and it diverges, too small and it crawls. Variants (SGD, Adam) and the use of mini-batches make it tractable on huge datasets. Backpropagation is just how the gradients get computed.

## See also

- [[Backpropagation]]
- [[Loss Function]]
- [[Learning Rate]]
- [[Stochastic Gradient Descent]]
- [[Optimization]]

## Further reading

- [Wikipedia: Gradient descent](https://en.wikipedia.org/wiki/Gradient_descent)
