import hashlib
import hmac

from fastapi.testclient import TestClient

from app.api import routes
from app.core import config
from app.core.database import get_session
from app.main import app


def test_subscriber_journey_score_webhook_and_digest() -> None:
    async def override_get_session():
        class DummySession:
            pass

        yield DummySession()

    async def fake_calculate_score(product_name: str, session=None) -> dict:
        return {"product": product_name, "score": 88}

    async def fake_handle_stripe_webhook(payload: bytes, signature: str, secret: str, session=None) -> dict:
        return {"status": "ok", "event_type": "invoice.paid"}

    async def fake_run_weekly_digest() -> dict[str, object]:
        return {
            "status": "sent",
            "opportunity_count": 2,
            "provider_message_id": "msg-e2e",
        }

    app.dependency_overrides[get_session] = override_get_session

    original_calculate_score = routes.calculate_score
    original_handle_stripe_webhook = routes.handle_stripe_webhook
    original_run_weekly_digest = routes.run_weekly_digest
    original_secret = config.settings.stripe_webhook_secret

    routes.calculate_score = fake_calculate_score
    routes.handle_stripe_webhook = fake_handle_stripe_webhook
    routes.run_weekly_digest = fake_run_weekly_digest
    config.settings.stripe_webhook_secret = "whsec_test"

    try:
        client = TestClient(app)

        score_response = client.get("/score/phone-stand")
        assert score_response.status_code == 200
        assert score_response.json()["score"] == 88

        payload = b'{"type":"invoice.paid"}'
        signature = hmac.new(
            config.settings.stripe_webhook_secret.encode("utf-8"),
            payload,
            hashlib.sha256,
        ).hexdigest()
        webhook_response = client.post(
            "/webhooks/stripe",
            content=payload,
            headers={"Stripe-Signature": signature},
        )
        assert webhook_response.status_code == 200
        assert webhook_response.json()["event_type"] == "invoice.paid"

        digest_response = client.post("/digest/weekly/run")
        assert digest_response.status_code == 200
        assert digest_response.json()["status"] == "sent"
        assert digest_response.json()["opportunity_count"] == 2
    finally:
        routes.calculate_score = original_calculate_score
        routes.handle_stripe_webhook = original_handle_stripe_webhook
        routes.run_weekly_digest = original_run_weekly_digest
        config.settings.stripe_webhook_secret = original_secret
        app.dependency_overrides.clear()
