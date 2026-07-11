"""Render the public evidence graphic from checked-in benchmark artifacts."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import median

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
ML_RESULTS = ROOT / "benchmark-results/reference/ml-reference.json"
OUTPUT = ROOT / "public/product-v1/research/evidence.png"


def main() -> None:
    data = json.loads(ML_RESULTS.read_text())
    ablations = data["experiments"]["dense_ternary_ablation"]
    cache = data["experiments"]["latent_cache"]

    protection: dict[float, list[float]] = defaultdict(list)
    for row in ablations:
        if row["distribution"] == "injected_outliers":
            protection[row["outlier_fraction_actual"] * 100].append(row["output"]["relative_l2"])

    cache_by_latent: dict[int, list[dict]] = defaultdict(list)
    for row in cache:
        cache_by_latent[row["latent_size"]].append(row)

    fig, axes = plt.subplots(1, 2, figsize=(16, 7.4), facecolor="#f7f7f5")
    fig.subplots_adjust(left=0.075, right=0.965, top=0.75, bottom=0.16, wspace=0.25)
    fig.text(0.075, 0.925, "Measured on the software reference.", fontsize=28, weight=520, color="#07101f")
    fig.text(
        0.075,
        0.865,
        "Small random tensors · Apple M4 Pro CPU · three deterministic seeds · July 2026",
        fontsize=12,
        color="#68717d",
    )

    ax = axes[0]
    xs = sorted(protection)
    ys = [median(protection[x]) for x in xs]
    ax.plot(xs, ys, color="#1265f3", linewidth=2.5, marker="o", markersize=7)
    ax.set_title("Protected outliers reduce output error", loc="left", fontsize=17, weight=560, pad=20)
    ax.set_xlabel("weights preserved in FP32 (%)", fontsize=10, color="#68717d", labelpad=14)
    ax.set_ylabel("median relative L2 error", fontsize=10, color="#68717d", labelpad=12)
    ax.set_ylim(0, 1.0)
    for x, y in zip(xs, ys, strict=True):
        if x in (0.0, 1.0009765625, max(xs)):
            ax.annotate(f"{y:.3f}", (x, y), xytext=(0, 11), textcoords="offset points", ha="center", fontsize=9)
    ax.text(
        0,
        -0.24,
        "Injected-outlier stress case. Lower is better.\n"
        "1% protection is a quality escape path, not a language benchmark.",
        transform=ax.transAxes,
        fontsize=9,
        color="#68717d",
        linespacing=1.5,
    )

    ax = axes[1]
    latents = sorted(cache_by_latent)
    ratios = [median([row["compression_ratio"] for row in cache_by_latent[size]]) for size in latents]
    errors = [median([row["reconstruction"]["relative_l2"] for row in cache_by_latent[size]]) for size in latents]
    ax.plot(latents, ratios, color="#07101f", linewidth=2.5, marker="o", markersize=7)
    ax.set_title("Latent width trades payload for fidelity", loc="left", fontsize=17, weight=560, pad=20)
    ax.set_xlabel("latent dimensions", fontsize=10, color="#68717d", labelpad=14)
    ax.set_ylabel("payload reduction vs FP16 K/V (×)", fontsize=10, color="#68717d", labelpad=12)
    ax.set_ylim(0, 56)
    for size, ratio, error in zip(latents, ratios, errors, strict=True):
        ax.annotate(
            f"{ratio:.1f}×\nerror {error:.4f}",
            (size, ratio),
            xytext=(0, 13),
            textcoords="offset points",
            ha="center",
            fontsize=9,
            color="#1265f3" if size == 32 else "#07101f",
        )
    ax.text(
        0,
        -0.24,
        "Tensor payload only; allocator and model overhead excluded.\n"
        "Reconstruction error is measured before attention, not task quality.",
        transform=ax.transAxes,
        fontsize=9,
        color="#68717d",
        linespacing=1.5,
    )

    for ax in axes:
        ax.set_facecolor("#f7f7f5")
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines[["left", "bottom"]].set_color("#aab1ba")
        ax.tick_params(axis="both", colors="#68717d", labelsize=9, length=3)
        ax.grid(False)

    fig.text(
        0.965,
        0.055,
        "Source: benchmark-results/reference/ml-reference.json",
        ha="right",
        fontsize=8,
        color="#8b939d",
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    main()
