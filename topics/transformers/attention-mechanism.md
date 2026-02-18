---
id: kb-2025-004
title: "The Attention Mechanism"
created: 2025-02-10
updated: 2025-02-10

author: human
curation_type: ai_assisted

sources:
  - id: src-001
    type: primary
    title: "Attention Is All You Need"
    authors: ["Vaswani et al."]
    url: "https://arxiv.org/abs/1706.03762"
    accessed: 2025-02-10
    published: 2017-06-12
    quotes:
      - text: "An attention function can be described as mapping a query and a set of key-value pairs to an output, where the query, keys, values, and output are all vectors."
        location: "Section 3.2 - Attention"
      - text: "We call our particular attention 'Scaled Dot-Product Attention'. The input consists of queries and keys of dimension d_k, and values of dimension d_v."
        location: "Section 3.2.1 - Scaled Dot-Product Attention"
      - text: "Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions."
        location: "Section 3.2.2 - Multi-Head Attention"

  - id: src-002
    type: primary
    title: "Neural Machine Translation by Jointly Learning to Align and Translate"
    authors: ["Bahdanau, Cho, Bengio"]
    url: "https://arxiv.org/abs/1409.0473"
    accessed: 2025-02-10
    published: 2014-09-01
    quotes:
      - text: "We conjecture that the use of a fixed-length vector is a bottleneck in improving the performance of this basic encoder-decoder architecture"
        location: "Abstract"
      - text: "Each time the proposed model generates a word in a translation, it (soft-)searches for a set of positions in a source sentence where the most relevant information is concentrated."
        location: "Abstract"

  - id: src-003
    type: secondary
    title: "The Illustrated Transformer"
    authors: ["Jay Alammar"]
    url: "https://jalammar.github.io/illustrated-transformer/"
    accessed: 2025-02-10
    published: 2018-06-27

topics:
  - transformers
  - attention
  - architecture
  - ai-fundamentals

confidence: high
verified: false
verified_by: unverified
verification_notes: "AI-assisted draft; quotes sourced from papers but need human verification against originals"

ai_metadata:
  model: claude-opus-4-6
  generation_date: 2025-02-10
  reviewed_by: pending
---

# The Attention Mechanism

## Overview

Attention is the core innovation behind modern transformer models. At its heart, it's a mechanism that lets a model dynamically decide which parts of its input are relevant to each part of its output, rather than compressing everything into a fixed-size representation.

## The Problem Attention Solves

Before attention, sequence-to-sequence models (used for translation, summarization, etc.) relied on encoding an entire input sequence into a single fixed-length vector. Bahdanau et al. identified this as a fundamental bottleneck: "the use of a fixed-length vector is a bottleneck in improving the performance of this basic encoder-decoder architecture" [src-002].

Their solution was to let the decoder look back at all encoder hidden states and learn which ones matter for each output step. The model "(soft-)searches for a set of positions in a source sentence where the most relevant information is concentrated" [src-002]. This was the birth of the attention mechanism for neural networks.

## Scaled Dot-Product Attention

Vaswani et al. formalized attention as a general operation: "an attention function can be described as mapping a query and a set of key-value pairs to an output, where the query, keys, values, and output are all vectors" [src-001].

The specific formulation used in transformers is **Scaled Dot-Product Attention** [src-001]:

```
Attention(Q, K, V) = softmax(Q·K^T / √d_k) · V
```

The steps:
1. **Dot product**: Compute similarity between each query and all keys (`Q·K^T`)
2. **Scale**: Divide by `√d_k` to prevent the dot products from growing too large in magnitude, which would push softmax into regions with vanishingly small gradients
3. **Softmax**: Convert to a probability distribution (attention weights)
4. **Weighted sum**: Multiply weights by values to get the output

The query, key, value framing comes from information retrieval: you have a *query* (what you're looking for), *keys* (labels for available information), and *values* (the actual information). The attention weights determine how much of each value to retrieve.

## Multi-Head Attention

Rather than computing attention once, transformers use **multi-head attention**: running multiple attention operations in parallel, each with different learned projections. "Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions" [src-001].

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) · W^O
where head_i = Attention(Q·W_i^Q, K·W_i^K, V·W_i^V)
```

Each "head" learns to attend to different types of relationships. In practice, different heads specialize in different patterns - some track syntactic relationships, others semantic ones, others positional patterns.

## Self-Attention vs. Cross-Attention

**Self-attention**: Queries, keys, and values all come from the same sequence. Each token attends to every other token in the same sequence. This is how a model builds contextual representations - the meaning of a word depends on the words around it.

**Cross-attention**: Queries come from one sequence, keys and values from another. This is used in encoder-decoder models where the decoder needs to attend to the encoder's output (similar to Bahdanau's original formulation).

In decoder-only models (like GPT), only self-attention is used, with a causal mask preventing tokens from attending to future positions.

## Computational Cost

The fundamental cost of self-attention is **O(n^2)** in sequence length, because every token must compute attention scores against every other token. For a sequence of length `n`:
- The attention matrix is `n × n`
- Both compute and memory scale quadratically

This quadratic scaling is the primary constraint on context length and has driven significant research into efficient attention variants (see [Modern Transformer Variants](modern-variants.md)).

## Further Reading

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) - The transformer paper
- [Bahdanau et al., 2014](https://arxiv.org/abs/1409.0473) - Original attention for seq2seq
- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) - Visual walkthrough [src-003]
- [Transformer Architecture Overview](transformer-architecture.md) - How attention fits into the full model
