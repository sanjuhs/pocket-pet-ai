import torch

from pocket_pet import PocketPetConfig, PocketPetTransformer


def tiny_model() -> PocketPetTransformer:
    torch.manual_seed(11)
    config = PocketPetConfig(
        vocab_size=32,
        hidden_size=32,
        intermediate_size=64,
        num_layers=2,
        num_heads=4,
        latent_size=8,
        max_sequence_length=32,
        outlier_fraction=0.02,
    )
    return PocketPetTransformer(config).eval()


def test_causal_prefix_is_independent_of_future_tokens() -> None:
    model = tiny_model()
    short = torch.tensor([[1, 2, 3]])
    long = torch.tensor([[1, 2, 3, 7, 9]])
    with torch.inference_mode():
        short_logits = model(short)
        long_logits = model(long)[:, :3]
    assert torch.allclose(short_logits, long_logits, atol=2e-5)


def test_generation_is_deterministic_and_populates_cache() -> None:
    model = tiny_model()
    prompt = torch.tensor([[1, 4, 2]])
    first, cache = model.generate(prompt, max_new_tokens=4)
    second, _ = model.generate(prompt, max_new_tokens=4)

    assert first.shape == (1, 7)
    assert torch.equal(first, second)
    assert cache.sequence_length() == 7
    assert cache.memory_bytes() > 0


def test_storage_report_counts_real_parameters_and_compresses() -> None:
    model = tiny_model()
    report = model.storage_report()
    assert report["parameters"] == sum(parameter.numel() for parameter in model.parameters())
    assert 1 < report["compression_ratio"] < 16
    assert report["frozen_export_bytes"] < report["fp32_bytes"]
