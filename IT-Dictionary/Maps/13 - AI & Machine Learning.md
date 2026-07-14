---
type: "map"
tags: [map, ai]
---

# AI & Machine Learning

> Systems that learn from data: models, training, the vocabulary of the current wave.

## Terms in this branch (22)

- [[AI Agent]] — An LLM wired to act: given tools and a goal, it loops reason→act→observe until done. The step from producing text to taking actions — and the source of agent security risk.
- [[Attention]] — A mechanism letting a model weigh the relevance of different input elements to each other when producing each output — dynamically focusing on what matters for the current token.
- [[Backpropagation]] — The algorithm that efficiently computes the gradient of the loss with respect to every weight in a network, by applying the chain rule backward from output to input.
- [[Context Window]] — The maximum number of tokens an [[LLM]] can attend to at once — its entire working memory.
- [[Deep Learning]] — Machine learning using neural networks with many layers, which learn hierarchical feature representations directly from raw data.
- [[Embedding]] — A dense vector representation of data (a word, sentence, image) in a high-dimensional space where semantic similarity corresponds to geometric closeness.
- [[Fine-tuning]] — Further training a pre-trained model on a smaller, task- or domain-specific dataset to specialise it, rather than training from scratch.
- [[Gradient Descent]] — The optimisation algorithm that trains most models: iteratively adjust parameters in the direction that most reduces a loss function, step by step downhill.
- [[Hallucination]] — When a generative model produces confident, fluent output that is factually wrong or fabricated — plausible-sounding nonsense.
- [[LLM]] — A very large transformer trained on vast text to predict the next token, which yields broad language understanding and generation as an emergent result.
- [[Loss Function]] — The function that scores how wrong the model's predictions are — mean squared error for regression, cross-entropy for classification.
- [[Machine Learning]] — Building systems that learn patterns from data to make predictions or decisions, rather than following explicitly programmed rules.
- [[Model Context Protocol]] — Open protocol standardizing how an AI agent connects to external tools and data — convenient, and how the lethal trifecta gets assembled by accident.
- [[Neural Network]] — A model of interconnected layers of simple units ('neurons') whose weighted connections are tuned during training — a universal function approximator loosely inspired by biology.
- [[Overfitting]] — When a model learns the training data too well — including its noise — and fails to generalise to new data.
- [[RAG]] — An LLM technique that retrieves relevant documents (usually by embedding similarity) and feeds them into the prompt as context, so answers are grounded in a specific knowledge base.
- [[Supervised Learning]] — Training on labelled examples (input → known correct output) so the model learns to map new inputs to outputs — classification (categories) or regression (continuous values).
- [[System Prompt]] — The operator's standing instructions placed ahead of user input; sets role and rules but is a soft boundary, not an access control.
- [[Tensor]] — The n-dimensional array that is deep learning's universal data type: a scalar is rank 0, a vector rank 1, a matrix rank 2, a batch of color images rank 4.
- [[Token]] — The unit a language model processes — typically a sub-word chunk (roughly ¾ of a word in English), produced by a tokeniser from raw text.
- [[Training]] — Iteratively adjusting a model's parameters to minimize a [[Loss Function]] over data — in deep learning: forward pass, compute loss, [[Backpropagation|backpropagate]] gradients, update weights, repeat for many epochs over batches.
- [[Transformer]] — The neural architecture (2017, 'Attention Is All You Need') built on self-attention, which processes all positions in a sequence in parallel and weighs their relationships.

---
← Back to [[_Home]]
