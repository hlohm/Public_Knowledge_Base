---
type: "term"
branch: "Hardware & Architecture"
tags: ["hardware"]
status: "developed"
---

# Branch Prediction

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]

A CPU mechanism that guesses the outcome of a conditional branch so the pipeline can keep fetching and executing instead of stalling until the branch resolves.

**Context.** Modern predictors are remarkably accurate, which is what makes deep pipelines pay off. The flip side: a misprediction flushes the pipeline, and the predictor state is shared enough across contexts to leak information (a Spectre vector). GPUs sidestep the whole game by not speculating per thread.

## See also

- [[Speculative Execution]]
- [[Out-of-Order Execution]]
- [[Pipeline]]
- [[Branch Divergence]]

## Further reading

- [Branch predictor — Wikipedia](https://en.wikipedia.org/wiki/Branch_predictor)
