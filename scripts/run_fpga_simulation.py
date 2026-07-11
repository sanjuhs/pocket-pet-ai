"""Generate Stage 2 golden vectors and an explicitly analytical MVU estimate."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from fpga.reference_model import estimate_dict, pack_ternary, ternary_mvu, unpack_ternary

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "benchmark-results" / "fpga-sim" / "reference.json"


def main() -> None:
    rng = np.random.default_rng(20260711)
    activations = rng.integers(-127, 128, size=64, dtype=np.int16).astype(np.int8)
    weights = rng.choice(np.array([-1, 0, 1], dtype=np.int8), size=(16, 64), p=[0.34, 0.32, 0.34])
    packed = pack_ternary(weights)
    decoded = unpack_ternary(packed, weights.size).reshape(weights.shape)
    protected = [(0, 3, 5), (7, 12, -4)]
    result = ternary_mvu(activations, decoded, protected=protected)
    dense_golden = weights.astype(np.int64) @ activations.astype(np.int64)
    dense_golden[0] += int(activations[3]) * 5
    dense_golden[7] += int(activations[12]) * -4
    if not np.array_equal(result, dense_golden):
        raise RuntimeError("ternary route does not match integer golden output")

    payload = {
        "claim_class": "simulated_reference_and_analytical_estimate",
        "seed": 20260711,
        "golden_vector": {
            "inputs": activations.tolist(),
            "weight_shape": list(weights.shape),
            "packed_weights_hex": packed.hex(),
            "protected_sidecar": protected,
            "outputs": result.tolist(),
            "exact_match": True,
        },
        "kernel_estimates": [estimate_dict(4096, 4096, lanes) for lanes in (8, 32, 128, 512)],
        "limitations": [
            "No RTL simulator or synthesis tool was available on this host.",
            "Cycle counts omit clock frequency, routing, DMA, memory stalls, and protected-path scheduling.",
            "This result is not FPGA-board performance evidence.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(OUTPUT)


if __name__ == "__main__":
    main()
