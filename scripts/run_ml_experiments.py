#!/usr/bin/env python3
"""Run bounded, reproducible Stage 1 ML mechanics experiments.

This is deliberately a software-reference harness. PyTorch expands ternary
symbols to ordinary tensors and therefore does not model FPGA timing or energy.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import platform
import statistics
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch import Tensor
from torch.nn import functional as F

from pocket_pet import PocketPetConfig, PocketPetTransformer
from pocket_pet.cache import QuantizedLatentCache
from pocket_pet.model import synchronize
from pocket_pet.quantization import TernaryLinear, ternary_decompose

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "benchmark-results/reference/ml-reference.json"
DEFAULT_CSV = ROOT / "benchmark-results/reference/ml-reference.csv"
SEEDS = (7, 17, 29)


def tensor_metrics(actual: Tensor, reference: Tensor) -> dict[str, float]:
    difference = (actual.float() - reference.float()).flatten()
    reference_flat = reference.float().flatten()
    denominator = torch.linalg.vector_norm(reference_flat).clamp_min(1e-12)
    return {
        "rmse": float(torch.sqrt(torch.mean(difference.square())).item()),
        "relative_l2": float((torch.linalg.vector_norm(difference) / denominator).item()),
        "max_abs": float(difference.abs().max().item()),
        "cosine_similarity": float(F.cosine_similarity(actual.float().flatten(), reference_flat, dim=0).item()),
    }


def dense_ternary_ablation() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for seed in SEEDS:
        generator = torch.Generator().manual_seed(seed)
        inputs = torch.randn(256, 128, generator=generator)
        base_weight = torch.randn(128, 128, generator=generator) / math.sqrt(128)
        for distribution in ("gaussian", "injected_outliers"):
            weight = base_weight.clone()
            if distribution == "injected_outliers":
                count = math.ceil(weight.numel() * 0.01)
                indices = weight.abs().flatten().topk(count).indices
                weight.view(-1)[indices] *= 8.0
            dense_output = F.linear(inputs, weight)
            for fraction in (0.0, 0.005, 0.01, 0.02, 0.05):
                ternary, scale, protected, mask = ternary_decompose(weight, fraction)
                reconstructed = ternary * scale + protected
                quantized_output = F.linear(inputs, ternary) * scale.squeeze(-1) + F.linear(inputs, protected)
                rows.append(
                    {
                        "seed": seed,
                        "distribution": distribution,
                        "outlier_fraction_requested": fraction,
                        "outlier_fraction_actual": float(mask.float().mean().item()),
                        "zero_symbol_fraction": float((ternary == 0).float().mean().item()),
                        "frozen_export_bits_estimate": (
                            2 * weight.numel() + 16 * weight.shape[0] + 48 * int(mask.sum().item())
                        ),
                        "fp32_weight_bits": 32 * weight.numel(),
                        "weight_storage_compression_estimate": (32 * weight.numel())
                        / (2 * weight.numel() + 16 * weight.shape[0] + 48 * int(mask.sum().item())),
                        "weight": tensor_metrics(reconstructed, weight),
                        "output": tensor_metrics(quantized_output, dense_output),
                    }
                )
    return rows


def ternary_integer_identity_experiment() -> list[dict[str, Any]]:
    """Check the add/subtract identity using integer arithmetic only."""
    rows = []
    for seed in SEEDS:
        generator = torch.Generator().manual_seed(seed)
        activations = torch.randint(-127, 128, (32, 128), generator=generator, dtype=torch.int32)
        symbols = torch.randint(-1, 2, (64, 128), generator=generator, dtype=torch.int32)
        matrix_product = activations @ symbols.T
        routed = torch.stack(
            [
                activations[:, output_symbols == 1].sum(dim=1) - activations[:, output_symbols == -1].sum(dim=1)
                for output_symbols in symbols
            ],
            dim=1,
        )
        difference = matrix_product - routed
        maximum = int(matrix_product.abs().max().item())
        rows.append(
            {
                "seed": seed,
                "activation_shape": list(activations.shape),
                "weight_shape": list(symbols.shape),
                "mismatched_outputs": int((difference != 0).sum().item()),
                "max_abs_difference": int(difference.abs().max().item()),
                "observed_max_abs_accumulator": maximum,
                "observed_signed_accumulator_bits": math.ceil(math.log2(maximum + 1)) + 1,
                "worst_case_bound": 127 * activations.shape[1],
                "worst_case_signed_accumulator_bits": math.ceil(math.log2(127 * activations.shape[1] + 1)) + 1,
            }
        )
    return rows


def latent_cache_experiment() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    hidden_size, tokens = 128, 128
    for seed in SEEDS:
        generator = torch.Generator().manual_seed(seed)
        for latent_size in (8, 16, 32, 64):
            source = torch.randn(1, tokens, latent_size, generator=generator)
            cache = QuantizedLatentCache(1)
            restored = cache.append(0, source)
            actual_bytes = cache.memory_bytes()
            expected_bytes = tokens * (latent_size + 2)
            dense_fp16_bytes = tokens * 2 * hidden_size * 2
            rows.append(
                {
                    "seed": seed,
                    "tokens": tokens,
                    "hidden_size": hidden_size,
                    "latent_size": latent_size,
                    "actual_bytes": actual_bytes,
                    "expected_bytes": expected_bytes,
                    "fp16_full_kv_bytes": dense_fp16_bytes,
                    "compression_ratio": dense_fp16_bytes / actual_bytes,
                    "reconstruction": tensor_metrics(restored, source),
                }
            )
    return rows


def causal_experiment() -> dict[str, Any]:
    torch.manual_seed(101)
    config = PocketPetConfig(
        vocab_size=64,
        hidden_size=32,
        intermediate_size=64,
        num_layers=2,
        num_heads=4,
        latent_size=8,
        max_sequence_length=32,
        outlier_fraction=0.01,
    )
    model = PocketPetTransformer(config).eval()
    tokens = torch.tensor([[1, 5, 9, 2, 12, 7, 3, 11]])
    prefix_length = 5
    with torch.inference_mode():
        prefix_logits = model(tokens[:, :prefix_length])
        extended_prefix_logits = model(tokens)[:, :prefix_length]

        one_shot_cache = QuantizedLatentCache(config.num_layers)
        one_shot_logits = model(tokens, one_shot_cache)
        incremental_cache = QuantizedLatentCache(config.num_layers)
        incremental_logits = torch.cat(
            [model(tokens[:, position : position + 1], incremental_cache) for position in range(tokens.shape[1])],
            dim=1,
        )
    return {
        "seed": 101,
        "tokens": tokens.shape[1],
        "prefix_tokens": prefix_length,
        "future_independence": tensor_metrics(extended_prefix_logits, prefix_logits),
        "one_shot_vs_incremental_quantized_cache": tensor_metrics(incremental_logits, one_shot_logits),
        "one_shot_cache_bytes": one_shot_cache.memory_bytes(),
        "incremental_cache_bytes": incremental_cache.memory_bytes(),
    }


def memory_accounting_experiment() -> list[dict[str, Any]]:
    config = PocketPetConfig()
    rows: list[dict[str, Any]] = []
    generator = torch.Generator().manual_seed(43)
    for tokens in (1, 32, 128, 512):
        cache = QuantizedLatentCache(config.num_layers)
        for layer in range(config.num_layers):
            cache.append(layer, torch.randn(1, tokens, config.latent_size, generator=generator))
        actual = cache.memory_bytes()
        latent_formula = config.num_layers * tokens * (config.latent_size + 2)
        full_formula = config.num_layers * tokens * 2 * config.hidden_size * 2
        rows.append(
            {
                "tokens": tokens,
                "layers": config.num_layers,
                "hidden_size": config.hidden_size,
                "latent_size": config.latent_size,
                "actual_latent_bytes": actual,
                "formula_latent_bytes": latent_formula,
                "formula_matches": actual == latent_formula,
                "fp16_full_kv_bytes": cache.fp16_full_kv_bytes(config),
                "formula_fp16_full_kv_bytes": full_formula,
                "cache_compression_ratio": full_formula / actual,
            }
        )
    return rows


def percentile(samples: list[float], quantile: float) -> float:
    return float(np.quantile(np.asarray(samples), quantile))


def time_callable(function: Any, device: torch.device, warmup: int, samples: int) -> dict[str, Any]:
    for _ in range(warmup):
        function()
    synchronize(device)
    durations = []
    for _ in range(samples):
        start = time.perf_counter_ns()
        function()
        synchronize(device)
        durations.append((time.perf_counter_ns() - start) / 1_000_000)
    return {
        "warmup_iterations": warmup,
        "samples": samples,
        "median_ms": statistics.median(durations),
        "p10_ms": percentile(durations, 0.10),
        "p90_ms": percentile(durations, 0.90),
        "min_ms": min(durations),
        "max_ms": max(durations),
    }


def timing_experiment(device: torch.device, samples: int) -> list[dict[str, Any]]:
    torch.manual_seed(71)
    inputs = torch.randn(256, 128, device=device)
    layer = TernaryLinear(128, 128, outlier_fraction=0.01).eval().to(device)
    weight = layer.weight.detach().clone()
    with torch.inference_mode():
        dense = time_callable(lambda: F.linear(inputs, weight), device, warmup=5, samples=samples)
        emulator = time_callable(lambda: layer(inputs), device, warmup=5, samples=samples)
    return [
        {
            "operation": "dense_fp32_linear",
            "shape": "[256,128]x[128,128]",
            "device": str(device),
            **dense,
        },
        {
            "operation": "dynamic_ternary_emulator",
            "shape": "[256,128]x[128,128]",
            "device": str(device),
            **emulator,
        },
    ]


def git_metadata() -> dict[str, Any]:
    def run(*args: str) -> str:
        return subprocess.run(args, cwd=ROOT, check=False, capture_output=True, text=True).stdout.strip()

    return {
        "commit": run("git", "rev-parse", "HEAD"),
        "working_tree_dirty": bool(run("git", "status", "--porcelain")),
    }


def machine_metadata(device: torch.device, command: str) -> dict[str, Any]:
    cpu_model = platform.processor() or "not reported by Python"
    physical_memory_bytes: int | str = "not reported"
    if platform.system() == "Darwin":
        cpu_query = subprocess.run(
            ("sysctl", "-n", "machdep.cpu.brand_string"), check=False, capture_output=True, text=True
        ).stdout.strip()
        memory_query = subprocess.run(
            ("sysctl", "-n", "hw.memsize"), check=False, capture_output=True, text=True
        ).stdout.strip()
        cpu_model = cpu_query or cpu_model
        physical_memory_bytes = int(memory_query) if memory_query.isdigit() else physical_memory_bytes
    return {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "command": command,
        "python": platform.python_version(),
        "torch": torch.__version__,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": cpu_model,
        "physical_memory_bytes": physical_memory_bytes,
        "logical_cpu_count": os.cpu_count(),
        "device": str(device),
        "mps_available": torch.backends.mps.is_available(),
        "random_seeds": list(SEEDS),
        "git": git_metadata(),
    }


def flatten_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    flattened: list[dict[str, Any]] = []

    def add(experiment: str, record: dict[str, Any]) -> None:
        row: dict[str, Any] = {"experiment": experiment}
        for key, value in record.items():
            if isinstance(value, dict):
                row.update({f"{key}_{nested_key}": nested_value for nested_key, nested_value in value.items()})
            else:
                row[key] = value
        flattened.append(row)

    for name in (
        "dense_ternary_ablation",
        "ternary_integer_identity",
        "latent_cache",
        "memory_accounting",
        "timing",
    ):
        for record in report["experiments"][name]:
            add(name, record)
    add("causal_equivalence", report["experiments"]["causal_equivalence"])
    return flattened


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = ["experiment"] + sorted({key for row in rows for key in row if key != "experiment"})
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("cpu", "mps"), default="cpu")
    parser.add_argument("--timing-samples", type=int, default=30)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--csv-output", type=Path, default=DEFAULT_CSV)
    args = parser.parse_args()
    if args.timing_samples < 5:
        parser.error("--timing-samples must be at least 5")
    if args.device == "mps" and not torch.backends.mps.is_available():
        parser.error("MPS is not available")

    device = torch.device(args.device)
    command = (
        f"uv run python scripts/run_ml_experiments.py --device {args.device} --timing-samples {args.timing_samples}"
    )
    report = {
        "schema_version": 1,
        "status": "measured_software_reference",
        "scope": (
            "Seeded random tensors and a randomly initialized tiny transformer. "
            "No pretrained model, language-quality task, FPGA, ASIC, energy meter, or packed ternary kernel was tested."
        ),
        "method": {
            "weights": "128x128 FP32 matrices; 256 FP32 input vectors; symmetric per-row ternarization",
            "outliers": "global top absolute-magnitude weights protected exactly in FP32 compute",
            "cache": "per-token symmetric int8 latent with one FP16 scale",
            "timing": "perf_counter_ns wall clock after five warm-up iterations; synchronization after every sample",
        },
        "environment": machine_metadata(device, command),
        "experiments": {
            "dense_ternary_ablation": dense_ternary_ablation(),
            "ternary_integer_identity": ternary_integer_identity_experiment(),
            "latent_cache": latent_cache_experiment(),
            "causal_equivalence": causal_experiment(),
            "memory_accounting": memory_accounting_experiment(),
            "timing": timing_experiment(device, args.timing_samples),
        },
        "interpretation_guardrail": (
            "Timing measures the readable PyTorch emulator, which re-ternarizes weights on every call. "
            "It is not a projection of packed kernels or FPGA/ASIC performance."
        ),
    }
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_csv(args.csv_output, flatten_rows(report))
    print(json.dumps({"json": str(args.json_output), "csv": str(args.csv_output)}, indent=2))


if __name__ == "__main__":
    main()
