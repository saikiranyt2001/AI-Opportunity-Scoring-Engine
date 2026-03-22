import pytest

from app.scoring import shadow_models


@pytest.mark.asyncio
async def test_shadow_reconciliation_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    async def ok_gpt4o(prompt: str) -> dict[str, int | str]:
        return {"model": "gpt-4o", "score": 90}

    async def fail_gemini(prompt: str) -> dict[str, int | str]:
        raise RuntimeError("timeout")

    async def ok_grok(prompt: str) -> dict[str, int | str]:
        return {"model": "grok", "score": 70}

    monkeypatch.setattr(shadow_models, "call_gpt4o", ok_gpt4o)
    monkeypatch.setattr(shadow_models, "call_gemini", fail_gemini)
    monkeypatch.setattr(shadow_models, "call_grok", ok_grok)

    payload = await shadow_models.run_shadow_reconciliation("phone-stand")

    assert payload["phase1_subscriber_visible"] is False
    assert payload["failures"] == 1
    assert payload["reconciliation"]["models_responded"] == 2
    assert payload["reconciliation"]["average_score"] == 80.0
