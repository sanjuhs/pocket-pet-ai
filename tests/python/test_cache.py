import torch

from pocket_pet import PocketPetConfig
from pocket_pet.cache import QuantizedLatentCache


def test_latent_cache_round_trip_and_memory_advantage() -> None:
    torch.manual_seed(3)
    config = PocketPetConfig(hidden_size=64, intermediate_size=128, num_layers=2, num_heads=4, latent_size=16)
    cache = QuantizedLatentCache(config.num_layers)
    source = torch.randn(1, 12, config.latent_size)
    for layer in range(config.num_layers):
        restored = cache.append(layer, source)
        assert torch.allclose(restored, source, atol=0.02)

    assert cache.sequence_length() == 12
    assert cache.memory_bytes() < cache.fp16_full_kv_bytes(config)
    # int8 latent + FP16 scale: 18 bytes/token/layer vs 256 bytes for FP16 K+V.
    assert cache.fp16_full_kv_bytes(config) / cache.memory_bytes() > 10


def test_cache_appends_incrementally() -> None:
    cache = QuantizedLatentCache(1)
    cache.append(0, torch.ones(1, 2, 4))
    cache.append(0, torch.zeros(1, 1, 4))
    assert cache.sequence_length() == 3
    assert cache.get(0).shape == (1, 3, 4)
