# Claude Working Notes

Follow `AGENTS.md` first. This file adds Claude-specific emphasis without redefining repository policy.

## Best-Fit Work

- Challenge architecture assumptions and identify missing evidence.
- Edit the white paper for internal consistency, traceable claims, and clear separation of measurements, estimates, and aspirations.
- Compare design options using explicit constraints: quality, latency, memory bandwidth, energy, programmability, and engineering cost.
- Produce design records or issue proposals before broad architectural changes.

## Review Questions

Before accepting technical prose or architecture, ask:

1. Is this implemented, simulated, measured, estimated, or proposed?
2. Can another contributor reproduce the result from the repository?
3. Are the baseline and experimental configurations comparable?
4. Does the action path enforce permissions outside the model?
5. Does the design acknowledge platform restrictions, especially on iOS?
6. Is a hardware speedup claim end-to-end, or only a kernel projection?

## File Naming

This uppercase `CLAUDE.md` is canonical. Do not create a separate `claude.md`; see `AGENTS.md` for the cross-platform rationale.
