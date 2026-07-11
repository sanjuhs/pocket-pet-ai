# Assumptions ledger

This ledger prevents targets from quietly becoming claims.

| ID | Assumption | Type | Validation |
|---|---|---|---|
| A1 | 9B ternary weights use 1.585 ideal bits or 2 physical bits per ordinary weight | Derived / representation choice | Inspect serialized package and metadata |
| A2 | Full frozen model package can fit 2-4 GB | Target | Produce manifest with byte count by tensor class |
| A3 | Batch-one decode streams the effective weight payload approximately once per generated token unless reuse is demonstrated | Conservative model | Compare hardware bytes/token counters with package bytes |
| A4 | Working memory target is 8-16 GB | Product target | Run 32K nominal context plus OS, audio, retrieval and tool workload |
| A5 | 120K context requires a trained compressed KV architecture | Design constraint | Matched-quality architecture evaluation and bytes/token curve |
| A6 | Median endpoint-to-first-audio can be below 450 ms | Stage 1 target | Timestamped causal audio trace, P50/P95/P99 |
| A7 | Nominal active device power can fit 8-15 W | Product target | Rail and wall power across declared duty cycles |
| A8 | FPGA ternary slice can exceed matched software energy efficiency by at least 2x | Stage 2 continuation gate | Identical tensors, precision, batch and system boundary |
| A9 | Typed proposals plus deterministic policy prevent unconfirmed consequential actions | Safety requirement | Replay and adversarial action suite by risk class |
| A10 | A natively trained ternary 7B-9B model can meet the product quality floor | Central research hypothesis | Pre-registered paired language, agent and speech evaluations |

Update an assumption only with a linked experiment artifact and date. Failed assumptions remain in history.
