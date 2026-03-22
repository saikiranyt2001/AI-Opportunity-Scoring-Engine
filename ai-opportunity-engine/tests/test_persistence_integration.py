from pathlib import Path

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.models import Base
from app.models.logs import PipelineLog
from app.models.product import Product
from app.models.shadow_model_run import ShadowModelRun
from app.models.score import Score
from app.scoring import shadow_models
from app.services.scoring_engine import calculate_score


@pytest.mark.asyncio
async def test_calculate_score_persists_records_with_async_sqlite(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def mock_gpt4o(prompt: str) -> dict[str, int | str]:
        return {"model": "gpt-4o", "score": 80}

    async def mock_gemini(prompt: str) -> dict[str, int | str]:
        return {"model": "gemini", "score": 75}

    async def mock_grok(prompt: str) -> dict[str, int | str]:
        return {"model": "grok", "score": 70}

    monkeypatch.setattr(shadow_models, "call_gpt4o", mock_gpt4o)
    monkeypatch.setattr(shadow_models, "call_gemini", mock_gemini)
    monkeypatch.setattr(shadow_models, "call_grok", mock_grok)

    db_path = tmp_path / "integration.db"
    engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}", echo=False)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_maker() as session:
        result = await calculate_score("phone-stand", session)

    assert result["product"] == "phone-stand"
    assert result["score"] == 85
    assert "shadow_models" not in result

    async with session_maker() as session:
        product_count = await session.scalar(select(func.count(Product.id)))
        score_count = await session.scalar(select(func.count(Score.id)))
        shadow_run_count = await session.scalar(select(func.count(ShadowModelRun.id)))
        log_count = await session.scalar(select(func.count(PipelineLog.id)))

    assert product_count == 1
    assert score_count == 1
    assert shadow_run_count == 1
    assert log_count == 1

    await engine.dispose()
