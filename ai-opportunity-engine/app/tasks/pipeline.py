from app.core.database import SessionLocal
from app.services.scoring_engine import calculate_score
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def run_pipeline() -> None:
    products = ["phone stand", "desk lamp"]

    async with SessionLocal() as session:
        for product in products:
            result = await calculate_score(product, session)
            logger.info("Pipeline result: %s", result)
