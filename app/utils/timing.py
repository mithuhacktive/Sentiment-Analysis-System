from __future__ import annotations
import time
from contextlib import contextmanager
from typing import Generator


@contextmanager
def timer(label: str = "") -> Generator[dict, None, None]:
    data: dict = {"label": label, "ms": 0.0}
    start = time.perf_counter()
    try:
        yield data
    finally:
        data["ms"] = round((time.perf_counter() - start) * 1000, 2)