# Research guide: from attractive thesis to falsifiable system

> **A curated path through ternary models, memory, decoding, FPGA dataflow, and agent safety.**  
> Updated 2026-07-11 · 16 verified primary sources · no paywalled downloads

The frozen-model thesis is plausible enough to test, but no single paper proves the whole product. The useful question is not “does 1.58-bit AI work?” It is: **which claim does each experiment retire, on which hardware, without moving the bottleneck elsewhere?**

## The decision stack

| Layer | Design decision | Evidence gate for this repository |
|---|---|---|
| Model | Native ternary training vs. post-training conversion | Reproduce quality and storage on one named checkpoint and revision |
| Exceptions | Uniform ternary vs. protected outlier path | Measure quality, exception density, metadata, and irregular-access cost |
| Context | GQA, latent attention, KV quantization, or a combination | Declare architecture dimensions; measure bytes/token and task quality |
| Decode | Conventional, speculative, or extra prediction heads | Measure acceptance, target calls/token, TTFT, throughput, and memory |
| FPGA | Fixed-layout ternary kernel and memory schedule | Bit-accurate simulation, synthesis report, timing, resources, and named board |
| System | Compute ceiling vs. bandwidth ceiling | Roofline from measured operations and bytes, plus transfer-inclusive timing |
| Authority | Model-issued actions vs. policy-authorized actions | Deny-by-default schemas, adversarial tests, confirmation, and observed results |

## Three reading paths

1. **Fast orientation (about 90 minutes):** BitNet b1.58 → GQA → hardware analysis of MLA → speculative decoding → FINN → Roofline → AgentDojo.
2. **Stage 1 implementation:** BitNet and Bitnet.cpp → LLM.int8() and SpQR → GQA/KIVI → speculative decoding/Medusa → Roofline → NIST AI 600-1.
3. **Stage 2 FPGA preparation:** BitNet b1.58 → Bitnet.cpp → BISMO → FINN → hardware analysis of MLA → Roofline. Keep the software golden model beside every RTL/HLS experiment.

---

## 01 · Native low-bit and ternary language models

### BitNet: Scaling 1-bit Transformers for Large Language Models

**Citation.** Wang, H. et al. (2023). *BitNet: Scaling 1-bit Transformers for Large Language Models*. arXiv:2310.11453.  
**Source.** [Primary record](https://arxiv.org/abs/2310.11453) · [Local PDF](../research/papers/01-ternary-llms/bitnet-2310.11453.pdf)

- **Why it matters:** Introduces BitLinear and a training-from-scratch route for 1-bit weights, making low-bit behavior part of the learned model rather than an afterthought.
- **Concrete implication:** Treat the native-low-bit candidate as its own training architecture and checkpoint lineage. Benchmark it against a matched full-precision baseline at equal model size and training exposure.
- **Caveat:** The paper is marked work in progress. Its language-model results do not establish Pocket Pet quality, edge latency, FPGA feasibility, or total-system energy.

### The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits

**Citation.** Ma, S. et al. (2024). *The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits*. arXiv:2402.17764.  
**Source.** [Primary record](https://arxiv.org/abs/2402.17764) · [Local PDF](../research/papers/01-ternary-llms/bitnet-b1.58-2402.17764.pdf)

- **Why it matters:** Moves the ordinary weight alphabet to `{−1, 0, +1}`, the representation at the center of this repository’s hardware hypothesis.
- **Concrete implication:** Define the exact ternary encoding, group scales, activation precision, accumulators, normalization, embeddings, and output head before quoting “1.58 bits.” Report effective package bits/parameter, not entropy alone.
- **Caveat:** Ternary arithmetic reduces weight cost; it does not remove activation, attention, KV-cache, normalization, memory, or control costs. Paper results are not a 7B–9B product measurement.

### Bitnet.cpp: Efficient Edge Inference for Ternary LLMs

**Citation.** Wang, J. et al. (2025). *Bitnet.cpp: Efficient Edge Inference for Ternary LLMs*. arXiv:2502.11880.  
**Source.** [Primary record](https://arxiv.org/abs/2502.11880) · [Local PDF](../research/papers/01-ternary-llms/bitnet-cpp-2502.11880.pdf)

- **Why it matters:** Supplies concrete CPU-oriented ternary packing and mixed-precision GEMM designs, including lookup-table and 2-bit-plus-scale paths.
- **Concrete implication:** Use its packing layout and lossless decode semantics as candidates for the Stage 1 reference, then compare against a transparent scalar golden implementation.
- **Caveat:** Its reported speedups are tied to its models, CPU implementations, baselines, and test machines. They are neither FPGA measurements nor guaranteed end-to-end conversational speedups.

---

## 02 · Mixed precision and outlier protection

### LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale

**Citation.** Dettmers, T., Lewis, M., Belkada, Y., & Zettlemoyer, L. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. NeurIPS 2022; arXiv:2208.07339.  
**Source.** [Primary record](https://arxiv.org/abs/2208.07339) · [Local PDF](../research/papers/02-mixed-precision-outliers/llm-int8-2208.07339.pdf)

- **Why it matters:** Shows a measured case where a small set of activation feature dimensions is handled separately at higher precision.
- **Concrete implication:** Prototype a protected activation path and record outlier frequency by layer and workload. Size hardware islands from measured traces, never from a universal percentage.
- **Caveat:** This is an 8-bit mixed-precision method for the evaluated transformer families. It does not prove that the same outlier structure, thresholds, or quality behavior holds for a native ternary model.

### SpQR: A Sparse-Quantized Representation for Near-Lossless LLM Weight Compression

**Citation.** Dettmers, T. et al. (2023). *SpQR: A Sparse-Quantized Representation for Near-Lossless LLM Weight Compression*. arXiv:2306.03078.  
**Source.** [Primary record](https://arxiv.org/abs/2306.03078) · [Local PDF](../research/papers/02-mixed-precision-outliers/spqr-2306.03078.pdf)

- **Why it matters:** Makes the protected-weight idea explicit: most weights are compressed while sensitive weights remain a sparse higher-precision structure.
- **Concrete implication:** Include indices, scales, alignment waste, sparse gathers, and load balance when estimating a protected path. Compare quality and real bytes—not only nominal weight bits.
- **Caveat:** Sparse exceptions can trade arithmetic savings for metadata and irregular memory traffic. SpQR’s post-training results do not validate a fixed ternary training recipe.

---

## 03 · KV-cache and attention architecture

### GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints

**Citation.** Ainslie, J. et al. (2023). *GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*. EMNLP 2023; arXiv:2305.13245.  
**Source.** [Primary record](https://arxiv.org/abs/2305.13245) · [Local PDF](../research/papers/03-kv-cache-attention/gqa-2305.13245.pdf)

- **Why it matters:** Provides the quality/speed middle ground between multi-head and multi-query attention by sharing key/value heads in groups.
- **Concrete implication:** Make KV-head count an explicit architecture and benchmark parameter. Calculate cache bytes from layers × tokens × KV heads × head dimension × K/V × bytes/value.
- **Caveat:** The paper uses uptraining to adapt existing checkpoints. Simply pooling or deleting KV heads from an arbitrary model is not evidence of retained quality.

### DeepSeek-V2 and Multi-head Latent Attention

**Citation.** DeepSeek-AI (2024). *DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model*. arXiv:2405.04434.  
**Source.** [Primary record](https://arxiv.org/abs/2405.04434) · [Local PDF](../research/papers/03-kv-cache-attention/deepseek-v2-mla-2405.04434.pdf)

- **Why it matters:** Introduces Multi-head Latent Attention (MLA), storing a compressed latent representation rather than conventional per-head keys and values.
- **Concrete implication:** For a future architecture—not an arbitrary converted checkpoint—evaluate latent dimension, projection/reconstruction compute, RoPE handling, cache bytes/token, and decode bandwidth together.
- **Caveat:** DeepSeek-V2 is a large mixture-of-experts system with its own training recipe. Its headline efficiency figures cannot be transplanted to a small ternary model or pocket device.

### KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache

**Citation.** Liu, Z. et al. (2024). *KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache*. ICML 2024; arXiv:2402.02750.  
**Source.** [Primary record](https://arxiv.org/abs/2402.02750) · [Local PDF](../research/papers/03-kv-cache-attention/kivi-2402.02750.pdf)

- **Why it matters:** Studies element distributions and uses asymmetric schemes for keys and values, plus a full-precision residual region.
- **Concrete implication:** Keep a recent-token residual window; test key per-channel and value per-token quantization against the exact baseline on long-context tasks. Record scales, zero points, packing, and dequantization time.
- **Caveat:** “2-bit KV” is not automatically a 8× end-to-end memory or speed improvement. Metadata, residual cache, kernels, batch size, context, and hardware determine the realized result.

### Hardware-Centric Analysis of DeepSeek’s Multi-Head Latent Attention

**Citation.** Geens, R., & Verhelst, M. (2025). *Hardware-Centric Analysis of DeepSeek’s Multi-Head Latent Attention*. Electronics Letters; arXiv:2506.02523.  
**Source.** [Primary record](https://arxiv.org/abs/2506.02523) · [Local PDF](../research/papers/03-kv-cache-attention/hardware-analysis-mla-2506.02523.pdf)

- **Why it matters:** Separates two MLA execution choices—reusing derived matrices or recomputing—and studies the resulting memory/compute trade.
- **Concrete implication:** Add both schedules to the accelerator design space. Use measured target bandwidth and compute ceilings to select one; do not assume the smallest cache yields the fastest kernel.
- **Caveat:** The paper uses hardware modeling/design-space exploration, not Pocket Pet board measurements. Model outputs are estimates until reproduced on the named target.

---

## 04 · Reducing sequential decode work

### Fast Inference from Transformers via Speculative Decoding

**Citation.** Leviathan, Y., Kalman, M., & Matias, Y. (2023). *Fast Inference from Transformers via Speculative Decoding*. ICML 2023; arXiv:2211.17192.  
**Source.** [Primary record](https://arxiv.org/abs/2211.17192) · [Local PDF](../research/papers/04-decoding/speculative-decoding-2211.17192.pdf)

- **Why it matters:** Gives a method for accepting multiple draft tokens while preserving the target model’s output distribution.
- **Concrete implication:** Measure acceptance length, draft cost, verifier utilization, target calls per accepted token, TTFT, and decode throughput by prompt class. Optimize for streamed speech latency, not an isolated best case.
- **Caveat:** Speedup depends on draft/target agreement and parallel hardware efficiency. A poor draft model can add work; output-equivalence does not imply identical floating-point traces.

### Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads

**Citation.** Cai, T. et al. (2024). *Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads*. ICML 2024; arXiv:2401.10774.  
**Source.** [Primary record](https://arxiv.org/abs/2401.10774) · [Local PDF](../research/papers/04-decoding/medusa-2401.10774.pdf)

- **Why it matters:** Explores multiple candidate tokens from extra decoding heads, avoiding a fully separate draft model in its core setup.
- **Concrete implication:** Consider prediction heads only if they are trained and frozen with the final model package. Budget their parameters, tree verification, cache behavior, and quality impact in hardware and model manifests.
- **Caveat:** Extra heads and tree attention are not free. Report the chosen acceptance scheme; some settings preserve typical acceptance behavior rather than exact target sampling.

---

## 05 · FPGA and low-bit accelerator discipline

### FINN: A Framework for Fast, Scalable Binarized Neural Network Inference

**Citation.** Umuroglu, Y. et al. (2017). *FINN: A Framework for Fast, Scalable Binarized Neural Network Inference*. FPGA 2017; arXiv:1612.07119.  
**Source.** [Primary record](https://arxiv.org/abs/1612.07119) · [Local PDF](../research/papers/05-fpga-accelerators/finn-1612.07119.pdf)

- **Why it matters:** Demonstrates layer-tailored streaming dataflow, explicit throughput targets, synthesis, board, latency, and power reporting for binarized neural networks.
- **Concrete implication:** Follow its evidence shape in Stage 2: fixed topology, per-layer resources, reproducible generation, resource/timing reports, named board, and board-level measurement.
- **Caveat:** FINN evaluates binary CNN classifiers, not ternary transformer decode. Its operations/s and latency cannot be used as Pocket Pet projections.

### BISMO: A Scalable Bit-Serial Matrix Multiplication Overlay for Reconfigurable Computing

**Citation.** Umuroglu, Y., Rasnayake, L., & Själander, M. (2018). *BISMO: A Scalable Bit-Serial Matrix Multiplication Overlay for Reconfigurable Computing*. FPL 2018; arXiv:1806.08862.  
**Source.** [Primary record](https://arxiv.org/abs/1806.08862) · [Local PDF](../research/papers/05-fpga-accelerators/bismo-1806.08862.pdf)

- **Why it matters:** Provides a parameterized bit-serial matrix engine and an explicit hardware-cost model, useful when activation and exception precision vary.
- **Concrete implication:** Compare a ternary add/subtract/skip array with a bit-serial baseline at equal tensor shapes, clock constraints, device, and I/O assumptions. Report useful matrix results, not binary TOPS alone.
- **Caveat:** BISMO is a general matrix-multiplication overlay, not a complete LLM accelerator. Peak binary operations can exaggerate application benefit when packing, memory, control, or low utilization dominates.

---

## 06 · Memory and energy reasoning

### Roofline: An Insightful Visual Performance Model for Floating-Point Programs and Multicore Architectures

**Citation.** Williams, S., Waterman, A., & Patterson, D. (2008). *Roofline: An Insightful Visual Performance Model for Floating-Point Programs and Multicore Architectures*. UC Berkeley Technical Report UCB/EECS-2008-134; later CACM 52(4), 2009.  
**Source.** [Primary report](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2008/EECS-2008-134.html) · [Local PDF](../research/papers/06-memory-energy/roofline-williams-waterman-patterson-2008-tech-report.pdf)

- **Why it matters:** Relates attainable performance to operational intensity and the lower of compute and memory ceilings—the core test for “fixed weights make it fast.”
- **Concrete implication:** Build separate rooflines for prefill, decode, ternary linear, attention, and KV codec. Count bytes at each relevant memory boundary and define a ternary-relevant operation metric alongside wall-clock latency and joules.
- **Caveat:** Roofline is a bound and diagnostic, not a prediction or energy measurement. Its original FLOP framing must be adapted carefully; optimistic peak ceilings can hide control, dependency, and utilization limits.

---

## 07 · Local agent safety and governance

### AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents

**Citation.** Debenedetti, E. et al. (2024). *AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents*. NeurIPS 2024 Datasets and Benchmarks; arXiv:2406.13352.  
**Source.** [Primary record](https://arxiv.org/abs/2406.13352) · [Local PDF](../research/papers/07-agent-safety/agentdojo-2406.13352.pdf)

- **Why it matters:** Evaluates agents in tasks where untrusted external data can contain instructions, directly relevant to email, browser, calendar, and file integrations.
- **Concrete implication:** Treat tool results as untrusted data, keep authority outside the model, and add attack/utility evaluation for every adapter. Require confirmation for consequential actions even when the model appears confident.
- **Caveat:** Benchmark outcomes depend on its tasks, attacks, models, and defenses. Passing AgentDojo would not certify a local companion or remove the need for permission, isolation, audit, and incident handling.

### NIST AI 600-1: Generative AI Profile

**Citation.** Autio, C. et al. (2024). *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*. NIST AI 600-1.  
**Source.** [Official publication and DOI](https://doi.org/10.6028/NIST.AI.600-1) · [Local PDF](../research/papers/07-agent-safety/nist-ai-600-1-genai-profile.pdf)

- **Why it matters:** Provides an official lifecycle-oriented risk-management profile spanning governance, measurement, content provenance, privacy, security, and incident response.
- **Concrete implication:** Maintain a risk register and evaluation plan per release; document data and model provenance, human oversight, red-team coverage, privacy decisions, monitoring, and incident processes.
- **Caveat:** This voluntary profile is not a product certification, legal opinion, or implementation specification. Compliance with a checklist does not demonstrate that a particular control works.

---

## Experiments this library suggests next

### Stage 1 · Software reference

1. **Package accounting:** report nominal ternary entropy, physical 2-bit packing, scales, exceptions, embeddings, norms, and runtime workspace separately.
2. **Outlier sweep:** compare uniform ternary, protected-weight, and protected-activation variants; plot quality against effective bytes and latency.
3. **Context matrix:** evaluate MHA/GQA-compatible candidates and KV precision/residual-window configurations using bytes/token and long-context quality.
4. **Decode study:** compare baseline decoding, a named draft model, and prediction heads using the same target and prompts.
5. **Measured roofline:** collect operations, memory traffic proxies, latency distribution, peak RSS, and power with the exact machine configuration.
6. **Policy adversary suite:** place malicious instructions in tool outputs and verify deny/confirm behavior independently of the model response.

### Stage 2 · FPGA feasibility

1. Freeze one tensor shape, encoding, scale format, accumulator width, rounding rule, and exception format.
2. Validate bit-for-bit against the Stage 1 golden model on randomized and saturation edge cases.
3. Synthesize a ternary kernel and a fair bit-serial baseline on one named device and toolchain.
4. Publish clocks, timing slack, LUT/FF/BRAM/DSP use, achieved utilization, transfer-inclusive/exclusive latency, and power-estimation method.
5. Add one bounded memory experiment—fixed weight layout **or** compressed KV—not a full-product claim.

## What this evidence does not justify

It does not justify claims of a completed FPGA, an ASIC, 7B–9B real-time performance, a particular battery life, all-day thermals, unrestricted phone control, or quality parity for a not-yet-trained model. Those remain targets or concepts until the corresponding checked-in benchmark, synthesis report, or board measurement exists.

## Provenance and integrity

All local files came from arXiv, NIST, or UC Berkeley’s official technical-report service. See [`research/papers/MANIFEST.csv`](../research/papers/MANIFEST.csv) for canonical URLs, retrieval date, byte counts, page counts, and SHA-256 digests. Public access does not change source copyright or license terms.
