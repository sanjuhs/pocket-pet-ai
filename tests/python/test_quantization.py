import torch

from pocket_pet.quantization import TernaryLinear, ternary_decompose


def test_ternary_symbols_and_protected_outliers_are_deterministic() -> None:
    weight = torch.tensor([[0.01, -0.4, 0.2, 9.0], [-8.0, 0.3, -0.1, 0.5]])
    ternary, scale, protected, mask = ternary_decompose(weight, outlier_fraction=0.25)

    assert set(ternary.unique().tolist()) <= {-1.0, 0.0, 1.0}
    assert mask.sum().item() == 2
    assert protected[0, 3].item() == 9.0
    assert protected[1, 0].item() == -8.0
    assert torch.all(ternary[mask] == 0)
    assert scale.shape == (2, 1)


def test_ternary_linear_runs_real_tensor_math_and_backpropagates() -> None:
    torch.manual_seed(2)
    layer = TernaryLinear(8, 4, outlier_fraction=0.125)
    inputs = torch.randn(3, 8, requires_grad=True)
    output = layer(inputs)
    output.square().mean().backward()

    assert output.shape == (3, 4)
    assert inputs.grad is not None
    assert torch.isfinite(inputs.grad).all()
    assert layer.storage_bits()["ternary_symbols"] == 2 * layer.weight.numel()
