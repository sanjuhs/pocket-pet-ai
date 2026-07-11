import numpy as np
import pytest

from fpga.reference_model import estimate_mvu, pack_ternary, saturate_signed, ternary_mvu, unpack_ternary


def test_pack_round_trip_and_reserved_symbol() -> None:
    values = np.array([-1, 0, 1, 1, 0, -1, 1], dtype=np.int8)
    assert np.array_equal(unpack_ternary(pack_ternary(values), len(values)), values)
    with pytest.raises(ValueError, match="reserved"):
        unpack_ternary(bytes([0b11]), 1)


def test_mvu_matches_dense_and_protected_sidecar() -> None:
    x = np.array([4, -3, 7, 2], dtype=np.int8)
    weights = np.array([[1, 0, -1, 1], [-1, 1, 0, 0]], dtype=np.int8)
    result = ternary_mvu(x, weights, protected=[(1, 2, 3)])
    expected = weights.astype(np.int64) @ x.astype(np.int64)
    expected[1] += x[2] * 3
    assert np.array_equal(result, expected)


def test_saturation_and_analytical_contract() -> None:
    assert saturate_signed(np.array([-999, -3, 3, 999]), 4).tolist() == [-8, -3, 3, 7]
    estimate = estimate_mvu(outputs=16, inputs=64, lanes=8)
    assert estimate.cycles == 128
    assert estimate.packing_ratio == 4.0
    assert estimate.operations_per_cycle == 8.0
