# Repository Agent Guide

This file is the shared source of truth for Codex, Claude, Hermes, and human contributors. Tool-specific files may add usage notes, but must not contradict this file.

## Mission

Build an open, evidence-led proof of concept for a private, local-first personal AI companion and investigate whether a frozen, low-bit model can be accelerated with model-specific hardware.

This repository is research software, not a finished medical, safety, or consumer device. Treat latency, memory, power, accuracy, and silicon projections as hypotheses until reproduced by a checked-in benchmark.

## Read First

1. `idea.md` for the product thesis.
2. `docs/stages.md` for scope and acceptance criteria.
3. `docs/architecture.md` for system boundaries and safety controls.
4. `agent.tech.md` for commands and repository conventions.
5. `CONTRIBUTING.md` before changing code or claims.

## Non-Negotiable Boundaries

- Never describe a simulation, estimate, mock, or UI animation as measured hardware performance.
- Never claim an FPGA or ASIC exists unless reproducible implementation evidence is committed.
- Keep model output advisory. A deterministic policy layer must authorize tool and device actions.
- Require explicit user confirmation for sending messages, purchases, deletion, security changes, location sharing, or other consequential actions.
- Default to local processing and least privilege. Do not commit personal data, credentials, model tokens, model weights, generated caches, or private recordings.
- Record model name, revision, quantization, prompt/config, hardware, software versions, warm-up, sample count, and measurement method with benchmark results.
- Do not silently replace real execution with fixtures. Tests may use fixtures, but must label them as such.
- Prefer small, reviewable changes. Preserve unrelated user work in a dirty tree.
- Use `uv` for Python environments and dependencies; do not hand-maintain a second pip workflow.
- Use the checked-in npm lockfile with `npm ci` in CI.

## Stage Discipline

- Stage 1 is a software reference system and benchmark harness on commodity hardware. It may simulate the future puck, but must say so.
- Stage 2 is an FPGA-oriented, bit-accurate kernel and system feasibility prototype. Stage 2 begins only after the Stage 1 benchmark contract is stable.
- ASIC/tape-out, a wearable product, unrestricted phone control, 7B–9B real-time performance, and all-day battery life are future research directions—not current repository capabilities.

## Agent Roles

- **Codex:** repository integration, implementation, tests, build health, and evidence-backed review.
- **Claude:** architecture critique, long-form technical writing, assumptions audit, and cross-document consistency.
- **Hermes:** bounded experiments, benchmark runs, dataset/model inventory, and structured result capture.

These are defaults, not silos. Any agent may work across roles, but one agent owns each file during parallel work. Agents must announce overlapping file edits before making them.

## Completion Checklist

- Run the relevant checks from `agent.tech.md`.
- Update tests and documentation with behavior changes.
- Update `CHANGELOG.md` under `Unreleased` for user-visible changes.
- Link every numerical public claim to either a reproducible result or an explicitly labeled estimate.
- Report skipped checks and the reason.

## Case-Sensitive Agent Files

`CLAUDE.md` is canonical. The default macOS filesystem treats `CLAUDE.md` and `claude.md` as the same path, while Linux may treat them as different files. Do not add a second lowercase-only copy: it can diverge and causes cross-platform checkout problems. Tools configured with `claude.md` should be pointed to `CLAUDE.md`.
