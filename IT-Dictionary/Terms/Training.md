---
type: "term"
branch: "AI & Machine Learning"
aliases: ["Model Training"]
tags: ["ai"]
status: "developed"
---

# Training

> **Branch:** [[13 - AI & Machine Learning|AI & Machine Learning]]
> **Also known as:** Model Training

Iteratively adjusting a model's parameters to minimize a [[Loss Function]] over data — in deep learning: forward pass, compute loss, [[Backpropagation|backpropagate]] gradients, update weights, repeat for many **epochs** over **batches**.

**Context.** The discipline lives in the data split: train on one set, tune on validation, report on a test set touched once — because a model can ace training data by memorizing it ([[Overfitting]]) while learning nothing. Training is the expensive, GPU-hungry phase; **inference** (using the trained model) is the cheap one — an asymmetry that shapes the economics of the whole field.

## See also

- [[Loss Function]]
- [[Gradient Descent]]
- [[Backpropagation]]
- [[Overfitting]]
- [[Fine-tuning]]

## Further reading

- [Wikipedia: Training, validation, and test data sets](https://en.wikipedia.org/wiki/Training,_validation,_and_test_data_sets)
