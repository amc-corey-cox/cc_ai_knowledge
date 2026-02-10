---
id: kb-2025-006
title: "Modern Transformer Variants"
created: 2025-02-10
updated: 2025-02-10

author: human
curation_type: ai_assisted

sources:
  - id: src-001
    type: primary
    title: "Language Models are Unsupervised Multitask Learners"
    authors: ["Radford et al."]
    url: "https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf"
    accessed: 2025-02-10
    published: 2019-02-14
    quotes:
      - text: "Language models can be trained without any explicit supervision"
        location: "Abstract (paraphrased from title/introduction)"
      - text: "We demonstrate that language models begin to learn these tasks without any explicit supervision when trained on a new dataset of millions of webpages called WebText."
        location: "Abstract"

  - id: src-002
    type: primary
    title: "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"
    authors: ["Devlin et al."]
    url: "https://arxiv.org/abs/1810.04805"
    accessed: 2025-02-10
    published: 2018-10-11
    quotes:
      - text: "Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers."
        location: "Abstract"
      - text: "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers."
        location: "Abstract"

  - id: src-003
    type: primary
    title: "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer"
    authors: ["Raffel et al."]
    url: "https://arxiv.org/abs/1910.10683"
    accessed: 2025-02-10
    published: 2019-10-23
    quotes:
      - text: "We introduce a unified framework that converts all text-based language problems into a text-to-text format."
        location: "Abstract"

  - id: src-004
    type: primary
    title: "Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer"
    authors: ["Shazeer et al."]
    url: "https://arxiv.org/abs/1701.06538"
    accessed: 2025-02-10
    published: 2017-01-23
    quotes:
      - text: "The MoE consists of a number of experts, each a simple feed-forward neural network, and a trainable gating network which selects a sparse combination of the experts to process each input."
        location: "Section 2 - The Structure of the Mixture-of-Experts Layer"

  - id: src-005
    type: primary
    title: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
    authors: ["Dao et al."]
    url: "https://arxiv.org/abs/2205.14135"
    accessed: 2025-02-10
    published: 2022-05-27
    quotes:
      - text: "We propose FlashAttention, an IO-aware exact attention algorithm that uses tiling to reduce the number of memory reads/writes between GPU high bandwidth memory (HBM) and GPU on-chip SRAM."
        location: "Abstract"

  - id: src-006
    type: primary
    title: "RoFormer: Enhanced Transformer with Rotary Position Embedding"
    authors: ["Su et al."]
    url: "https://arxiv.org/abs/2104.09864"
    accessed: 2025-02-10
    published: 2021-04-20
    quotes:
      - text: "We propose a novel method named Rotary Position Embedding (RoPE) to encode position information with a rotation matrix."
        location: "Abstract"

  - id: src-007
    type: primary
    title: "GLU Variants Improve Transformer"
    authors: ["Shazeer"]
    url: "https://arxiv.org/abs/2002.05202"
    accessed: 2025-02-10
    published: 2020-02-12

topics:
  - transformers
  - architecture
  - model-variants
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

# Modern Transformer Variants

## Overview

The original 2017 Transformer was an encoder-decoder model for machine translation. Since then, the architecture has diverged into several major families, each optimized for different use cases. This article surveys the key variants and the innovations that have pushed transformers to their current scale.

## Architectural Families

### Decoder-Only (GPT Family)

The GPT approach uses only the transformer decoder with causal (left-to-right) self-attention masking. Each token can only attend to tokens before it, making the model naturally autoregressive - it generates text one token at a time.

Radford et al. showed that "language models begin to learn these tasks without any explicit supervision when trained on a new dataset of millions of webpages" [src-001]. The key insight was that a large enough language model, trained on enough data, develops general capabilities as a byproduct of next-token prediction.

**Examples**: GPT-2, GPT-3, GPT-4, Llama, Mistral, Claude's underlying architecture, Gemini

**Strengths**: Natural text generation, scales well, simple training objective (predict next token)
**Tradeoffs**: Unidirectional context (can't look ahead), generation is inherently sequential at inference time

Decoder-only models dominate the current LLM landscape. Nearly all frontier models use this architecture.

### Encoder-Only (BERT Family)

BERT uses only the transformer encoder with bidirectional attention - each token can attend to all other tokens. "BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers" [src-002].

BERT is trained with **masked language modeling** (MLM): randomly mask 15% of input tokens and predict them. This forces the model to develop deep bidirectional representations, since any token might need to be predicted.

**Examples**: BERT, RoBERTa, DeBERTa, ELECTRA

**Strengths**: Rich bidirectional representations, excellent for classification and understanding tasks
**Tradeoffs**: Not naturally generative (can't produce open-ended text), largely superseded by decoder-only models for most tasks

### Encoder-Decoder (T5 Family)

T5 preserves the original transformer structure but frames all tasks as text-to-text: "a unified framework that converts all text-based language problems into a text-to-text format" [src-003]. Translation, summarization, question answering, and classification all become "input text in, output text out."

**Examples**: T5, FLAN-T5, BART, mBART, UL2

**Strengths**: Natural fit for tasks with distinct input/output (translation, summarization), can leverage encoder's bidirectional context
**Tradeoffs**: More complex than decoder-only, less common in frontier models

## Key Innovations Since 2017

### Mixture of Experts (MoE)

MoE replaces the dense feed-forward layers with multiple parallel "expert" networks and a learned routing mechanism. "The MoE consists of a number of experts, each a simple feed-forward neural network, and a trainable gating network which selects a sparse combination of the experts to process each input" [src-004].

Only a subset of experts (typically 1-2 out of 8+) are activated per token, so the model has many more total parameters than it uses for any given input. This allows much larger model capacity without proportionally increasing compute.

**Examples**: Mixtral 8x7B (activates 2 of 8 experts per token), GPT-4 (reported to use MoE), DeepSeek-V3

**Tradeoffs**: Higher memory (all experts must be loaded), routing instability during training, but dramatically better compute efficiency per parameter

### Rotary Position Embeddings (RoPE)

RoPE replaced the original sinusoidal and learned position embeddings. Su et al. "propose a novel method named Rotary Position Embedding (RoPE) to encode position information with a rotation matrix" [src-006].

RoPE encodes positions by rotating the query and key vectors in 2D subspaces. The dot product between rotated vectors naturally decays with distance, giving the model a built-in recency bias. Critically, RoPE can be extrapolated to longer sequences than seen during training, though various extensions (YaRN, dynamic NTK scaling) improve this further.

**Adopted by**: Llama, Mistral, Qwen, PaLM, Gemma, and most modern open models

### SwiGLU / Gated Linear Units

The original transformer FFN used ReLU activation: `FFN(x) = max(0, xW₁ + b₁)W₂ + b₂`. Shazeer showed that gated variants, particularly SwiGLU, consistently outperform ReLU in transformers [src-007]:

```
SwiGLU(x) = (x·W₁ ⊙ Swish(x·W_gate))·W₂
```

The gating mechanism (element-wise multiplication with a learned gate) gives the network more expressive power. SwiGLU is now standard in most modern architectures.

### FlashAttention

FlashAttention doesn't change the mathematical operation - it computes exact attention - but radically changes *how* it's computed on GPUs. Dao et al. "propose FlashAttention, an IO-aware exact attention algorithm that uses tiling to reduce the number of memory reads/writes between GPU high bandwidth memory (HBM) and GPU on-chip SRAM" [src-005].

By restructuring the computation to minimize data movement between memory levels (not just minimize FLOPs), FlashAttention achieves 2-4x wall-clock speedup and enables much longer context lengths. FlashAttention-2 and FlashAttention-3 further improved performance.

**Impact**: Enabled the jump from ~4K to 128K+ context lengths in production models.

### Grouped Query Attention (GQA)

The original multi-head attention has separate K and V projections for each head. GQA shares K and V across groups of heads (e.g., 8 query heads per KV head). This dramatically reduces the KV cache size during inference - the primary memory bottleneck for long-context generation - with minimal quality loss.

**Adopted by**: Llama 2 70B, Llama 3, Mistral, and most production models

### RMSNorm

A simplification of LayerNorm that drops the mean-centering step and only normalizes by root mean square. Slightly cheaper to compute, and empirically works just as well. Standard in Llama and most modern architectures.

### Pre-LN vs. Post-LN

The original transformer applies LayerNorm after the residual connection (Post-LN). Most modern models apply it before the sub-layer (Pre-LN), which produces more stable gradients and is easier to train at scale. Some architectures sandwich normalization both before and after.

## The Modern Recipe

A typical 2024-2025 frontier model combines:

| Component | Original (2017) | Modern Standard |
|-----------|-----------------|-----------------|
| Architecture | Encoder-decoder | Decoder-only |
| Position encoding | Sinusoidal | RoPE |
| Normalization | Post-LN LayerNorm | Pre-LN RMSNorm |
| FFN activation | ReLU | SwiGLU |
| Attention | Multi-head | Grouped Query (GQA) |
| Attention kernel | Naive | FlashAttention |
| Sparsity | Dense | MoE (for some) |
| Context length | 512 tokens | 128K-1M+ tokens |

Each of these changes is incremental, but together they represent a fundamentally different beast from the 2017 model.

## Further Reading

- [GPT-2 Paper](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) [src-001]
- [BERT Paper](https://arxiv.org/abs/1810.04805) [src-002]
- [FlashAttention Paper](https://arxiv.org/abs/2205.14135) [src-005]
- [The Attention Mechanism](attention-mechanism.md) - Foundation for all variants
- [Transformer Architecture Overview](transformer-architecture.md) - The original design
