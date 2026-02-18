---
id: kb-2025-011
title: "Local Inference Engines"
created: 2025-02-10
updated: 2025-02-10

author: human
curation_type: ai_assisted

sources:
  - id: src-001
    type: primary
    title: "llama.cpp GitHub Repository"
    authors: ["Georgi Gerganov et al."]
    url: "https://github.com/ggerganov/llama.cpp"
    accessed: 2025-02-10
    quotes:
      - text: "The main goal of llama.cpp is to enable LLM inference with minimal setup and state-of-the-art performance on a wide variety of hardware - locally and in the cloud."
        location: "README"

  - id: src-002
    type: primary
    title: "Efficient Memory Management for Large Language Model Serving with PagedAttention"
    authors: ["Kwon et al."]
    url: "https://arxiv.org/abs/2309.06180"
    accessed: 2025-02-10
    published: 2023-09-12
    quotes:
      - text: "We propose PagedAttention, an attention algorithm inspired by the classical virtual memory and paging techniques in operating systems. On top of it, we build vLLM, an LLM serving system."
        location: "Abstract"
      - text: "PagedAttention allows storing continuous key and value tensors in non-contiguous memory space. Specifically, PagedAttention partitions the KV cache of each sequence into KV blocks."
        location: "Section 4.1 - PagedAttention"

  - id: src-003
    type: primary
    title: "Ollama Documentation"
    url: "https://github.com/ollama/ollama"
    accessed: 2025-02-10
    quotes:
      - text: "Get up and running with large language models."
        location: "README"

  - id: src-004
    type: primary
    title: "SGLang: Efficient Execution of Structured Language Model Programs"
    authors: ["Zheng et al."]
    url: "https://arxiv.org/abs/2312.07104"
    accessed: 2025-02-10
    published: 2023-12-12
    quotes:
      - text: "We introduce SGLang, a system for efficient execution of complex language model programs. SGLang consists of a frontend language and a runtime."
        location: "Abstract"

  - id: src-005
    type: primary
    title: "mlx-lm: Language Models on Apple Silicon"
    url: "https://github.com/ml-explore/mlx-examples/tree/main/llms/mlx_lm"
    accessed: 2025-02-10

topics:
  - local-inference
  - inference-engines
  - serving
  - ai-fundamentals

confidence: high
verified: false
verified_by: unverified
verification_notes: "AI-assisted draft; quotes sourced from repos and papers but need human verification"

ai_metadata:
  model: claude-opus-4-6
  generation_date: 2025-02-10
  reviewed_by: pending
---

# Local Inference Engines

## Overview

Inference engines are the software that actually runs language models — loading weights, processing tokens, managing memory, and generating output. The choice of engine determines what hardware you can use, how fast generation runs, how many concurrent users you can serve, and what model formats you can load.

The landscape splits roughly into two camps: **local/consumer tools** (optimized for single-user, minimal setup) and **serving engines** (optimized for throughput, concurrency, and production deployment).

## Local-First Engines

### llama.cpp

The project that ignited the local LLM movement. "The main goal of llama.cpp is to enable LLM inference with minimal setup and state-of-the-art performance on a wide variety of hardware - locally and in the cloud" [src-001].

**What it is**: A C/C++ implementation of LLM inference with no dependencies beyond a C compiler. Originally built to run Meta's Llama models on MacBooks, it now supports most open model architectures.

**Key strengths**:
- **Universal hardware support**: CPU (x86, ARM), NVIDIA GPU (CUDA), Apple GPU (Metal), AMD GPU (ROCm/Vulkan), Intel GPU (SYCL), and more
- **CPU inference**: Can run entirely on CPU, which no other major engine does well
- **Partial GPU offloading**: Split a model across GPU and CPU when it doesn't fully fit in VRAM
- **GGUF format**: The native quantization format, with the widest range of bit widths (2-8 bit)
- **Minimal dependencies**: Compiles from source with just a C compiler
- **llama-server**: Built-in OpenAI-compatible API server

**Tradeoffs**:
- Single-user focused (limited concurrent request handling compared to serving engines)
- C/C++ codebase can be hard to extend
- Not the fastest option for pure GPU inference

**When to use**: Consumer hardware, mixed CPU/GPU setups, running quantized models locally, when you need maximum hardware compatibility.

### Ollama

A user-friendly wrapper around llama.cpp (and other backends) that handles model management, downloading, and serving. "Get up and running with large language models" [src-003].

**What it is**: Ollama provides a Docker-like experience for LLMs: `ollama pull llama3` downloads a model, `ollama run llama3` starts a conversation, and `ollama serve` exposes an API.

**Key strengths**:
- **Simplest setup**: One command to install, one command to run
- **Model library**: Curated registry of pre-quantized models
- **Modelfile**: Dockerfile-like format for customizing models (system prompts, parameters, adapters)
- **Background service**: Runs as a daemon, handles model loading/unloading
- **OpenAI-compatible API**: Drop-in replacement for many applications

**Tradeoffs**:
- Less control than using llama.cpp directly
- Abstracts away quantization choices (uses its own quant selection)
- Model library is curated but not exhaustive
- Performance overhead vs. raw llama.cpp is minimal but exists

**When to use**: Getting started with local LLMs, application development against a local API, when you want simplicity over fine-tuning control.

### MLX / mlx-lm

Apple's ML framework optimized for Apple Silicon. mlx-lm [src-005] is the language model inference library built on it.

**Key strengths**:
- **Apple Silicon native**: Uses the unified memory architecture directly (GPU and CPU share memory pool)
- **No memory copy**: Models load directly into unified memory, no CPU→GPU transfer needed
- **Python-first**: Easy to extend and customize
- **Quantization support**: 4-bit and 8-bit, with good quality

**Tradeoffs**:
- Apple Silicon only (M1/M2/M3/M4)
- Smaller ecosystem than llama.cpp
- Fewer model architectures supported

**When to use**: Mac users who want native performance without GGUF conversion.

## Serving Engines

### vLLM

The most widely deployed open-source LLM serving engine. Built around **PagedAttention**: "an attention algorithm inspired by the classical virtual memory and paging techniques in operating systems" [src-002].

**The PagedAttention insight**: During inference, the KV cache (stored attention states for generated tokens) wastes enormous amounts of GPU memory due to fragmentation. Traditional systems pre-allocate contiguous memory blocks for the maximum sequence length, wasting memory on shorter sequences. PagedAttention "allows storing continuous key and value tensors in non-contiguous memory space" by partitioning "the KV cache of each sequence into KV blocks" [src-002] — just like virtual memory pages.

**Key strengths**:
- **Throughput**: Optimized for serving many concurrent requests
- **PagedAttention**: ~2-4x better memory utilization than naive implementations
- **Continuous batching**: New requests are added to the batch without waiting for existing ones to finish
- **Broad model support**: Hugging Face Transformers format, GPTQ, AWQ, and more
- **OpenAI-compatible API**: Drop-in replacement for production deployments
- **Tensor parallelism**: Split models across multiple GPUs

**Tradeoffs**:
- GPU-only (NVIDIA primarily, some AMD support)
- Higher minimum hardware requirements than local engines
- More complex setup than Ollama
- Optimized for throughput over single-request latency

**When to use**: Production serving, multi-user scenarios, when you need maximum throughput on GPU hardware.

### SGLang

"A system for efficient execution of complex language model programs" [src-004]. SGLang focuses on structured generation and complex LLM programs (multi-turn, branching, constrained output).

**Key strengths**:
- **RadixAttention**: Automatic KV cache reuse across requests with shared prefixes
- **Structured generation**: Efficient constrained decoding (JSON, regex, grammar)
- **Frontend language**: Python DSL for complex generation programs
- **Competitive throughput**: Often matches or exceeds vLLM on benchmarks

**Tradeoffs**:
- Newer ecosystem, fewer production deployments
- GPU-focused (NVIDIA)
- The frontend DSL is powerful but adds learning curve

**When to use**: Structured output generation, complex multi-step LLM programs, workloads with shared prefixes (e.g., same system prompt across requests).

### Text Generation Inference (TGI)

Hugging Face's serving solution. Rust-based, production-tested at scale on HF's own infrastructure. Good default choice for teams already in the Hugging Face ecosystem.

## Comparison

| Engine | Primary Use | Hardware | Model Format | Ease of Setup |
|--------|------------|----------|--------------|--------------|
| llama.cpp | Local, consumer | CPU + any GPU | GGUF | Medium |
| Ollama | Local, developer | CPU + any GPU | Ollama library | Easy |
| MLX | Local, Mac | Apple Silicon | MLX/safetensors | Easy |
| vLLM | Serving | GPU (NVIDIA/AMD) | HF/GPTQ/AWQ | Medium |
| SGLang | Serving, structured | GPU (NVIDIA) | HF/GPTQ/AWQ | Medium |
| TGI | Serving | GPU (NVIDIA) | HF/GPTQ/AWQ | Medium |

## The OpenAI-Compatible API Convention

Nearly every inference engine now exposes an API matching OpenAI's chat completions format (`/v1/chat/completions`). This has become the de facto standard for LLM APIs, making it possible to swap backends without changing application code. This is one of the most important practical developments in the local LLM ecosystem — it decouples application development from model serving.

## Further Reading

- [llama.cpp GitHub](https://github.com/ggerganov/llama.cpp) [src-001]
- [vLLM Paper](https://arxiv.org/abs/2309.06180) [src-002]
- [Ollama GitHub](https://github.com/ollama/ollama) [src-003]
- [SGLang Paper](https://arxiv.org/abs/2312.07104) [src-004]
- [Quantization Methods](quantization-methods.md) - How models are compressed for these engines
- [Hardware and Optimization](hardware-and-optimization.md) - Choosing hardware for inference
