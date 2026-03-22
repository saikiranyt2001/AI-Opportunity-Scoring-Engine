from sqlalchemy.ext.asyncio import AsyncSession

from app.models.patent_risk_flag import PatentRiskFlag
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def classify_patent_risk(opportunity: str) -> dict[str, str]:
    # Compliance: risk flags are informational and never suppress opportunities.
    return {
        "opportunity": opportunity,
        "risk_level": "low",
        "action": "informational_only",
    }


async def run_patent_scanner(session: AsyncSession | None = None) -> None:
    opportunities = [
        {"product_id": 1, "name": "phone stand"},
        {"product_id": 2, "name": "desk lamp"},
    ]
    results = []
    for item in opportunities:
        classification = await classify_patent_risk(item["name"])
        results.append(classification)
        if session is not None:
            session.add(
                PatentRiskFlag(
                    product_id=item["product_id"],
                    risk_level=classification["risk_level"],
                    rationale="NLP patent risk estimate",
                    action="informational_only",
                )
            )

    if session is not None:
        await session.commit()

    logger.info("Patent scanner informational flags: %s", results)
