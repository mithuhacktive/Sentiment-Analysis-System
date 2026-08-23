#!/usr/bin/env python3
"""Benchmark inference speed at different review counts."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.ml.model import get_model

SAMPLE = "The battery life on this product is outstanding. Very comfortable to use. Highly recommend."
SIZES = [10, 50, 100, 250]


def main():
    model = get_model()
    model.load()
    print("=== SentiGuard Benchmark ===\n")
    print(f"{'Reviews':<10} {'Total (ms)':<14} {'Per review (ms)':<18} {'Throughput (rev/s)'}")
    print("-" * 60)

    for n in SIZES:
        texts = [SAMPLE] * n
        start = time.perf_counter()
        model.predict_batch(texts)
        elapsed = time.perf_counter() - start
        per_rev = (elapsed / n) * 1000
        throughput = n / elapsed
        print(f"{n:<10} {elapsed*1000:<14.1f} {per_rev:<18.2f} {throughput:.1f}")


if __name__ == "__main__":
    main()