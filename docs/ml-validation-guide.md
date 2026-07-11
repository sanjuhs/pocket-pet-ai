# ML validation guide

## What this evidence establishes

The checked-in Stage 1 harness exercises real PyTorch tensor operations in the
Pocket Pet reference transformer. It is designed to answer narrow engineering
questions before a packed kernel or FPGA exists:

1. How much numerical error does the current per-row ternary rule introduce on
   seeded synthetic matrices?
2. Does protecting a small fixed set of large weights reduce error, especially
   when the weight distribution has unusually large values?
3. What reconstruction error and tensor-payload reduction result from the int8
   latent cache?
4. Does the attention implementation preserve causal prefixes, and does
   token-at-a-time cached execution agree with one-shot cached execution?
5. Does the cache's allocated tensor payload exactly match its documented byte
   formula?
6. How expensive is the readable dynamic-quantization emulator on this CPU?

The committed outputs live in
[`benchmark-results/reference/ml-reference.json`](../benchmark-results/reference/ml-reference.json)
and
[`benchmark-results/reference/ml-reference.csv`](../benchmark-results/reference/ml-reference.csv).
The JSON is canonical; CSV is provided for plotting and spreadsheet analysis.

## Committed reference observations

The July 11, 2026 CPU run on an Apple M4 Pro with 48 GiB physical memory produced
the following bounded observations (three seeds unless stated otherwise):

- On Gaussian matrices, median output relative-L2 error moved from `0.5231` with
  no protected weights to `0.4859` at a one-percent protected fraction and
  `0.4109` at five percent. The corresponding frozen-weight storage estimate
  moved from `15.06×` to `12.28×` and `7.07×` versus FP32, exposing the quality /
  storage tradeoff rather than hiding it.
- After multiplying the largest one percent of weights by eight, median output
  relative-L2 error moved from `0.8975` with no protection to `0.1934` at one
  percent. This supports the protected-path mechanism for this synthetic stress
  test; it does not establish the correct budget for a trained model.
- Int8 latent reconstruction had median relative-L2 error from `0.0040` to
  `0.0059` across latent widths 8–64. Payload ratios versus width-128 FP16 K/V
  ranged from `51.2×` (latent width 8) to `7.76×` (latent width 64); the default
  width 32 ratio was `15.06×`.
- Causal-prefix relative-L2 error was `6.36e-8`, and one-shot versus incremental
  cached execution error was `4.63e-8`, within floating-point noise for this
  seeded tiny random model.
- Actual cache tensor payload matched the formula at all tested lengths. At the
  default dimensions it was 52,224 bytes for 512 tokens versus a 786,432-byte
  FP16 K/V baseline, again `15.06×`.
- Across three seeds, integer ternary matrix multiplication exactly matched an
  explicit sum-of-positive-routes minus sum-of-negative-routes implementation.
  This validates the arithmetic identity on these vectors, not an FPGA circuit.
- Median `128 × 128` linear timing for 256 input rows was 0.00990 ms for dense
  PyTorch and 0.12392 ms for the dynamic ternary emulator. The emulator was about
  12.5× slower because it decomposes weights on every call; this is evidence
  against using the readable implementation as a performance claim.

These numbers are copied from the linked JSON and should be updated whenever the
committed reference output is regenerated.

## Reproduce it

From the repository root:

```bash
uv sync
uv run python scripts/run_ml_experiments.py --device cpu --timing-samples 30
uv run pytest
uv run ruff check src tests/python scripts/run_ml_experiments.py
```

The run records Python, PyTorch, NumPy, operating-system, device, Git revision,
dirty-tree state, seeds, warm-up count, sample count, and timing method. Timing
will vary with thermals, background load, and software versions. Compare numerical
metrics across systems; treat latency as machine-local.

## Reading the experiments

### Dense versus ternary and outlier protection

Each row uses a `128 × 128` FP32 matrix and 256 FP32 input vectors. The bulk
matrix is quantized to `{-1, 0, +1}` with one FP32 scale per output row. A selected
global fraction of the largest-magnitude weights is removed from the bulk and
added back exactly by the protected path. The harness reports weight and output
RMSE, relative L2 error, maximum absolute error, cosine similarity, and a frozen
export storage estimate. That estimate follows the prototype format (two bits per
symbol, FP16 row scales and protected values, 32-bit protected indices), while
this readable PyTorch compute path adds protected values in FP32.

Two synthetic distributions are measured: ordinary Gaussian weights and the same
weights after the largest one percent are multiplied by eight. Multiple seeds
keep a single favorable draw from driving the conclusion. The ablation is useful
for choosing a candidate outlier budget, but it cannot choose the final budget:
that requires a trained checkpoint and downstream quality evaluation.

### Latent-cache reconstruction

Random latent vectors are quantized independently per token to int8 using one
FP16 scale. Latent sizes 8, 16, 32, and 64 are compared with a conventional
two-tensor FP16 K/V baseline at hidden width 128. The reported compression is
tensor payload only:

```text
latent bytes = layers × batch × tokens × (latent width + 2-byte scale)
FP16 K/V bytes = layers × batch × tokens × 2 × hidden width × 2 bytes
```

Allocator metadata, temporary dequantized tensors, K/V up-projection workspace,
and model weights are excluded. Those must be measured separately in a deployment
kernel. The experiment measures latent reconstruction, not attention-output or
task-quality degradation from a trained latent-attention model.

### Causality and cached execution

The future-independence check compares logits for a five-token prefix alone with
the same five positions inside a longer sequence. The incremental check compares
one-shot quantized-cache inference with token-at-a-time inference using the same
cache format. Near-floating-point-noise error supports the implementation
invariant; it is not evidence of language ability.

### Memory accounting

For 1, 32, 128, and 512 tokens, the harness compares actual `numel × element_size`
over the stored tensors with the closed-form formula above. This validates payload
bookkeeping. It does not measure peak resident memory because the current PyTorch
attention path materializes dequantized latents and expanded K/V tensors.

### Timing

The dense and ternary measurements use the same input and weight shapes. The
ternary layer currently finds outliers and reconstructs its execution tensors on
every call. That readable implementation is expected to be slower than a highly
optimized dense kernel. Its latency is a regression baseline for software only.

An FPGA hypothesis becomes testable only after export freezes symbols, scales,
protected indices/values, tiling, accumulator precision, and golden vectors. FPGA
claims then require synthesis reports plus on-board latency, throughput, power,
and external-memory traffic measurements. None of those are produced here.

## What these results do not show

- No pretrained or fine-tuned model was evaluated, so there is no claim about
  perplexity, task accuracy, speech quality, tool-use reliability, or safety.
- No packed ternary CPU/GPU kernel was timed.
- No FPGA bitstream, synthesis, place-and-route, timing closure, board, power
  meter, or energy measurement was used.
- Compression ratios are representation and tensor-payload ratios, not measured
  end-to-end process-memory reductions.
- Random small matrices do not establish that a 7B–9B model will preserve quality
  at the same outlier fraction.
- The experiments do not validate a consumer puck's thermals, battery life, or
  real-time conversational latency.

## Next evidence gates

1. Freeze a small pretrained checkpoint and record its exact model ID, revision,
   tokenizer, evaluation set, and license.
2. Evaluate dense, ternary-only, and protected-outlier variants on perplexity and
   at least one task metric with confidence intervals.
3. Train latent attention end-to-end, then compare attention outputs and quality
   across context lengths rather than quantizing an untrained latent alone.
4. Export packed two-bit symbols and implement a CPU golden kernel that consumes
   the exact planned hardware layout.
5. Define fixed-point accumulator formats and compare every layer against golden
   vectors before FPGA synthesis.
6. Measure peak memory and memory traffic with platform profilers; measure energy
   with external instrumentation.
