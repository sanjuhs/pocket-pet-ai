# Reference Architecture

## System Boundary

The reference system separates probabilistic understanding from deterministic authority.

```text
ear/phone input
      |
audio/vision preprocessing
      |
frozen-model inference <----> active context + retrieved local memory
      |
structured response or action proposal
      |
deterministic policy controller ----> deny / require confirmation
      |
permission-scoped phone, desktop, or service adapter
      |
observed result returned to model and user
```

The model may interpret, plan, and propose. It does not directly receive unrestricted operating-system capabilities. Adapters expose narrow, typed operations; the controller checks identity, permission, risk, confirmation, and result.

## Logical Components

### Input plane

Low-power voice activity detection, wake handling, noise suppression, and event-driven visual capture should reduce unnecessary full-model execution. Continuous recording is not a default requirement and should not be represented as implemented until it is.

### Inference plane

The long-term target is a frozen 7B–9B multimodal model with mostly ternary weights and protected higher-precision parameters. Stage 1 may use smaller text or audio-capable models to validate tooling. Candidate selection must account for license, architecture access, hardware support, task quality, memory, and conversion effort—not parameter count alone.

### Memory plane

- **Immutable package:** model weights, fixed routing/layout metadata, tokenizer, and static inference configuration.
- **Active memory:** activations, scratch buffers, audio/vision buffers, and hot KV cache.
- **Compressed context:** latent or lower-precision older context, if experimentally validated.
- **Long-term memory:** encrypted, user-inspectable structured records retrieved only when relevant.

KV compression and long-term retrieval are different mechanisms and must be benchmarked separately.

### Action plane

Actions use versioned schemas. The controller enforces deny-by-default capabilities and risk tiers:

- low risk: read non-sensitive local status or prepare a draft;
- medium risk: open an app or modify reversible local state;
- high risk: send, purchase, delete, disclose, change security, or share location—always confirm.

Adapters prefer official APIs, then accessibility trees, with visual clicking only as a constrained fallback. Every action returns observed success or failure.

### Security plane

Secrets and personal memory remain outside model prompts unless needed and authorized. Encrypt writable storage, isolate connector tokens, minimize retention, support deletion, and maintain an audit trail that avoids storing sensitive content by default.

## Hardware Research Mapping

The frozen-model thesis enables fixed tensor shapes, weight layout, routing, sparsity locations, and mixed-precision islands. Candidate accelerator blocks include ternary add/subtract/skip arrays, SRAM scratchpads, weight-near-compute storage, latent-KV codecs, normalization/high-precision units, and streaming decode/audio paths.

These are research candidates. Ternary storage arithmetic alone does not establish end-to-end speed or energy gains: memory traffic, activations, normalization, attention, host transfer, control, and quality-preserving exceptions must all be measured.

## Benchmark Dimensions

- time to first response/token and sustained decoding throughput;
- end-to-end speech latency, when speech is implemented;
- resident and peak memory, including KV growth;
- task quality and action success rate;
- idle, typical, and burst power using a documented method;
- policy false-allow/false-deny behavior;
- kernel timing separately from transfer and complete pipeline timing.

See `docs/stages.md` for the acceptance gates.
