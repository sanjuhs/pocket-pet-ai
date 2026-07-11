# Pocket Pet inference prototype

This directory contains a real, deliberately small transformer inference path—not an API stub and not a precomputed response table. It executes causal attention and a gated feed-forward network in PyTorch. The ordinary projection weights are quantized to `{-1, 0, +1}` on each forward pass, while the largest one percent travel through a sparse protected FP32 path. Attention compresses each token to a learned latent vector and stores that latent as int8 with a per-token FP16 scale.

The implementation is a correctness and architecture instrument. PyTorch does not provide a packed ternary matrix kernel here, so the emulator expands symbols to normal tensors during compute. Consequently, wall-clock performance is **not** a claim about FPGA speed. `storage_report()` separately reports a transparent frozen-export estimate based on two-bit ternary symbols, per-row FP16 scales, FP16 protected values, and 32-bit protected indices.

## Run it

The project pins Python 3.12 because it has stable macOS ARM64 PyTorch wheels.

```bash
uv sync
uv run pytest
uv run python scripts/benchmark.py --device auto --prompt-length 64 --new-tokens 16
uv run jupyter nbconvert --to notebook --execute notebooks/ternary_accelerator.ipynb --output /tmp/ternary_accelerator.executed.ipynb
```

`--device auto` chooses Apple Metal when available and otherwise uses CPU. For tiny matrices CPU can be faster because Metal dispatch overhead dominates.

## What is implemented

- `TernaryLinear`: symmetric, per-output-channel ternarization plus a deterministic global top-magnitude outlier pathway.
- `LatentCausalAttention`: queries remain full width, while a learned latent is cached and later expanded into keys and values.
- `QuantizedLatentCache`: int8 latent values plus FP16 per-token scales, appendable one decoding step at a time.
- `PocketPetTransformer`: token/position embeddings, RMSNorm, causal attention, SwiGLU-style feed-forward blocks, tied output embeddings, greedy or temperature sampling, and incremental decoding.
- `benchmark_model`: median end-to-end prefill/generation latency, generated-token rate, frozen-weight estimate, cache bytes, and an equivalent conventional FP16 K/V baseline.

The compressed cache uses `layers × tokens × (latent_size + 2)` bytes for batch size one: one int8 byte per latent coordinate plus a two-byte scale. A conventional multi-head FP16 cache uses `layers × tokens × 2 × hidden_size × 2` bytes. With the default 128-wide model and 32-wide latent, this is approximately a 15× reduction before allocator overhead.

## Stage 1 — software emulation

Stage 1 establishes invariants before optimizing kernels:

1. Train or load dense weights and identify protected outliers with a fixed rule.
2. Export ternary symbols, channel scales, protected values, and indices.
3. Verify logits and task accuracy against a dense checkpoint; choose the outlier budget based on quality, not storage alone.
4. Measure prefill latency, decode latency, cache growth, peak resident memory, energy, and quality independently.
5. Train the latent projection and K/V expansion layers end-to-end; post-training cache compression alone is not equivalent.

This repository demonstrates steps 1, 2, and the inference mechanics of 4. It does not claim pretrained language ability: weights are randomly initialized so the notebook runs offline without a multi-gigabyte download. Fine-tuning and evaluation against a dense teacher are the next experiment.

## Stage 2 — FPGA handoff

Freeze one exact checkpoint and emit a versioned hardware bundle:

- two-bit packed ternary tiles in the accelerator's physical traversal order;
- FP16 scale table and sparse protected `(index, value)` streams;
- layer dimensions, strides, tile sizes, and SHA-256 checksums;
- int8 latent-cache format and FP16 scale semantics;
- golden input IDs, per-layer activation hashes, logits, and generated IDs.

The first FPGA kernel should implement `y = scale × (sum(x where w=+1) - sum(x where w=-1)) + protected(x)`. Keep FP16 or BF16 accumulation initially, then test narrower fixed-point accumulators against golden vectors. The cache DMA contract is append-only `[batch, token, latent]` int8 data plus `[batch, token, 1]` FP16 scales. K/V expansion should operate in tiles so reconstructed full-width tensors never round-trip to external DRAM.

Acceptance gates should be explicit: bit-exact symbol unpacking; bounded layer error against the emulator; no causal-mask violation; stable long-sequence cache addressing; measured tokens/second, time-to-first-token, joules/token, and DRAM bytes/token. Only after those pass should work move to speculative or multi-token decoding.

## Important limitations

- Ternarization currently happens at runtime for readability; deployment should export once.
- The sparse protected path is represented densely during PyTorch compute, although its storage estimate is sparse.
- Dequantized K/V tensors are materialized for attention; hardware should fuse expansion with tiled attention.
- Learned absolute positions cap context length; a production long-context model should use a suitable rotary or relative scheme.
- Random weights validate mechanics, determinism, memory accounting, and causal behavior—not language quality or accuracy.

