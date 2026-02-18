---
id: kb-2025-005
title: "Transformer Architecture Overview"
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
      - text: "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely."
        location: "Abstract"
      - text: "The encoder maps an input sequence of symbol representations to a sequence of continuous representations. Given z, the decoder then generates an output sequence of symbols one element at a time."
        location: "Section 3.1 - Encoder and Decoder Stacks"
      - text: "Since our model contains no recurrence and no convolution, in order for the model to make use of the order of the sequence, we must inject some information about the relative or absolute position of the tokens in the sequence."
        location: "Section 3.5 - Positional Encoding"
      - text: "We employ a residual connection around each of the two sub-layers, followed by layer normalization."
        location: "Section 3.1 - Encoder and Decoder Stacks"

  - id: src-002
    type: primary
    title: "Layer Normalization"
    authors: ["Ba, Kiros, Hinton"]
    url: "https://arxiv.org/abs/1607.06450"
    accessed: 2025-02-10
    published: 2016-07-21
    quotes:
      - text: "We transpose batch normalization into layer normalization by computing the mean and variance used for normalization from all of the summed inputs to the neurons in a layer on a single training case."
        location: "Section 3 - Layer Normalization"

  - id: src-003
    type: secondary
    title: "The Illustrated Transformer"
    authors: ["Jay Alammar"]
    url: "https://jalammar.github.io/illustrated-transformer/"
    accessed: 2025-02-10
    published: 2018-06-27

topics:
  - transformers
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

# Transformer Architecture Overview

## Overview

The Transformer is a neural network architecture "based solely on attention mechanisms, dispensing with recurrence and convolutions entirely" [src-001]. Introduced by Vaswani et al. in 2017, it replaced the dominant RNN/LSTM paradigm for sequence modeling and became the foundation for virtually all modern large language models.

## The Original Encoder-Decoder Structure

The original Transformer has two halves [src-001]:

- **Encoder**: "maps an input sequence of symbol representations to a sequence of continuous representations"
- **Decoder**: "generates an output sequence of symbols one element at a time"

This was designed for sequence-to-sequence tasks like machine translation. Modern LLMs typically use only the decoder (GPT-style) or only the encoder (BERT-style) - see [Modern Transformer Variants](modern-variants.md).

## Building Blocks

### Token Embeddings

Raw input (text) is first tokenized into subword units, then each token is mapped to a dense vector via a learned embedding table. These vectors are the model's internal representation of tokens.

### Positional Encoding

"Since our model contains no recurrence and no convolution, in order for the model to make use of the order of the sequence, we must inject some information about the relative or absolute position of the tokens in the sequence" [src-001].

The original paper used fixed sinusoidal functions:

```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

These are added to the token embeddings before entering the model. The sinusoidal approach was chosen because it allows the model to generalize to sequence lengths not seen during training. Modern models often use learned positional embeddings or rotary position embeddings (RoPE) instead.

### The Encoder Block

Each encoder layer contains two sub-layers:

1. **Multi-head self-attention** - each token attends to all other tokens (see [Attention Mechanism](attention-mechanism.md))
2. **Feed-forward network (FFN)** - a position-wise fully connected network applied independently to each token: `FFN(x) = max(0, xW₁ + b₁)W₂ + b₂`

Both sub-layers use **residual connections** and **layer normalization**: "We employ a residual connection around each of the two sub-layers, followed by layer normalization" [src-001]. The pattern is:

```
output = LayerNorm(x + SubLayer(x))
```

### The Decoder Block

Each decoder layer has three sub-layers:

1. **Masked multi-head self-attention** - same as encoder, but with a causal mask preventing attention to future positions (critical for autoregressive generation)
2. **Multi-head cross-attention** - queries from decoder, keys/values from encoder output
3. **Feed-forward network** - same structure as encoder

Again, each sub-layer has residual connections and layer normalization.

### Layer Normalization

Layer normalization (LayerNorm) normalizes activations across the feature dimension for each individual input, unlike batch normalization which normalizes across the batch. Ba et al. compute "the mean and variance used for normalization from all of the summed inputs to the neurons in a layer on a single training case" [src-002].

This makes training more stable by keeping activations in a consistent range regardless of batch size. A practical detail: modern implementations often use **Pre-LN** (normalize before the sub-layer) rather than the original **Post-LN** (normalize after), as Pre-LN is easier to train at large scale.

### Output Head

For language modeling, the decoder's output vectors are projected back to vocabulary size via a linear layer, then softmax produces a probability distribution over the next token.

## Key Design Properties

### Parallelism

Unlike RNNs that process tokens sequentially, transformers process all tokens simultaneously during training. This enables massive GPU parallelism and is a primary reason transformers scale so well.

### Depth Through Stacking

The original Transformer used N=6 encoder and decoder layers. Modern models stack far more: GPT-3 uses 96 layers, Llama 2 70B uses 80 layers. Each additional layer allows the model to build more abstract representations.

### Parameter Count

Most parameters live in two places:
- **Attention projections**: The Q, K, V, and output projection matrices in each attention layer
- **FFN layers**: The two weight matrices in each feed-forward block (these often contain ~2/3 of total parameters)
- **Embedding tables**: The token embedding matrix (shared with the output projection in many models)

## The Original Scale

Vaswani et al.'s "big" model:
- d_model = 1024 (hidden dimension)
- 16 attention heads
- 6 layers each for encoder and decoder
- ~213M parameters
- Trained on 8 P100 GPUs for 3.5 days

For comparison, GPT-4 is estimated at over 1 trillion parameters. The architecture has scaled over four orders of magnitude.

## Further Reading

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) - The foundational paper [src-001]
- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) - Excellent visual guide [src-003]
- [The Attention Mechanism](attention-mechanism.md) - Deep dive on attention
- [Modern Transformer Variants](modern-variants.md) - How the architecture has evolved
