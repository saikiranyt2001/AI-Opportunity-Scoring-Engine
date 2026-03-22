from fastapi.testclient import TestClient

from app.api import routes
from app.core import config
from app.core.database import get_session
from app.main import app


def test_stripe_test_endpoint_disabled_by_default() -> None:
    async def override_get_session():
        class DummySession:
            pass

        yield DummySession()

    app.dependency_overrides[get_session] = override_get_session

    original_environment = config.settings.environment
    original_enabled = config.settings.enable_stripe_test_webhook

    config.settings.environment = "production"
    config.settings.enable_stripe_test_webhook = False

    try:
        client = TestClient(app)
        response = client.post("/webhooks/stripe/test")
        assert response.status_code == 403
    finally:
        config.settings.environment = original_environment
        config.settings.enable_stripe_test_webhook = original_enabled
        app.dependency_overrides.clear()


def test_stripe_test_endpoint_enabled_non_production() -> None:
    async def override_get_session():
        class DummySession:
            pass

        yield DummySession()

    async def fake_handle_stripe_webhook(payload: bytes, signature: str, secret: str, session=None) -> dict:
        return {"status": "ok", "event_type": "checkout.session.completed"}

    app.dependency_overrides[get_session] = override_get_session

    original_environment = config.settings.environment
    original_enabled = config.settings.enable_stripe_test_webhook
    original_handler = routes.handle_stripe_webhook

    config.settings.environment = "development"
    config.settings.enable_stripe_test_webhook = True
    routes.handle_stripe_webhook = fake_handle_stripe_webhook

    try:
        client = TestClient(app)
        response = client.post("/webhooks/stripe/test")
        assert response.status_code == 200
        payload = response.json()
        assert payload["status"] == "ok"
        assert payload["event_type"] == "checkout.session.completed"
    finally:
        config.settings.environment = original_environment
        config.settings.enable_stripe_test_webhook = original_enabled
        routes.handle_stripe_webhook = original_handler
        app.dependency_overrides.clear()
