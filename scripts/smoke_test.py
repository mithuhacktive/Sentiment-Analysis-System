#!/usr/bin/env python3
"""Quick smoke test — run against a live server."""
import sys
import httpx

BASE = "http://localhost:8000/api/v1"


def check(name, resp):
    if resp.status_code == 200:
        print(f"  [PASS] {name}")
    else:
        print(f"  [FAIL] {name} — HTTP {resp.status_code}: {resp.text[:200]}")
        sys.exit(1)


def main():
    print("=== SentiGuard Smoke Test ===")
    with httpx.Client(timeout=60) as c:
        check("health", c.get(f"{BASE}/health"))
        check("ready", c.get(f"{BASE}/health/ready"))
        check("analyze product name", c.post(f"{BASE}/analyze", json={"query": "Sony WH-1000XM5"}))
        check("analyze URL", c.post(f"{BASE}/analyze", json={"query": "https://example.com/product/test"}))
        check("feedback", c.post(f"{BASE}/feedback", json={"analysis_id": "test-001", "correct_label": "POSITIVE"}))
    print("\n=== All smoke tests passed ===")


if __name__ == "__main__":
    main()