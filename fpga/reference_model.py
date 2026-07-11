"""Bit-accurate reference functions for the Stage 2 ternary MVU contract."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np

TERNARY_TO_BITS = {0: 0b00, 1: 0b01, -1: 0b10}
BITS_TO_TERNARY = {value: key for key, value in TERNARY_TO_BITS.items()}


def pack_ternary(values: np.ndarray) -> bytes:
    """Pack four {-1, 0, +1} weights into each byte, least-significant first."""
    flat = np.asarray(values, dtype=np.int8).reshape(-1)
    if not np.isin(flat, (-1, 0, 1)).all():
        raise ValueError("ternary weights must be -1, 0, or +1")
    packed = bytearray((len(flat) + 3) // 4)
    for index, value in enumerate(flat):
        packed[index // 4] |= TERNARY_TO_BITS[int(value)] << (2 * (index % 4))
    return bytes(packed)


def unpack_ternary(payload: bytes, count: int) -> np.ndarray:
    """Decode the Stage 2 two-bit format and reject the reserved 0b11 symbol."""
    result = np.empty(count, dtype=np.int8)
    for index in range(count):
        bits = (payload[index // 4] >> (2 * (index % 4))) & 0b11
        if bits not in BITS_TO_TERNARY:
            raise ValueError("reserved ternary symbol 0b11")
        result[index] = BITS_TO_TERNARY[bits]
    return result


def saturate_signed(values: np.ndarray, bits: int) -> np.ndarray:
    if bits < 2:
        raise ValueError("signed accumulator needs at least two bits")
    low, high = -(1 << (bits - 1)), (1 << (bits - 1)) - 1
    return np.clip(values, low, high).astype(np.int64)


def ternary_mvu(
    activations: np.ndarray,
    weights: np.ndarray,
    *,
    accumulator_bits: int = 32,
    protected: list[tuple[int, int, int]] | None = None,
) -> np.ndarray:
    """Compute add/sub/skip MVU output plus sparse (row, column, delta) sidecar."""
    x = np.asarray(activations, dtype=np.int64)
    w = np.asarray(weights, dtype=np.int8)
    if w.ndim != 2 or x.ndim != 1 or w.shape[1] != x.shape[0]:
        raise ValueError("expected weights [outputs, inputs] and matching activation vector")
    if not np.isin(w, (-1, 0, 1)).all():
        raise ValueError("weights must be ternary")
    result = np.zeros(w.shape[0], dtype=np.int64)
    for row in range(w.shape[0]):
        positive = x[w[row] == 1].sum(dtype=np.int64)
        negative = x[w[row] == -1].sum(dtype=np.int64)
        result[row] = positive - negative
    for row, column, delta in protected or []:
        result[row] += x[column] * int(delta)
    return saturate_signed(result, accumulator_bits)


@dataclass(frozen=True)
class MvuEstimate:
    outputs: int
    inputs: int
    lanes: int
    cycles: int
    packed_weight_bytes: int
    dense_int8_weight_bytes: int
    packing_ratio: float
    operations: int
    operations_per_cycle: float


def estimate_mvu(outputs: int, inputs: int, lanes: int) -> MvuEstimate:
    """Deterministic kernel model; excludes clocks, routing, DMA, and board stalls."""
    if min(outputs, inputs, lanes) <= 0:
        raise ValueError("dimensions and lanes must be positive")
    cycles_per_output = (inputs + lanes - 1) // lanes
    cycles = outputs * cycles_per_output
    operations = outputs * inputs
    packed = outputs * ((inputs + 3) // 4)
    return MvuEstimate(
        outputs=outputs,
        inputs=inputs,
        lanes=lanes,
        cycles=cycles,
        packed_weight_bytes=packed,
        dense_int8_weight_bytes=outputs * inputs,
        packing_ratio=(outputs * inputs) / packed,
        operations=operations,
        operations_per_cycle=operations / cycles,
    )


def estimate_dict(outputs: int, inputs: int, lanes: int) -> dict[str, int | float]:
    return asdict(estimate_mvu(outputs, inputs, lanes))
