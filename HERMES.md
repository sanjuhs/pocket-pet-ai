# Hermes Working Notes

Follow `AGENTS.md` first.

## Best-Fit Work

- Run bounded model and kernel experiments from written configurations.
- Capture raw results and concise structured summaries.
- Inventory candidate models and licenses before downloading weights.
- Re-run benchmarks to test variance and regressions.

## Experiment Contract

Every result must include model identifier and immutable revision when available, quantization, task/data, hardware, operating system, runtime versions, command/config, warm-up, sample count, summary statistics, and known limitations. Separate generated or synthetic inputs from real-world evaluation data. Do not commit restricted datasets or large model artifacts.
