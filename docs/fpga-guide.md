# FPGA feasibility guide

This folder defines a small, testable Stage 2 boundary. It does **not** claim that Pocket Pet AI has run on an FPGA. The current evidence is a bit-accurate Python golden model, deterministic vectors, a synthesizable reference kernel, and an analytical cycle/packing model.

## Why fixed ternary weights may help

A frozen ternary matrix replaces a general multiply with three routes: add the activation, subtract it, or skip it. Two-bit symbols provide a 4x packing ratio versus int8 weights before scales and protected outliers. When one checkpoint is fixed, tiles can be ordered in physical traversal order and held in on-chip or near-compute banks, reducing instruction and address flexibility.

The benefit is conditional. Decoding can remain memory-bound; zeros do not save energy unless the dataflow actually gates them; accumulators and activations still need precision; protected outliers add a side path; and host/DRAM traffic can erase a fast kernel's gain.

## Reproduce the simulated evidence

```bash
uv run pytest tests/fpga
uv run python scripts/run_fpga_simulation.py
```

The generated `benchmark-results/fpga-sim/reference.json` includes the seed, activations, packed two-bit weights, protected sidecar, exact integer outputs, and lane-count sweeps. The RTL encoding is `00=skip`, `01=add`, `10=subtract`, and `11=reserved`.

## What the result proves

- Packing round-trips without ambiguity and rejects the reserved symbol.
- Routed add/subtract/skip arithmetic exactly matches integer matrix multiplication for the checked vector.
- The protected sidecar exactly adds sparse higher-precision deltas.
- Accumulator saturation and cycle accounting have executable regression tests.

It does not prove timing closure, FPGA resource use, board power, tokens per second, model quality, or end-to-end latency. No supported RTL simulator or synthesis tool was available on the measurement host.

## Board acceptance gates

1. Run the checked-in vectors through RTL simulation and require bit-exact outputs.
2. Synthesize for one named FPGA and publish tool version, clock constraint, LUT/DSP/BRAM/URAM use, and timing slack.
3. Measure the kernel on board, including DMA and stalls, then report joules and bytes per output—not only peak operations.
4. Reproduce representative transformer layers against the PyTorch emulator with an explicit error budget.
5. Integrate latent-KV reads and the protected sidecar before making end-to-end claims.
6. Compare against an optimized dense or 4-bit baseline on the same board and power-measurement setup.

Only after these gates pass should the project discuss FPGA acceleration as measured evidence.
