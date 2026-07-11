from __future__ import annotations

import torch
from torch import Tensor


class QuantizedLatentCache:
    """Per-layer int8 latent cache with per-token symmetric scales.

    Full keys and values are reconstructed only for the attention operation. This
    models a compressed writable memory tier; production kernels would reconstruct
    tiled K/V directly into SRAM rather than allocating the full tensors at once.
    """

    def __init__(self, num_layers: int):
        self._values: list[Tensor | None] = [None] * num_layers
        self._scales: list[Tensor | None] = [None] * num_layers

    @staticmethod
    def _quantize(values: Tensor) -> tuple[Tensor, Tensor]:
        scale = values.detach().abs().amax(dim=-1, keepdim=True).clamp_min(1e-8) / 127.0
        quantized = torch.round(values / scale).clamp(-127, 127).to(torch.int8)
        return quantized, scale.to(torch.float16)

    def append(self, layer: int, values: Tensor) -> Tensor:
        quantized, scale = self._quantize(values)
        if self._values[layer] is None:
            self._values[layer], self._scales[layer] = quantized, scale
        else:
            self._values[layer] = torch.cat((self._values[layer], quantized), dim=1)
            self._scales[layer] = torch.cat((self._scales[layer], scale), dim=1)
        return self.get(layer, values.dtype)

    def get(self, layer: int, dtype: torch.dtype = torch.float32) -> Tensor:
        values, scales = self._values[layer], self._scales[layer]
        if values is None or scales is None:
            raise IndexError(f"layer {layer} cache is empty")
        return values.to(dtype) * scales.to(dtype)

    def sequence_length(self, layer: int = 0) -> int:
        values = self._values[layer]
        return 0 if values is None else values.shape[1]

    def memory_bytes(self) -> int:
        tensors = [tensor for tensor in (*self._values, *self._scales) if tensor is not None]
        return sum(tensor.numel() * tensor.element_size() for tensor in tensors)

    def fp16_full_kv_bytes(self, config: object) -> int:
        """Equivalent standard FP16 K+V cache size for the current sequence."""
        values = self._values[0]
        batch_size = 0 if values is None else values.shape[0]
        return (
            2
            * config.num_layers
            * batch_size
            * self.sequence_length()
            * config.hidden_size
            * torch.tensor([], dtype=torch.float16).element_size()
        )
