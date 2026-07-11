from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PocketPetConfig:
    """Dimensions for the deliberately small, locally executable model."""

    vocab_size: int = 256
    hidden_size: int = 128
    intermediate_size: int = 320
    num_layers: int = 3
    num_heads: int = 4
    latent_size: int = 32
    max_sequence_length: int = 512
    outlier_fraction: float = 0.01

    def __post_init__(self) -> None:
        if self.hidden_size % self.num_heads:
            raise ValueError("hidden_size must be divisible by num_heads")
        if not 0 <= self.outlier_fraction < 1:
            raise ValueError("outlier_fraction must be in [0, 1)")
        if self.latent_size <= 0:
            raise ValueError("latent_size must be positive")

    @property
    def head_size(self) -> int:
        return self.hidden_size // self.num_heads
