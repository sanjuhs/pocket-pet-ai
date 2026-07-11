#!/usr/bin/env python3
import argparse
import json

import torch

from pocket_pet import PocketPetConfig, PocketPetTransformer
from pocket_pet.model import benchmark_model


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark the Pocket Pet ternary transformer emulator")
    parser.add_argument("--prompt-length", type=int, default=64)
    parser.add_argument("--new-tokens", type=int, default=16)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--device", choices=("auto", "cpu", "mps"), default="auto")
    args = parser.parse_args()

    torch.manual_seed(7)
    device = (
        "mps"
        if args.device == "auto" and torch.backends.mps.is_available()
        else "cpu"
        if args.device == "auto"
        else args.device
    )
    model = PocketPetTransformer(PocketPetConfig()).eval().to(device)
    report = {
        "storage": model.storage_report(),
        "runtime": benchmark_model(model, args.prompt_length, args.new_tokens, args.repeats),
        "interpretation": (
            "PyTorch emulates ternary arithmetic; reported frozen-export bytes assume packed 2-bit symbols."
        ),
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
