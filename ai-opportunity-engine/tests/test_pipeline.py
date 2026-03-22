import pytest

from app.tasks import pipeline as pipeline_module


class DummySession:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


@pytest.mark.asyncio
async def test_pipeline_runs_without_crash(monkeypatch: pytest.MonkeyPatch) -> None:
    async def mock_score(product: str, session=None) -> dict[str, int | str]:
        return {"product": product, "score": 80}

    monkeypatch.setattr(pipeline_module, "SessionLocal", DummySession)
    monkeypatch.setattr(pipeline_module, "calculate_score", mock_score)

    await pipeline_module.run_pipeline()
