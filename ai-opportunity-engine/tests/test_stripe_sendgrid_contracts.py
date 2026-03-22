import hashlib
import hmac

import pytest

from app.services.sendgrid_digest import render_weekly_digest, send_weekly_digest
from app.services.stripe_webhook import handle_stripe_webhook


@pytest.mark.asyncio
async def test_stripe_webhook_signature_contract() -> None:
    payload = b'{"type":"invoice.paid"}'
    secret = "whsec_test"
    signature = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()

    result = await handle_stripe_webhook(payload=payload, signature=signature, secret=secret)

    assert result["status"] == "ok"
    assert result["event_type"] == "invoice.paid"


@pytest.mark.asyncio
async def test_sendgrid_digest_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    class MockResponse:
        status_code = 202
        headers = {"X-Message-Id": "msg-123"}

    async def mock_post(self, *args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient.post", mock_post)

    html = render_weekly_digest([{"product": "phone-stand", "score": 85}])
    result = await send_weekly_digest(
        to_email="user@example.com",
        subject="Weekly Digest",
        html=html,
        api_key="sg_test",
    )

    assert "phone-stand" in html
    assert result["status"] == "sent"
    assert result["provider_message_id"] == "msg-123"
