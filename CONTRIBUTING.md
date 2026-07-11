# Contributing

Thank you for helping make local AI research more reproducible and honest.

## Before You Start

- Read `AGENTS.md`, `docs/stages.md`, and `docs/architecture.md`.
- For substantial changes, open an issue describing scope, evidence, and affected interfaces.
- Keep pull requests focused. Do not combine a visual redesign, model change, and benchmark-method change without a clear reason.
- Confirm that every dependency, dataset, model, image, and paper excerpt can legally be used and redistributed as proposed.

## Development

```bash
npm ci
npm run lint
npm run build
npm test
```

For Python changes, use the repository's `uv` environment:

```bash
uv sync --all-extras --dev
uv run pytest
uv run ruff check .
```

Run only configured commands and explain any skipped check in the pull request.

## Experiments and Claims

A benchmark contribution must include:

- immutable model revision and model license;
- quantization and inference configuration;
- hardware, OS, runtime, and relevant power mode;
- input/task description, warm-up, repetitions, and statistical summary;
- raw machine-readable output or a documented generation path;
- baseline definition and known limitations.

Label numbers as measured, simulated, estimated, target, or concept. Do not compare unlike workloads or report a kernel improvement as an end-to-end system result.

## Pull Requests

- Add or update tests for behavior changes.
- Update documentation and `CHANGELOG.md` under `Unreleased` when users are affected.
- Do not commit secrets, personal information, recordings, model weights, datasets, generated build products, or oversized result files.
- Complete the pull request template and respond to review with evidence.

## Commit Style

Use concise, imperative subjects, for example: `Add KV cache estimator`. Reference issues where useful. Signed commits are welcome but not required.

## Community Expectations

Be precise, constructive, and respectful. Critique methods and evidence, not people. Report conduct concerns privately to the maintainers.
