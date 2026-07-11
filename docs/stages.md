# Delivery Stages

The stages are evidence gates. Dates are planning signals, not promises, and later stages do not begin merely because earlier UI work looks complete.

## Stage 1 — Commodity-Hardware Reference System

### Goal

Create a reproducible software proof of concept that simulates the proposed pocket puck on a supported Mac or Linux machine and establishes honest baselines for future acceleration.

### Required Work

1. Publish the landing page, architecture overview, roadmap, and downloadable white paper.
2. Provide a `uv`-managed Python package and explanatory notebook using at least one small candidate model whose license and revision are recorded.
3. Implement or measure:
   - model parameter/storage estimation across precisions;
   - KV-cache memory estimation with declared architecture inputs;
   - a ternary or low-bit linear reference operation checked against a higher-precision baseline;
   - time to first token, decode throughput, peak memory, and task-quality proxy;
   - an optional speech/action loop only when its real dependencies are present.
4. Demonstrate a structured action proposal flowing through deterministic allow/deny/confirm policy logic. Execution may target a safe local sandbox; consequential real-world action is not required.
5. Emit machine-readable benchmark results with full environment metadata.

### Acceptance Criteria

- Fresh-clone web and Python setup instructions work on a documented supported environment.
- CI passes web lint/build/tests and Python lint/tests.
- At least one checked-in benchmark configuration runs end to end without private services.
- Numerical results are reproducible within a declared tolerance or their observed variance is reported.
- The public site and white paper distinguish measured results from estimates and targets.
- No downloaded model weights or credentials are committed.

### Explicit Non-Goals

- Claiming a fabricated FPGA/ASIC speedup or power result.
- Demonstrating a full 7B–9B multimodal model on a custom pocket device.
- Unrestricted Android or iOS control.
- Production-grade always-listening audio or personal-memory storage.

## Stage 2 — FPGA Feasibility Prototype

### Entry Gate

Stage 1 benchmark formats, reference kernels, and quality checks are stable enough to serve as a golden model.

### Goal

Determine, on a named FPGA board and toolchain, whether fixed-layout ternary compute and selected attention/memory techniques produce useful, verifiable kernel-level gains.

### Required Work

1. Define a fixed tensor shape and ternary encoding with a bit-accurate software golden model.
2. Implement addition/subtraction/skip matrix-vector or tiled matrix kernels in synthesizable RTL/HLS.
3. Verify bit accuracy against randomized and edge-case vectors in simulation.
4. Synthesize for one named FPGA target and publish tool version, clock constraints, resource utilization, timing, and power-estimation method.
5. Measure board execution where hardware is available: host transfer excluded and included, throughput, latency distribution, energy method, and numerical agreement.
6. Explore one bounded memory-path question, such as fixed weight layout, double buffering, compressed KV representation, or sparse skipping.
7. Compare against a clearly defined CPU/GPU software baseline while separating kernel, transfer, and end-to-end timing.

### Acceptance Criteria

- Simulation is bit-accurate against the golden model for the committed test suite.
- Synthesis meets its declared timing constraint or reports the failure without hiding it.
- Resource and timing reports are generated reproducibly from scripts and tool versions.
- Any board measurement identifies the exact board, clock, interfaces, and instrumentation.
- The report states what the kernel result does—and does not—imply for a complete model or product.

### Explicit Non-Goals

- ASIC tape-out or production silicon projections presented as measurements.
- Full-model 7B–9B deployment unless independently achieved and documented.
- Product battery-life or thermal certification.
- Quality parity inferred from arithmetic correctness alone.

## Stage 3+ — Conditional Research

Only after Stage 2 evidence: integrated accelerator dataflow, multimodal/speech specialization, safe phone/desktop companions, chiplet/ASIC exploration, and wearable industrial design. Each requires a separate threat model, acceptance criteria, and funding/manufacturing plan.
