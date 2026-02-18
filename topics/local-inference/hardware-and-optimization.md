---
id: kb-2025-012
title: "Hardware Requirements and Optimization for Local LLM Inference"
created: 2025-02-10
updated: 2025-02-10

author: human
curation_type: ai_assisted

sources:
  - id: src-001
    type: primary
    title: "Efficient Memory Management for Large Language Model Serving with PagedAttention"
    authors: ["Kwon et al."]
    url: "https://arxiv.org/abs/2309.06180"
    accessed: 2025-02-10
    published: 2023-09-12
    quotes:
      - text: "In LLM serving, the KV cache memory for each request is huge and grows and shrinks dynamically. When managed inefficiently, this memory can be significantly wasted by fragmentation and redundant duplication."
        location: "Abstract"

  - id: src-002
    type: primary
    title: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
    authors: ["Dao et al."]
    url: "https://arxiv.org/abs/2205.14135"
    accessed: 2025-02-10
    published: 2022-05-27
    quotes:
      - text: "We argue that a missing principle is making attention algorithms IO-aware — accounting for reads and writes between levels of GPU memory."
        location: "Abstract"

  - id: src-003
    type: primary
    title: "Speculative Decoding with Big Little Decoder"
    authors: ["Kim et al."]
    url: "https://arxiv.org/abs/2302.07863"
    accessed: 2025-02-10
    published: 2023-02-15
    quotes:
      - text: "The key observation is that in many practical settings, there exists a much smaller model that can generate a large proportion of the tokens that the larger model would have generated."
        location: "Abstract"

  - id: src-004
    type: primary
    title: "Fast Inference from Transformers via Speculative Decoding"
    authors: ["Leviathan et al."]
    url: "https://arxiv.org/abs/2211.17192"
    accessed: 2025-02-10
    published: 2022-11-30
    quotes:
      - text: "Speculative decoding works by first using a faster but less powerful draft model to generate a sequence of tokens, and then using the target model to verify them in parallel."
        location: "Section 1 (paraphrased from introduction)"

  - id: src-005
    type: secondary
    title: "Apple Silicon GPU Memory Architecture"
    url: "https://developer.apple.com/documentation/metal/gpu_devices_and_work_submission/understanding_gpu_family_4"
    accessed: 2025-02-10

topics:
  - local-inference
  - hardware
  - optimization
  - ai-fundamentals

confidence: high
verified: false
verified_by: unverified
verification_notes: "AI-assisted draft; memory estimates are approximate and based on general formulas, specific numbers should be verified against current hardware specs"

ai_metadata:
  model: claude-opus-4-6
  generation_date: 2025-02-10
  reviewed_by: pending
---

# Hardware Requirements and Optimization for Local LLM Inference

## Overview

Running LLMs locally is fundamentally a memory problem. The model weights must fit in memory (GPU VRAM, system RAM, or both), and there must be headroom for the KV cache that grows with context length. Once a model fits in memory, the next constraint is memory bandwidth — how fast you can feed weights to the compute units.

This article covers practical sizing, hardware options, and optimization techniques for local inference.

## The Memory Equation

### Model Weights

The base memory requirement for model weights:

```
Weight memory = parameters × (bits_per_weight / 8)
```

For a 70B model:
- FP16 (16-bit): 70B × 2 bytes = **140 GB**
- Q8 (8-bit): 70B × 1 byte = **70 GB**
- Q4 (4-bit): 70B × 0.5 bytes = **35 GB**

### KV Cache

During generation, the model stores key and value tensors for all previous tokens in the sequence. This is the **KV cache**, and it grows with context length.

Per-token KV cache size:
```
KV per token = 2 × num_layers × num_kv_heads × head_dim × bytes_per_value
```

For Llama 3 70B (80 layers, 8 KV heads, 128 head dim, FP16):
- Per token: 2 × 80 × 8 × 128 × 2 = **327 KB per token**
- At 4K context: ~1.3 GB
- At 32K context: ~10.5 GB
- At 128K context: ~42 GB

"In LLM serving, the KV cache memory for each request is huge and grows and shrinks dynamically" [src-001]. For long-context local use, the KV cache can rival or exceed the weight memory.

### Total Memory

```
Total ≈ weight_memory + kv_cache + overhead (~500MB-1GB)
```

## Hardware Options

### NVIDIA GPUs (CUDA)

The default choice for LLM inference. Key specs that matter:

| GPU | VRAM | Bandwidth | Approx. Price (2024-2025) |
|-----|------|-----------|--------------------------|
| RTX 4060 | 8 GB | 272 GB/s | ~$300 |
| RTX 4070 Ti Super | 16 GB | 672 GB/s | ~$800 |
| RTX 4090 | 24 GB | 1,008 GB/s | ~$1,600-2,000 |
| RTX 5090 | 32 GB | 1,792 GB/s | ~$2,000 |
| A100 | 40/80 GB | 2,039 GB/s | ~$10,000+ (used) |
| H100 | 80 GB | 3,350 GB/s | ~$25,000+ |

**VRAM is the hard constraint** — if the model doesn't fit, it doesn't run (on GPU alone). Bandwidth determines generation speed.

**Multi-GPU**: Two GPUs can be combined via tensor parallelism, but NVLink bandwidth matters. Consumer GPUs communicate over PCIe (64 GB/s), which is significantly slower than NVLink (900 GB/s on H100). Multi-GPU on consumer cards works but doesn't scale linearly.

### Apple Silicon (Unified Memory)

Apple's M-series chips share memory between CPU and GPU, which is uniquely advantageous for LLMs:

- **M1/M2/M3 Pro**: 18-36 GB unified memory
- **M2/M3/M4 Max**: 32-128 GB unified memory
- **M2/M3/M4 Ultra**: 64-192 GB unified memory

The advantage: a Mac Studio with 192GB can load a 70B model at Q4 with room to spare, something that would require multiple NVIDIA GPUs. The disadvantage: GPU memory bandwidth on Apple Silicon (~400-800 GB/s on Max/Ultra) is lower than high-end NVIDIA GPUs, so token generation is slower per token.

**Best for**: Large models that don't fit in discrete GPU VRAM, long-context workloads, single-user local use where throughput isn't critical.

### CPU-Only Inference

When no GPU is available (or the model is too large for any GPU):

- Runs entirely in system RAM (64-512+ GB is commodity)
- Memory bandwidth is the bottleneck: DDR5 maxes around 50-90 GB/s (vs. 1,000+ GB/s for high-end GPUs)
- Token generation is 5-20x slower than GPU
- Viable for smaller models (7-13B quantized) or when latency isn't critical

llama.cpp is the primary engine for CPU inference.

### Partial GPU Offloading

When a model almost fits in VRAM, you can offload some layers to GPU and keep the rest in RAM. llama.cpp handles this natively with the `-ngl` (number of GPU layers) flag.

Performance depends on how many layers fit on GPU:
- 100% of layers on GPU → full GPU speed
- 75% on GPU → decent speed, some CPU bottleneck
- 25% on GPU → only marginally faster than CPU-only

The layers that run on CPU become the bottleneck because data must transfer between CPU and GPU memory each forward pass.

## Optimization Techniques

### Memory Bandwidth is King

For autoregressive generation (the common case), LLM inference is **memory-bandwidth bound**, not compute-bound. Each generated token requires reading the entire model weights from memory once. The arithmetic intensity is extremely low.

This means:
- Faster GPU compute (more CUDA cores) helps less than you'd expect
- Higher memory bandwidth helps linearly
- Quantization helps because smaller weights = less memory to read per token

**Tokens per second** (rough estimate for generation):
```
tokens/sec ≈ memory_bandwidth / model_size_in_bytes
```

A Q4 70B model (~35 GB) on an RTX 4090 (1,008 GB/s): ~29 tokens/sec theoretical maximum. Real numbers are lower due to overhead, but this sets the ceiling.

### Prompt Processing vs. Generation

**Prompt processing** (prefill) processes all input tokens in parallel. This is compute-bound and benefits from GPU parallelism. It's much faster per-token than generation.

**Generation** (decoding) produces one token at a time. This is memory-bandwidth-bound. Each token requires a full pass through the model weights.

This asymmetry means a 10,000-token prompt might process in a few seconds, but generating 1,000 tokens of response takes significantly longer.

### Continuous Batching

When serving multiple users, **continuous batching** interleaves requests. While one request is waiting for its next token, the GPU processes tokens for other requests. This dramatically improves throughput (tokens/second across all users) without hurting per-request latency much. This is a core optimization in vLLM and other serving engines.

### Speculative Decoding

Uses a small "draft" model to predict several tokens ahead, then verifies them all in a single pass through the large model. "In many practical settings, there exists a much smaller model that can generate a large proportion of the tokens that the larger model would have generated" [src-003].

The large model processes the draft tokens in parallel (like prompt processing — fast), accepting correct predictions and rejecting wrong ones. When most predictions are correct, you get multiple tokens per large-model forward pass, improving throughput.

**When it helps**: When a cheap draft model predicts well (common tokens, formulaic text). Less helpful for creative or reasoning-heavy generation.

### Flash Attention and IO-Awareness

FlashAttention makes attention computation faster not by reducing FLOPs but by reducing memory traffic. The key principle: "making attention algorithms IO-aware — accounting for reads and writes between levels of GPU memory" [src-002].

This matters most for long contexts where the attention matrix is large. FlashAttention computes attention in tiles, keeping intermediate results in fast SRAM rather than writing to slow HBM. This is now standard in essentially all inference engines.

### KV Cache Quantization

The KV cache can be quantized separately from model weights (typically to 8-bit or 4-bit), reducing its memory footprint. This extends the maximum context length for a given amount of memory, at the cost of slight quality degradation in long-context tasks.

## Practical Sizing Guide

### What can I run?

| Available Memory | Model Size (Q4) | Examples |
|-----------------|-----------------|----------|
| 8 GB VRAM | Up to 7B | Llama 3.1 8B, Mistral 7B, Qwen 2.5 7B |
| 16 GB VRAM | Up to 13B | Llama 3.1 8B (with long context), CodeLlama 13B |
| 24 GB VRAM | Up to 30B | Qwen 2.5 32B (tight), Codestral 22B |
| 32 GB VRAM | Up to 40B | Llama 3.1 70B (partial offload) |
| 48 GB VRAM | Up to 70B | Llama 3.1 70B, Qwen 2.5 72B |
| 64 GB unified | Up to 70B | Most 70B models at Q4 with moderate context |
| 128+ GB unified | Up to 120B+ | Large models at higher quant levels |

These are rough guidelines — actual fit depends on quantization level, context length, and engine overhead.

### The "Good Enough" Local Setup

For most local LLM use cases in 2025:
- **Budget**: RTX 4060 (8GB) + 7B models. Surprisingly capable for coding assistance and chat.
- **Mid-range**: RTX 4070 Ti Super (16GB) or Mac with 32-36GB. Runs 7-13B models comfortably.
- **Enthusiast**: RTX 4090/5090 (24-32GB) or Mac with 64-96GB. Runs 30-70B models.
- **No-compromise local**: Mac Studio Ultra (192GB) or multi-GPU. Runs the largest open models.

## Further Reading

- [PagedAttention / vLLM Paper](https://arxiv.org/abs/2309.06180) [src-001]
- [FlashAttention Paper](https://arxiv.org/abs/2205.14135) [src-002]
- [Speculative Decoding Paper](https://arxiv.org/abs/2302.07863) [src-003]
- [Quantization Methods](quantization-methods.md) - How to compress models to fit
- [Inference Engines](inference-engines.md) - Software for running models
