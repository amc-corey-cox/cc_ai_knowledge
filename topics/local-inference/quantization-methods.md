---
id: kb-2025-010
title: "Quantization Methods for Large Language Models"
created: 2025-02-10
updated: 2025-02-10

author: human
curation_type: ai_assisted

sources:
  - id: src-001
    type: primary
    title: "GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers"
    authors: ["Frantar et al."]
    url: "https://arxiv.org/abs/2210.17323"
    accessed: 2025-02-10
    published: 2022-10-31
    quotes:
      - text: "GPTQ, a new one-shot weight quantization method based on approximate second-order information, that is both highly-accurate and highly-efficient."
        location: "Abstract"
      - text: "GPTQ can quantize GPT models with 175 billion parameters in approximately four GPU hours, reducing the bitwidth down to 3 or 4 bits per weight, with negligible accuracy degradation relative to the unquantized baseline."
        location: "Abstract"

  - id: src-002
    type: primary
    title: "AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration"
    authors: ["Lin et al."]
    url: "https://arxiv.org/abs/2306.00978"
    accessed: 2025-02-10
    published: 2023-06-01
    quotes:
      - text: "We propose Activation-aware Weight Quantization (AWQ), a hardware-friendly approach for LLM low-bit weight-only quantization. Our method is based on the observation that weights are not equally important: protecting only 1% of salient weights can greatly reduce quantization error."
        location: "Abstract"
      - text: "AWQ does not rely on any backpropagation or reconstruction, so it can well preserve LLMs' generalization ability on different domains and modalities, without overfitting to the calibration set."
        location: "Abstract"

  - id: src-003
    type: primary
    title: "LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale"
    authors: ["Dettmers et al."]
    url: "https://arxiv.org/abs/2208.07339"
    accessed: 2025-02-10
    published: 2022-08-15
    quotes:
      - text: "We develop a procedure for Int8 matrix multiplication for feed-forward and attention projection layers in transformers, which cut the memory needed for inference by half while retaining full precision performance."
        location: "Abstract"
      - text: "We show for the first time that a multi-billion-parameter transformer can be run at the full 16-bit performance level using only 8-bit weights."
        location: "Abstract"

  - id: src-004
    type: primary
    title: "GGUF Format Specification"
    url: "https://github.com/ggerganov/ggml/blob/master/docs/gguf.md"
    accessed: 2025-02-10
    quotes:
      - text: "GGUF is a file format for storing models for inference with GGML and executors based on GGML."
        location: "Introduction"

  - id: src-005
    type: primary
    title: "QuIP#: Even Better LLM Quantization with Hadamard Incoherence and Lattice Codebooks"
    authors: ["Tseng et al."]
    url: "https://arxiv.org/abs/2402.04396"
    accessed: 2025-02-10
    published: 2024-02-06

topics:
  - quantization
  - local-inference
  - optimization
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

# Quantization Methods for Large Language Models

## Overview

Quantization reduces the numerical precision of model weights (and sometimes activations) to make models smaller and faster. A 70B parameter model in 16-bit precision requires ~140GB of memory — far beyond consumer hardware. Quantize to 4-bit and it fits in ~35GB, within reach of high-end consumer GPUs.

The core tradeoff is straightforward: lower precision means smaller models and faster inference, but potentially degraded output quality. The art is in minimizing that quality loss.

## Why Quantization Works

Neural network weights are stored as floating-point numbers, typically 16-bit (FP16/BF16) or 32-bit (FP32). But most of these bits encode precision the model doesn't need. The distribution of weight values is typically concentrated in a narrow range, with a few outliers. Quantization exploits this by mapping the continuous weight values to a smaller set of discrete values.

The key insight: models are remarkably robust to weight perturbations. Small rounding errors in individual weights largely cancel out across millions of parameters. The challenge is handling the outlier weights that carry disproportionate importance.

## Quantization Approaches

### Weight-Only vs. Weight-and-Activation

**Weight-only quantization** compresses just the model weights. During inference, weights are dequantized back to higher precision for the actual computation. This reduces memory and loading time but doesn't reduce computation cost proportionally.

**Weight-and-activation quantization** also quantizes the intermediate values during computation, enabling integer arithmetic on hardware that supports it. More aggressive but potentially more lossy.

Most practical LLM quantization today is weight-only.

### Post-Training Quantization (PTQ) vs. Quantization-Aware Training (QAT)

**PTQ** quantizes a model after training is complete, typically using a small calibration dataset. This is what most methods below use — it's fast (hours, not weeks) and doesn't require retraining.

**QAT** incorporates quantization into the training process, letting the model learn to compensate for precision loss. Produces better results but requires the full training pipeline. More common for smaller models and deployment-critical applications.

## Major Methods

### GPTQ

"A new one-shot weight quantization method based on approximate second-order information, that is both highly-accurate and highly-efficient" [src-001]. GPTQ was a breakthrough because it showed that "GPT models with 175 billion parameters [can be quantized] in approximately four GPU hours, reducing the bitwidth down to 3 or 4 bits per weight, with negligible accuracy degradation" [src-001].

**How it works**: GPTQ quantizes weights layer by layer, using second-order (Hessian) information to determine which weights are most sensitive to quantization error and adjusting remaining weights to compensate. It processes weights in groups and uses a calibration dataset (typically ~128 samples) to measure activation patterns.

**Characteristics**:
- GPU-accelerated quantization and inference
- 4-bit and 3-bit support
- Requires GPU for efficient inference (uses CUDA kernels)
- Widely supported (Hugging Face Transformers, vLLM, text-generation-inference)

### AWQ (Activation-Aware Weight Quantization)

"Based on the observation that weights are not equally important: protecting only 1% of salient weights can greatly reduce quantization error" [src-002].

**How it works**: Instead of treating all weights equally, AWQ identifies the most important weights by looking at activation magnitudes (not weight magnitudes). Weights connected to channels with large activations are scaled up before quantization, preserving their precision. Critically, "AWQ does not rely on any backpropagation or reconstruction, so it can well preserve LLMs' generalization ability on different domains and modalities, without overfitting to the calibration set" [src-002].

**Characteristics**:
- Often slightly better quality than GPTQ at the same bit width
- Hardware-friendly (no special kernel requirements)
- Good generalization — doesn't overfit to calibration data
- 4-bit focus
- Supported by vLLM, text-generation-inference, and many frameworks

### GGUF / llama.cpp Quantization

"GGUF is a file format for storing models for inference with GGML and executors based on GGML" [src-004]. The GGUF format includes a family of quantization types specific to the llama.cpp ecosystem.

**Quantization types** (common ones):
- **Q8_0**: 8-bit, ~8.5 bpw (bits per weight). Virtually lossless.
- **Q6_K**: 6-bit with k-quant optimization. Near-lossless for most models.
- **Q5_K_M**: 5-bit, medium quality. Good balance point.
- **Q4_K_M**: 4-bit, medium quality. Most popular for consumer hardware.
- **Q3_K_M**: 3-bit, medium quality. Noticeable quality loss on smaller models.
- **Q2_K**: 2-bit. Significant quality loss; mainly useful for very large models.
- **IQ4_XS, IQ3_S, etc.**: "Importance matrix" variants that use calibration data for better quality at extreme compression.

The "K" variants (k-quants) use different bit widths for different layers, allocating more bits to sensitive layers. The "IQ" variants use importance-based quantization.

**Characteristics**:
- CPU-first design (runs on any hardware)
- Also supports GPU offloading (CUDA, Metal, Vulkan)
- Self-contained single-file format
- Wide range of quantization levels (2-8 bit)
- The most common format for local inference

### bitsandbytes (LLM.int8 / QLoRA)

Dettmers et al. showed that "a multi-billion-parameter transformer can be run at the full 16-bit performance level using only 8-bit weights" [src-003]. The key was handling outlier features separately — the few dimensions with large magnitudes are kept in 16-bit while everything else is quantized to 8-bit.

**Characteristics**:
- Integrated with Hugging Face Transformers (one-line quantization)
- 8-bit (LLM.int8()) and 4-bit (NF4 for QLoRA) support
- Primary use case: fitting models into GPU memory for fine-tuning (QLoRA)
- Runtime quantization (no separate quantization step)
- NVIDIA GPU required

### QuIP# and Extreme Quantization

Research methods pushing to 2-bit and below. QuIP# uses Hadamard transforms to spread information across weights before quantization, making each weight carry more uniform importance [src-005]. These methods are more experimental but point toward the future.

## Comparison

| Method | Typical Bits | Speed | Hardware | Best For |
|--------|-------------|-------|----------|----------|
| GPTQ | 3-4 | Fast inference | GPU (CUDA) | GPU serving |
| AWQ | 4 | Fast inference | GPU (CUDA) | GPU serving, generalization |
| GGUF | 2-8 | Varies | CPU + optional GPU | Local/consumer, flexibility |
| bitsandbytes | 4-8 | Moderate | GPU (CUDA) | Fine-tuning (QLoRA) |

## Practical Guidelines

### Choosing a Bit Width

- **8-bit**: Virtually no quality loss. Use when memory is tight but not critical.
- **6-bit**: Negligible quality loss for most models. Good default if you have the memory.
- **5-bit**: Slight quality loss, often hard to notice. Good balance.
- **4-bit**: The sweet spot for consumer hardware. Noticeable quality loss on smaller models (<13B), acceptable on larger ones.
- **3-bit**: Measurable quality degradation. Acceptable for very large models (70B+) where it's the only way to fit.
- **2-bit**: Significant degradation. Last resort for extreme constraints.

### Rule of Thumb for Memory

Memory required ≈ (parameters × bits_per_weight) / 8 + overhead

- 7B model at Q4: ~4-5 GB
- 13B model at Q4: ~8-9 GB
- 34B model at Q4: ~20 GB
- 70B model at Q4: ~35-40 GB

Add ~1-2 GB for context (KV cache) depending on sequence length.

### Choosing a Method

- **Running locally on CPU or mixed CPU/GPU?** → GGUF
- **Serving on a GPU?** → AWQ or GPTQ
- **Fine-tuning on limited GPU memory?** → bitsandbytes (QLoRA)
- **Need maximum quality at given bit width?** → AWQ or IQ-quants (GGUF)

## Further Reading

- [GPTQ Paper](https://arxiv.org/abs/2210.17323) [src-001]
- [AWQ Paper](https://arxiv.org/abs/2306.00978) [src-002]
- [LLM.int8() Paper](https://arxiv.org/abs/2208.07339) [src-003]
- [GGUF Spec](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md) [src-004]
- [Inference Engines](inference-engines.md) - Software that runs quantized models
- [Hardware and Optimization](hardware-and-optimization.md) - Sizing your setup
