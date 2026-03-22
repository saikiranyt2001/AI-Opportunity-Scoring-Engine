from sqlalchemy.ext.asyncio import AsyncSession

from app.models.position_alert import PositionAlert
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def evaluate_exit_criteria() -> list[dict[str, object]]:
    # Placeholder for real position rule checks from specification.
    return [
        {"position_id": 1, "criterion": "velocity_drop", "triggered": False},
        {"position_id": 1, "criterion": "margin_compression", "triggered": False},
        {"position_id": 1, "criterion": "competition_spike", "triggered": False},
    ]


async def run_position_monitor(session: AsyncSession | None = None) -> None:
    findings = await evaluate_exit_criteria()
    triggered = [item for item in findings if item["triggered"]]

    if session is not None:
        for item in findings:
            session.add(
                PositionAlert(
                    product_id=int(item["position_id"]),
                    criterion=str(item["criterion"]),
                    severity="warning" if item["triggered"] else "info",
                    message=f"Criterion {item['criterion']} evaluated",
                    resolved=not bool(item["triggered"]),
                )
            )
        await session.commit()

    if triggered:
        logger.warning("Position monitor alerts: %s", triggered)
    else:
        logger.info("Position monitor ran with no alerts")
