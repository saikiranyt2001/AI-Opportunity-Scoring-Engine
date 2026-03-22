from fastapi.testclient import TestClient

from app.api import routes
from app.core.database import get_session
from app.main import app


def test_score_endpoint_returns_subscriber_safe_payload() -> None:
    async def override_get_session():
        class DummySession:
            pass

        yield DummySession()

    async def fake_calculate_score(product_name: str, session=None) -> dict:
        return {
            "product": product_name,
            "score": 85,
        }

    app.dependency_overrides[get_session] = override_get_session
    original_calculate_score = routes.calculate_score
    routes.calculate_score = fake_calculate_score

    try:
        client = TestClient(app)

        response = client.get("/score/phone-stand")

        assert response.status_code == 200

        payload = response.json()
        assert payload["product"] == "phone-stand"
        assert payload["score"] == 85
        assert "shadow_models" not in payload
    finally:
        routes.calculate_score = original_calculate_score
        app.dependency_overrides.clear()
