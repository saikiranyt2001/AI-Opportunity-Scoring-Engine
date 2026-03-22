import pytest

from app.scoring import shadow_models


@pytest.mark.asyncio
async def test_shadow_models_success(monkeypatch: pytest.MonkeyPatch) -> None:
    async def mock_gpt4o(prompt: str):
        return {"model": "gpt-4o", "score": 80}

    async def mock_gemini(prompt: str):
        return {"model": "gemini", "score": 75}

    async def mock_grok(prompt: str):
        return {"model": "grok", "score": 70}

    monkeypatch.setattr(shadow_models, "call_gpt4o", mock_gpt4o)
    monkeypatch.setattr(shadow_models, "call_gemini", mock_gemini)
    monkeypatch.setattr(shadow_models, "call_grok", mock_grok)

    result = await shadow_models.run_shadow_models("test product")

    assert len(result) == 3
    assert {r["model"] for r in result} == {"gpt-4o", "gemini", "grok"}


@pytest.mark.asyncio
async def test_shadow_models_partial_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    async def mock_gpt4o(prompt: str):
        return {"model": "gpt-4o", "score": 80}

    async def mock_fail(prompt: str):
        raise Exception("API failure")

    monkeypatch.setattr(shadow_models, "call_gpt4o", mock_gpt4o)
    monkeypatch.setattr(shadow_models, "call_gemini", mock_fail)
    monkeypatch.setattr(shadow_models, "call_grok", mock_fail)

    result = await shadow_models.run_shadow_models("test product")

    # Only one should succeed
    assert len(result) == 1
    assert result[0]["model"] == "gpt-4o"


@pytest.mark.asyncio
async def test_shadow_models_all_fail(monkeypatch: pytest.MonkeyPatch) -> None:
    async def mock_fail(prompt: str):
        raise Exception("API down")

    monkeypatch.setattr(shadow_models, "call_gpt4o", mock_fail)
    monkeypatch.setattr(shadow_models, "call_gemini", mock_fail)
    monkeypatch.setattr(shadow_models, "call_grok", mock_fail)

    result = await shadow_models.run_shadow_models("test product")

    # Should not crash and return empty list
    assert result == []


@pytest.mark.asyncio
async def test_shadow_reconciliation_metrics(monkeypatch: pytest.MonkeyPatch) -> None:
    async def mock_gpt4o(prompt: str):
        return {"model": "gpt-4o", "score": 80}

    async def mock_gemini(prompt: str):
        return {"model": "gemini", "score": 70}

    async def mock_grok(prompt: str):
        return {"model": "grok", "score": 60}

    monkeypatch.setattr(shadow_models, "call_gpt4o", mock_gpt4o)
    monkeypatch.setattr(shadow_models, "call_gemini", mock_gemini)
    monkeypatch.setattr(shadow_models, "call_grok", mock_grok)

    payload = await shadow_models.run_shadow_reconciliation("test product")

    assert payload["reconciliation"]["models_responded"] == 3
    assert payload["reconciliation"]["average_score"] == 70.0
    assert payload["reconciliation"]["score_spread"] == 20.0