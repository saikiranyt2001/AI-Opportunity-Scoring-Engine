from sqlalchemy.ext.asyncio import AsyncSession

from app.models.accessory_keyword import AccessoryKeyword
from app.models.logs import PipelineLog


async def derive_accessory_keywords(
    opportunity_text: str,
    session: AsyncSession | None = None,
    product_id: int | None = None,
) -> list[str]:
    # Placeholder output until provider-specific prompt wiring is added.
    keywords = [
        "travel case",
        "replacement parts",
        "mounting kit",
        "cleaning accessory",
        "storage organizer",
    ]

    if session is not None and product_id is not None:
        for index, keyword in enumerate(keywords, start=1):
            session.add(
                AccessoryKeyword(
                    product_id=product_id,
                    keyword=keyword,
                    rank=index,
                    source_model="claude",
                )
            )

    if session is not None:
        session.add(
            PipelineLog(
                event_type="accessory_derived",
                message=f"Derived accessories for: {opportunity_text}",
            )
        )
        await session.commit()

    return keywords
