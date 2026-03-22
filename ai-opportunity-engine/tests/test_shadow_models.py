import pytest

from app.scoring import shadow_models


@pytest.mark.asyncio
async def test_shadow_models_success(monkeypatch: pytest.MonkeyPatch) -> None:
    async def mock_gpt4o(prompt: str) -> dict[str, int | str]:
        return {"model": "gpt-4o", "score": 80}

    async def mock_gemini(prompt: str) -> dict[str, int | str]:
        return {"model": "gemini", "score": 75}

    async def mock_grok(prompt: str) -> dict[str, int | str]:
        return {"model": "grok", "score": 70}

    monkeypatch.setattr(shadow_models, "call_gpt4o", mock_gpt4o)
    monkeypatch.setattr(shadow_models, "call_gemini", mock_gemini)
    monkeypatch.setattr(shadow_models, "call_grok", mock_grok)

    result = await shadow_models.run_shadow_models("test product")

    assert len(result) == 3
    assert result[0]["model"] == "gpt-4o"


@pytest.mark.asyncio
async def test_shadow_models_partial_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    async def mock_gpt4o(prompt: str) -> dict[str, int | str]:
        return {"model": "gpt-4o", "score": 80}

    async def mock_gemini(prompt: str) -> dict[str, int | str]:
        raise Exception("API failure")

    async def mock_grok(prompt: str) -> dict[str, int | str]:
        raise Exception("API failure")

    monkeypatch.setattr(shadow_models, "call_gpt4o", mock_gpt4o)
    monkeypatch.setattr(shadow_models, "call_gemini", mock_gemini)
    monkeypatch.setattr(shadow_models, "call_grok", mock_grok)

    result = await shadow_models.run_shadow_models("test product")

    assert len(result) == 1
    assert result[0]["model"] == "gpt-4o"


@pytest.mark.asyncio
async def test_shadow_models_all_fail(monkeypatch: pytest.MonkeyPatch) -> None:
    async def mock_fail(prompt: str) -> dict[str, int | str]:
        raise Exception("API down")

    monkeypatch.setattr(shadow_models, "call_gpt4o", mock_fail)
    monkeypatch.setattr(shadow_models, "call_gemini", mock_fail)
    monkeypatch.setattr(shadow_models, "call_grok", mock_fail)

    result = await shadow_models.run_shadow_models("test product")

    assert result == []
