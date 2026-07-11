# Agent Technical Reference

## Toolchain

- Node.js `>=22.13.0` and npm
- Python version declared by `pyproject.toml`
- `uv` for Python environments, locking, and execution
- Git for version control

## Web Commands

```bash
npm ci
npm run dev
npm run lint
npm run build
npm test
```

`npm test` currently includes a production build. During iteration, run targeted tests where possible, then run the full command before handoff.

## Python Commands

Once `pyproject.toml` is present:

```bash
uv sync --all-extras --dev
uv run pytest
uv run ruff check .
uv run python -m prototype --help
```

Only run commands supported by the current project configuration. If a command is not configured yet, report it as unavailable rather than improvising a second dependency system.

## Notebook Rules

- Keep reusable logic in importable Python modules; notebooks orchestrate and explain it.
- Use deterministic seeds where practical.
- Clear private data and large cell outputs before commit.
- Record the environment and model revision in benchmark notebooks.
- Prefer scripts for CI and repeatable benchmarks.

## Repository Conventions

- TypeScript/React UI lives under `app/`.
- Static public downloads belong under `public/`.
- Python research code, notebooks, and tests follow `pyproject.toml` and their own package layout.
- Architecture and stage contracts live under `docs/`.
- Generated reports must identify their source data and generation command.
- Model weights, caches, datasets, secrets, recordings, FPGA build products, and local benchmark runs are ignored by default.

## Claims Vocabulary

Use one of these labels for performance numbers:

- **Measured:** produced by a reproducible run on identified hardware.
- **Simulated:** produced by a named simulator and configuration.
- **Estimated:** derived analytically; show assumptions.
- **Target:** an engineering goal, not achieved performance.
- **Concept:** a proposed direction without validation.
