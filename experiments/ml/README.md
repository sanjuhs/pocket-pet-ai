# ML reference experiments

This folder defines the bounded Stage 1 experiments run by
`scripts/run_ml_experiments.py`. They use seeded random tensors and the tiny,
randomly initialized Pocket Pet transformer. They test implementation mechanics;
they do **not** measure language quality, a trained checkpoint, an FPGA, or an ASIC.

The harness covers:

- dense-versus-ternary weight and output error;
- protected-outlier fraction ablations;
- int8 latent-cache reconstruction error and byte reduction;
- causal-prefix invariance and cached incremental equivalence;
- tensor-level cache memory accounting; and
- CPU timing of dense PyTorch linear algebra versus the readable ternary emulator.

Run from the repository root:

```bash
uv run python scripts/run_ml_experiments.py
```

The command writes a detailed JSON record and a tidy CSV table to
`benchmark-results/reference/`. The committed reference output was measured on
the machine identified inside the JSON. Re-run it on every target machine; do not
generalize its timing to hardware that was not tested.
