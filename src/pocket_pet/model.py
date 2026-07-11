from __future__ import annotations

import time
from dataclasses import asdict

import torch
from torch import Tensor, nn
from torch.nn import functional as F

from .cache import QuantizedLatentCache
from .config import PocketPetConfig
from .quantization import TernaryLinear


class RMSNorm(nn.Module):
    def __init__(self, size: int, eps: float = 1e-5):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(size))
        self.eps = eps

    def forward(self, inputs: Tensor) -> Tensor:
        normalized = inputs * torch.rsqrt(inputs.pow(2).mean(dim=-1, keepdim=True) + self.eps)
        return normalized * self.weight


class LatentCausalAttention(nn.Module):
    def __init__(self, config: PocketPetConfig):
        super().__init__()
        kwargs = {"bias": False, "outlier_fraction": config.outlier_fraction}
        self.num_heads = config.num_heads
        self.head_size = config.head_size
        self.q_proj = TernaryLinear(config.hidden_size, config.hidden_size, **kwargs)
        self.latent_proj = TernaryLinear(config.hidden_size, config.latent_size, **kwargs)
        self.k_up = TernaryLinear(config.latent_size, config.hidden_size, **kwargs)
        self.v_up = TernaryLinear(config.latent_size, config.hidden_size, **kwargs)
        self.out_proj = TernaryLinear(config.hidden_size, config.hidden_size, **kwargs)

    def _heads(self, values: Tensor) -> Tensor:
        batch, sequence, _ = values.shape
        return values.view(batch, sequence, self.num_heads, self.head_size).transpose(1, 2)

    def forward(self, inputs: Tensor, layer: int, cache: QuantizedLatentCache | None) -> Tensor:
        batch, query_length, _ = inputs.shape
        q = self._heads(self.q_proj(inputs))
        current_latent = self.latent_proj(inputs)
        if cache is None:
            latent = current_latent
            past_length = 0
        else:
            past_length = cache.sequence_length(layer)
            latent = cache.append(layer, current_latent)

        k, v = self._heads(self.k_up(latent)), self._heads(self.v_up(latent))
        scores = q @ k.transpose(-2, -1) / self.head_size**0.5
        key_positions = torch.arange(latent.shape[1], device=inputs.device)
        query_positions = torch.arange(past_length, past_length + query_length, device=inputs.device)
        causal = key_positions.unsqueeze(0) <= query_positions.unsqueeze(1)
        scores = scores.masked_fill(~causal.view(1, 1, query_length, -1), torch.finfo(scores.dtype).min)
        attended = F.softmax(scores, dim=-1) @ v
        attended = attended.transpose(1, 2).contiguous().view(batch, query_length, -1)
        return self.out_proj(attended)


class FeedForward(nn.Module):
    def __init__(self, config: PocketPetConfig):
        super().__init__()
        kwargs = {"bias": False, "outlier_fraction": config.outlier_fraction}
        self.gate = TernaryLinear(config.hidden_size, config.intermediate_size, **kwargs)
        self.up = TernaryLinear(config.hidden_size, config.intermediate_size, **kwargs)
        self.down = TernaryLinear(config.intermediate_size, config.hidden_size, **kwargs)

    def forward(self, inputs: Tensor) -> Tensor:
        return self.down(F.silu(self.gate(inputs)) * self.up(inputs))


class TransformerBlock(nn.Module):
    def __init__(self, config: PocketPetConfig):
        super().__init__()
        self.attention_norm = RMSNorm(config.hidden_size)
        self.attention = LatentCausalAttention(config)
        self.ffn_norm = RMSNorm(config.hidden_size)
        self.feed_forward = FeedForward(config)

    def forward(self, inputs: Tensor, layer: int, cache: QuantizedLatentCache | None) -> Tensor:
        inputs = inputs + self.attention(self.attention_norm(inputs), layer, cache)
        return inputs + self.feed_forward(self.ffn_norm(inputs))


class PocketPetTransformer(nn.Module):
    """Tiny causal transformer that emulates the proposed frozen accelerator dataflow."""

    def __init__(self, config: PocketPetConfig | None = None):
        super().__init__()
        config = config or PocketPetConfig()
        self.config = config
        self.token_embedding = nn.Embedding(config.vocab_size, config.hidden_size)
        self.position_embedding = nn.Embedding(config.max_sequence_length, config.hidden_size)
        self.layers = nn.ModuleList(TransformerBlock(config) for _ in range(config.num_layers))
        self.final_norm = RMSNorm(config.hidden_size)
        self.lm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)
        self.lm_head.weight = self.token_embedding.weight

    def forward(self, token_ids: Tensor, cache: QuantizedLatentCache | None = None) -> Tensor:
        past_length = 0 if cache is None else cache.sequence_length()
        if past_length + token_ids.shape[1] > self.config.max_sequence_length:
            raise ValueError("sequence exceeds max_sequence_length")
        positions = torch.arange(past_length, past_length + token_ids.shape[1], device=token_ids.device)
        hidden = self.token_embedding(token_ids) + self.position_embedding(positions)
        for layer_index, layer in enumerate(self.layers):
            hidden = layer(hidden, layer_index, cache)
        return self.lm_head(self.final_norm(hidden))

    @torch.inference_mode()
    def generate(
        self, prompt: Tensor, max_new_tokens: int = 16, temperature: float = 0.0
    ) -> tuple[Tensor, QuantizedLatentCache]:
        if prompt.ndim != 2:
            raise ValueError("prompt must have shape [batch, sequence]")
        cache = QuantizedLatentCache(self.config.num_layers)
        logits = self(prompt, cache)
        generated = prompt
        for _ in range(max_new_tokens):
            next_logits = logits[:, -1]
            if temperature > 0:
                probabilities = F.softmax(next_logits / temperature, dim=-1)
                next_token = torch.multinomial(probabilities, num_samples=1)
            else:
                next_token = next_logits.argmax(dim=-1, keepdim=True)
            generated = torch.cat((generated, next_token), dim=1)
            logits = self(next_token, cache)
        return generated, cache

    def storage_report(self) -> dict[str, int | float | dict[str, int]]:
        totals = {
            key: 0 for key in ("ternary_symbols", "scales", "protected_values", "protected_indices", "fp32_baseline")
        }
        for module in self.modules():
            if isinstance(module, TernaryLinear):
                layer = module.storage_bits()
                for key in totals:
                    totals[key] += layer[key]
        quantized_bits = sum(value for key, value in totals.items() if key != "fp32_baseline")
        unquantized_parameters = sum(
            parameter.numel()
            for name, parameter in self.named_parameters()
            if not any(
                name.startswith(prefix) for prefix, module in self.named_modules() if isinstance(module, TernaryLinear)
            )
        )
        # Embeddings, norms and tied LM head remain FP32 in this research model.
        quantized_bits += unquantized_parameters * 32
        full_bits = sum(parameter.numel() for parameter in self.parameters()) * 32
        return {
            "config": asdict(self.config),
            "parameters": sum(parameter.numel() for parameter in self.parameters()),
            "fp32_bytes": full_bits // 8,
            "frozen_export_bytes": quantized_bits // 8,
            "compression_ratio": full_bits / quantized_bits,
            "ternary_detail_bits": totals,
        }


def synchronize(device: torch.device) -> None:
    if device.type == "mps":
        torch.mps.synchronize()
    elif device.type == "cuda":
        torch.cuda.synchronize(device)


@torch.inference_mode()
def benchmark_model(
    model: PocketPetTransformer, prompt_length: int = 64, new_tokens: int = 16, repeats: int = 3
) -> dict[str, float | int | str]:
    device = next(model.parameters()).device
    generator = torch.Generator(device="cpu").manual_seed(7)
    prompt = torch.randint(0, model.config.vocab_size, (1, prompt_length), generator=generator).to(device)
    model.generate(prompt, max_new_tokens=1)
    synchronize(device)
    durations, final_cache = [], None
    for _ in range(repeats):
        start = time.perf_counter()
        _, final_cache = model.generate(prompt, max_new_tokens=new_tokens)
        synchronize(device)
        durations.append(time.perf_counter() - start)
    assert final_cache is not None
    median = sorted(durations)[len(durations) // 2]
    return {
        "device": str(device),
        "prompt_tokens": prompt_length,
        "generated_tokens": new_tokens,
        "median_seconds": median,
        "generated_tokens_per_second": new_tokens / median,
        "latent_cache_bytes": final_cache.memory_bytes(),
        "fp16_full_kv_bytes": final_cache.fp16_full_kv_bytes(model.config),
        "cache_compression_ratio": final_cache.fp16_full_kv_bytes(model.config) / final_cache.memory_bytes(),
    }
