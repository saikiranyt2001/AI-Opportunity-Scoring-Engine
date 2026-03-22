import hashlib
import hmac

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_session
from app.schemas.score_schema import ScoreResponse
from app.services.scoring_engine import calculate_score
from app.services.stripe_webhook import handle_stripe_webhook
from app.tasks.weekly_digest import run_weekly_digest

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/score/{product}", response_model=ScoreResponse)
async def score_product(product: str, session: AsyncSession = Depends(get_session)) -> dict:
    return await calculate_score(product, session)


@router.post("/webhooks/stripe")
async def stripe_webhook(
    request: Request,
    session: AsyncSession = Depends(get_session),
    stripe_signature: str = Header(default="", alias="Stripe-Signature"),
) -> dict[str, str]:
    if not settings.stripe_webhook_secret:
        raise HTTPException(status_code=500, detail="Stripe webhook secret is not configured")

    payload = await request.body()
    try:
        return await handle_stripe_webhook(
            payload=payload,
            signature=stripe_signature,
            secret=settings.stripe_webhook_secret,
            session=session,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/webhooks/stripe/test")
async def stripe_webhook_test(session: AsyncSession = Depends(get_session)) -> dict[str, str]:
    if settings.environment.lower() == "production" or not settings.enable_stripe_test_webhook:
        raise HTTPException(status_code=403, detail="Stripe test webhook endpoint is disabled")

    payload = b'{"type":"checkout.session.completed","mode":"test"}'
    secret = settings.stripe_webhook_secret or "local-test-secret"
    signature = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()

    return await handle_stripe_webhook(
        payload=payload,
        signature=signature,
        secret=secret,
        session=session,
    )


@router.post("/digest/weekly/run")
async def trigger_weekly_digest() -> dict[str, object]:
    return await run_weekly_digest()
