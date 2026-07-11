import torch

from pocket_pet import PocketPetConfig, PocketPetTransformer
from pocket_pet.cache import QuantizedLatentCache
from pocket_pet.quantization import ternary_decompose


def test_protecting_outliers_improves_injected_outlier_reconstruction() -> None:
    torch.manual_seed(19)
    weight = torch.randn(32, 32)
    indices = weight.abs().flatten().topk(11).indices
    weight.view(-1)[indices] *= 20

    errors = []
    for fraction in (0.0, 0.02):
        ternary, scale, protected, _ = ternary_decompose(weight, fraction)
        errors.append(torch.linalg.vector_norm(ternary * scale + protected - weight))

    assert errors[1] < errors[0]


def test_ternary_integer_matmul_equals_routed_add_subtract() -> None:
    torch.manual_seed(31)
    activations = torch.randint(-127, 128, (5, 17), dtype=torch.int32)
    symbols = torch.randint(-1, 2, (7, 17), dtype=torch.int32)
    reference = activations @ symbols.T
    routed = torch.stack(
        [
            activations[:, output_symbols == 1].sum(dim=1) - activations[:, output_symbols == -1].sum(dim=1)
            for output_symbols in symbols
        ],
        dim=1,
    )

    assert torch.equal(reference, routed)


def test_cache_byte_formula_matches_allocated_tensor_payload() -> None:
    config = PocketPetConfig(hidden_size=64, intermediate_size=128, num_layers=3, num_heads=4, latent_size=12)
    cache = QuantizedLatentCache(config.num_layers)
    for layer in range(config.num_layers):
        cache.append(layer, torch.randn(2, 17, config.latent_size))

    expected = config.num_layers * 2 * 17 * (config.latent_size + 2)
    assert cache.memory_bytes() == expected


def test_one_shot_and_incremental_cache_paths_are_numerically_equivalent() -> None:
    torch.manual_seed(23)
    config = PocketPetConfig(
        vocab_size=32,
        hidden_size=32,
        intermediate_size=64,
        num_layers=2,
        num_heads=4,
        latent_size=8,
        max_sequence_length=16,
    )
    model = PocketPetTransformer(config).eval()
    tokens = torch.tensor([[2, 8, 5, 3, 1, 9]])

    with torch.inference_mode():
        one_shot_cache = QuantizedLatentCache(config.num_layers)
        one_shot = model(tokens, one_shot_cache)
        incremental_cache = QuantizedLatentCache(config.num_layers)
        incremental = torch.cat(
            [model(tokens[:, index : index + 1], incremental_cache) for index in range(tokens.shape[1])], dim=1
        )

    assert torch.allclose(one_shot, incremental, atol=2e-5)
    assert one_shot_cache.memory_bytes() == incremental_cache.memory_bytes()
