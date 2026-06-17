---
type: "term"
branch: "AI & Machine Learning"
aliases: ["Cost Function", "Objective Function"]
tags: ["ai"]
status: "developed"
---

# Loss Function

> **Branch:** [[13 - AI & Machine Learning|AI & Machine Learning]]
> **Also known as:** Cost Function, Objective Function

The function that scores how wrong the model's predictions are — mean squared error for regression, cross-entropy for classification. Training is nothing but minimizing this number.

**Context.** The loss *is* the objective: the model becomes whatever the loss rewards, including unintended shortcuts — which makes loss design the steering wheel of ML (and misspecified losses the source of its Goodhart failures). It must be differentiable for [[Gradient Descent]] to work, which is why surrogate losses stand in for the things you actually want (accuracy isn't differentiable; cross-entropy is).

## See also

- [[Gradient Descent]]
- [[Training]]
- [[Backpropagation]]
- [[Overfitting]]

## Further reading

- [Wikipedia: Loss function](https://en.wikipedia.org/wiki/Loss_function)
