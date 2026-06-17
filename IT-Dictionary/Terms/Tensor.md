---
type: "term"
branch: "AI & Machine Learning"
tags: ["ai"]
status: "developed"
---

# Tensor

> **Branch:** [[13 - AI & Machine Learning|AI & Machine Learning]]

The n-dimensional array that is deep learning's universal data type: a scalar is rank 0, a vector rank 1, a matrix rank 2, a batch of color images rank 4. Frameworks are named after it for a reason.

**Context.** Everything — inputs, weights, activations, gradients — is a tensor, and nearly all computation is tensor contractions (batched [[Matrix Multiplication]]), which is precisely the operation GPUs and [[Tensor Core]]s accelerate. Practical fluency is mostly *shape* fluency: reading `(batch, seq, d_model)` and knowing which axes an operation touches. The ML usage is looser than the physicist's tensor — here it really just means 'n-d array.'

## See also

- [[Matrix Multiplication]]
- [[Tensor Core]]
- [[GPU]]
- [[Neural Network]]
- [[Embedding]]

## Further reading

- [Wikipedia: Tensor (machine learning)](https://en.wikipedia.org/wiki/Tensor_(machine_learning))
