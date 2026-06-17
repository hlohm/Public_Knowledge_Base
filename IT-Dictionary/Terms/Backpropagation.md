---
type: "term"
branch: "AI & Machine Learning"
aliases: ["Backprop"]
tags: [ai, fundamental]
status: "developed"
---

# Backpropagation

> **Branch:** [[13 - AI & Machine Learning|AI & Machine Learning]]
> **Also known as:** Backprop

The algorithm that efficiently computes the gradient of the loss with respect to every weight in a network, by applying the chain rule backward from output to input.

**Context.** The 1986 insight that made training deep networks feasible — it's the chain rule from calculus applied systematically, reusing intermediate results so the cost is one backward pass rather than perturbing each weight. Gradient descent then uses these gradients to update weights.

## See also

- [[Gradient Descent]]
- [[Neural Network]]
- [[Loss Function]]
- [[Chain Rule]]
- [[Automatic Differentiation]]

## Further reading

- [Wikipedia: Backpropagation](https://en.wikipedia.org/wiki/Backpropagation)
