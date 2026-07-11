# Pocket Pet AI

Pocket Pet AI is an open research project exploring a private, local-first personal AI companion built around a frozen, low-bit model. The long-term concept combines an ear-worn interface, a pocket compute device, and permissioned phone and desktop companions. This repository starts with a software reference implementation and an evidence-driven path toward FPGA feasibility—not a claim that the custom hardware already exists.

**Live site:** [pocket-pet-ai.vercel.app](https://pocket-pet-ai.vercel.app) · **Whitepaper:** [read online](https://pocket-pet-ai.vercel.app/research)

## What Is Here

- A public landing page explaining the product and research thesis.
- A downloadable technical white paper.
- A Python/`uv` research workspace for model and memory experiments.
- A staged architecture for local inference, memory, speech, and deterministic action authorization.
- CI and contribution rules for reproducible claims.

The detailed thesis is in [`idea.md`](idea.md). Scope and acceptance criteria are in [`docs/stages.md`](docs/stages.md), and system boundaries are in [`docs/architecture.md`](docs/architecture.md).

## Current Status

The project is in **Stage 1: software reference prototype**. Any latency, memory, power, or quality figure on the site or in the paper must be labeled as measured, simulated, estimated, target, or concept. See [`CHANGELOG.md`](CHANGELOG.md) for shipped changes.

## Quick Start

### Website

Requires Node.js `>=22.13.0`.

```bash
npm ci
npm run dev
```

Then open the local URL printed by the development server.

```bash
npm run lint
npm run build
npm test
```

### Research workspace

Requires [`uv`](https://docs.astral.sh/uv/). When `pyproject.toml` is present:

```bash
uv sync --all-extras --dev
uv run pytest
```

See [`agent.tech.md`](agent.tech.md) for the complete command contract.

## Research Stages

- **Stage 1 — Reference system:** run a small, legally redistributable candidate model on commodity hardware; provide a deterministic action-policy demo; benchmark latency, memory, throughput, and quality with complete metadata.
- **Stage 2 — FPGA feasibility:** implement and validate bit-accurate ternary compute and memory-path kernels, synthesize on a named FPGA target, and compare measured kernel results with the Stage 1 baseline without presenting kernel speedup as end-to-end product speedup.
- **Later research:** integrated multimodal models, device companions, ASIC/chiplet exploration, and wearable hardware follow only after the earlier evidence gates.

## Safety and Privacy

The model proposes actions; deterministic software checks permissions, risk, and confirmation requirements before execution. Sensitive actions must require explicit approval. Never use prototype automation with accounts or devices containing irreplaceable data.

Please report vulnerabilities privately as described in [`SECURITY.md`](SECURITY.md).

## Agent Compatibility

Shared instructions are in [`AGENTS.md`](AGENTS.md), with focused notes for [`CODEX.md`](CODEX.md), [`CLAUDE.md`](CLAUDE.md), and [`HERMES.md`](HERMES.md). `CLAUDE.md` is intentionally the only Claude instruction file because case-only duplicate filenames are unsafe across macOS and Linux filesystems.

## Deploying

The public repository is connected to Vercel for production deployment. A successful local or CI build does not prove a deployment succeeded: keep credentials out of Git and verify the production URL after each release.

## Contributing and License

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a change. By contributing, you agree that your work is licensed under the [MIT License](LICENSE).
