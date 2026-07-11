# Pocket Pet AI research library

> **16 primary sources · 7 engineering decisions · verified 2026-07-11**

This directory is a small, decision-oriented reading set for the frozen-model accelerator thesis. It is not an exhaustive bibliography and it is not evidence that the proposed product or FPGA exists.

| Track | Question it helps answer | Sources |
|---|---|---:|
| `01-ternary-llms` | Can ternary weights be trained and executed usefully? | 3 |
| `02-mixed-precision-outliers` | Which values may need protected precision? | 2 |
| `03-kv-cache-attention` | How can decode-time memory traffic be reduced? | 4 |
| `04-decoding` | How can sequential decoding steps be amortized? | 2 |
| `05-fpga-accelerators` | What does a reproducible low-bit FPGA study require? | 2 |
| `06-memory-energy` | Is a kernel compute-bound or bandwidth-bound? | 1 |
| `07-agent-safety` | How should tool-using behavior be evaluated and governed? | 2 |

Start with the [annotated research guide](../../docs/research-guide.md). File integrity and provenance are recorded in [MANIFEST.csv](./MANIFEST.csv).

## Evidence boundary

- Results in a source apply to that source's models, tasks, hardware, software, and measurement method.
- A CPU kernel result is not an FPGA result; an FPGA CNN result is not a transformer result; and a kernel result is not an end-to-end product result.
- Ternary weights do not make attention, activations, normalization, KV traffic, host transfer, audio, or policy enforcement free.
- Public accessibility does not place a paper in the public domain. Each PDF remains under its authors' or publisher's terms; the repository's MIT license does not relicense it.

## Verification

Every PDF in this directory was opened with Poppler `pdfinfo`, its first page was rendered with `pdftoppm` and visually inspected, and its SHA-256 digest was recorded on 2026-07-11. Re-run:

```bash
find research/papers -type f -name '*.pdf' -print0 | sort -z \
  | xargs -0 -n1 sh -c 'pdfinfo "$0" >/dev/null'
shasum -a 256 research/papers/*/*.pdf
```

