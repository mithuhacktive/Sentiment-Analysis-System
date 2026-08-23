from __future__ import annotations
import pytest
import os

os.environ["SENTIGUARD_OFFLINE"] = "true"


@pytest.mark.asyncio
async def test_health(client):
    resp = await client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "model_loaded" in data


@pytest.mark.asyncio
async def test_analyze_offline(client):
    resp = await client.post("/api/v1/analyze", json={"query": "Sony WH-1000XM5"})
    assert resp.status_code == 200
    data = resp.json()
    assert "analysis_id" in data
    assert "status" in data
    assert "pipeline" in data


@pytest.mark.asyncio
async def test_analyze_empty_query(client):
    resp = await client.post("/api/v1/analyze", json={"query": "   "})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_analyze_url_input(client):
    resp = await client.post("/api/v1/analyze", json={"query": "https://example.com/product"})
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_feedback_endpoint(client):
    resp = await client.post("/api/v1/feedback", json={
        "analysis_id": "test-uuid-1234",
        "correct_label": "POSITIVE",
    })
    assert resp.status_code == 200
    assert resp.json()["accepted"] is True