import json
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.logs import PipelineLog
from app.models.product import Product
from app.models.shadow_model_run import ShadowModelRun
from app.models.score import Score
from app.scoring.shadow_models import run_shadow_reconciliation


async def _get_or_create_product(session: AsyncSession, product_name: str) -> Product:
    product_stmt = select(Product).where(Product.name == product_name)
    product = await session.scalar(product_stmt)

    if product is None:
        product = Product(name=product_name)
        session.add(product)
        await session.flush()

    return product


async def calculate_score(
    product_name: str, session: AsyncSession | None = None
) -> dict[str, Any]:
    primary_score = 85

    shadow_payload = await run_shadow_reconciliation(product_name)
    shadow_results = shadow_payload.get("results", [])
    reconciliation = shadow_payload.get("reconciliation", {})

    if session is not None:
        try:
            product = await _get_or_create_product(session, product_name)

            session.add(
                Score(
                    product_id=product.id,
                    primary_score=primary_score,
                    shadow_payload=json.dumps(shadow_results),
                )
            )

            session.add(
                ShadowModelRun(
                    product_id=product.id,
                    models_responded=int(reconciliation.get("models_responded", 0)),
                    failures=int(shadow_payload.get("failures", 0)),
                    average_score=float(reconciliation.get("average_score", 0.0)),
                    score_spread=float(reconciliation.get("score_spread", 0.0)),
                    raw_payload=json.dumps(shadow_payload),
                )
            )

            session.add(
                PipelineLog(
                    event_type="score_calculated",
                    message=f"Score calculated for {product_name}",
                )
            )

            await session.commit()

        except Exception as e:
            await session.rollback()

            # Optional: structured logging (recommended)
            session.add(
                PipelineLog(
                    event_type="score_failed",
                    message=f"Failed scoring for {product_name}: {str(e)}",
                )
            )
            await session.commit()

    return {
        "product": product_name,
        "score": primary_score,
    }