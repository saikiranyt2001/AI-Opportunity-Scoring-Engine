from app.core.config import settings
from app.core.database import SessionLocal
from app.services.scoring_engine import calculate_score
from app.services.sendgrid_digest import render_weekly_digest, send_weekly_digest
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def run_weekly_digest() -> dict[str, object]:
    products = ["phone stand", "desk lamp"]

    async with SessionLocal() as session:
        opportunities = []
        for product in products:
            opportunities.append(await calculate_score(product, session))

        html = render_weekly_digest(opportunities)

        if not settings.sendgrid_api_key:
            logger.info("Skipping digest send because SENDGRID_API_KEY is not configured")
            return {
                "status": "skipped",
                "reason": "missing_sendgrid_api_key",
                "opportunity_count": len(opportunities),
            }

        result = await send_weekly_digest(
            to_email=settings.digest_default_recipient,
            subject=settings.digest_subject,
            html=html,
            api_key=settings.sendgrid_api_key,
            session=session,
        )

    return {
        "status": result["status"],
        "opportunity_count": len(opportunities),
        "provider_message_id": result.get("provider_message_id", ""),
    }
