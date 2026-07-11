from __future__ import annotations

import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F


def ternary_decompose(weight: Tensor, outlier_fraction: float = 0.01) -> tuple[Tensor, Tensor, Tensor, Tensor]:
    """Split a weight matrix into ternary bulk values and exact protected outliers.

    The returned tensors satisfy ``reconstructed = ternary * scale + protected``.
    Quantization is symmetric per output channel; the largest global magnitudes take
    the protected path. The prototype computes this decomposition during inference,
    while an FPGA export would materialize the symbols, scales, masks and outliers.
    """
    if weight.ndim != 2:
        raise ValueError("weight must be a matrix")
    if not 0 <= outlier_fraction < 1:
        raise ValueError("outlier_fraction must be in [0, 1)")

    protected_mask = torch.zeros_like(weight, dtype=torch.bool)
    protected_count = math.ceil(weight.numel() * outlier_fraction)
    if protected_count:
        indices = weight.detach().abs().flatten().topk(protected_count, sorted=False).indices
        protected_mask.view(-1)[indices] = True

    bulk = weight.masked_fill(protected_mask, 0.0)
    nonzero_count = (~protected_mask).sum(dim=1, keepdim=True).clamp_min(1)
    scale = bulk.abs().sum(dim=1, keepdim=True) / nonzero_count
    scale = scale.clamp_min(torch.finfo(weight.dtype).eps)
    # BitNet-style magnitude threshold; zeros create useful structured skipping.
    threshold = 0.7 * scale
    ternary = torch.where(
        bulk > threshold,
        torch.ones_like(bulk),
        torch.where(bulk < -threshold, -torch.ones_like(bulk), torch.zeros_like(bulk)),
    )
    protected = weight * protected_mask
    return ternary, scale, protected, protected_mask


class TernaryLinear(nn.Linear):
    """Linear layer using a ternary bulk path plus sparse FP32 protected weights."""

    def __init__(self, in_features: int, out_features: int, bias: bool = False, outlier_fraction: float = 0.01):
        super().__init__(in_features, out_features, bias=bias)
        self.outlier_fraction = outlier_fraction

    def quantized_components(self) -> tuple[Tensor, Tensor, Tensor, Tensor]:
        return ternary_decompose(self.weight, self.outlier_fraction)

    def forward(self, inputs: Tensor) -> Tensor:
        ternary, scale, protected, _ = self.quantized_components()
        bulk = F.linear(inputs, ternary, None) * scale.squeeze(-1)
        return bulk + F.linear(inputs, protected, self.bias)

    def storage_bits(self) -> dict[str, int]:
        """Theoretical frozen export cost; masks are implicit in the 2-bit symbols."""
        _, scale, protected, mask = self.quantized_components()
        return {
            "ternary_symbols": 2 * self.weight.numel(),
            "scales": 16 * scale.numel(),
            "protected_values": 16 * int(mask.sum().item()),
            "protected_indices": 32 * int(mask.sum().item()),
            "fp32_baseline": 32 * self.weight.numel(),
            "zeros": int((protected == 0).sum().item()),
        }
