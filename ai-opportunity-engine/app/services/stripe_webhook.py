import hashlib
import hmac
import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.logs import PipelineLog


def verify_stripe_signature(payload: bytes, signature: str, secret: str) -> bool:
    digest = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, signature)


def parse_stripe_event(payload: bytes) -> dict:
    return json.loads(payload.decode("utf-8"))


async def handle_stripe_webhook(
    payload: bytes,
    signature: str,
    secret: str,
    session: AsyncSession | None = None,
) -> dict[str, str]:
    if not verify_stripe_signature(payload, signature, secret):
        raise ValueError("Invalid Stripe signature")

    event = parse_stripe_event(payload)

    if session is not None:
        session.add(
            PipelineLog(
                event_type="stripe_webhook",
                message=f"Received Stripe event: {event.get('type', 'unknown')}",
            )
        )
        await session.commit()

    return {
        "status": "ok",
        "event_type": str(event.get("type", "unknown")),
    }
