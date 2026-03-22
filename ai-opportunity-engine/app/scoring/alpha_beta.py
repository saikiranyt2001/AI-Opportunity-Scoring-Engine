from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alpha_beta_metric import AlphaBetaMetric


@dataclass
class AlphaBetaInput:
    alpha_components: list[float]
    beta_components: list[float]


def _weighted_average(values: list[float]) -> float:
    if not values:
        return 0.0
    return round(sum(values) / len(values), 2)


def calculate_alpha_beta(payload: AlphaBetaInput) -> dict[str, float]:
    alpha_score = _weighted_average(payload.alpha_components)
    beta_score = _weighted_average(payload.beta_components)
    oqs = round((alpha_score * 0.6) + (beta_score * 0.4), 2)

    # Half-life is a heuristic estimate for opportunity durability.
    alpha_half_life_days = round(max(alpha_score - beta_score, 0) * 1.5 + 7, 2)

    return {
        "alpha_score": alpha_score,
        "beta_score": beta_score,
        "oqs": oqs,
        "alpha_half_life_days": alpha_half_life_days,
    }


async def calculate_alpha_beta_and_persist(
    payload: AlphaBetaInput,
    session: AsyncSession,
    product_id: int,
) -> dict[str, float]:
    result = calculate_alpha_beta(payload)
    session.add(
        AlphaBetaMetric(
            product_id=product_id,
            alpha_score=result["alpha_score"],
            beta_score=result["beta_score"],
            oqs=result["oqs"],
            alpha_half_life_days=result["alpha_half_life_days"],
        )
    )
    await session.commit()
    return result
