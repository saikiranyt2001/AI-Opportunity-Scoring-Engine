from fastapi.testclient import TestClient

from app.api import routes
from app.core.database import get_session
from app.main import app


client = TestClient(app)


def test_score_endpoint() -> None:
    async def override_get_session():
        class DummySession:
            pass

        yield DummySession()

    async def mock_calculate_score(product_name: str, session=None) -> dict:
        return {"product": product_name, "score": 85}

    app.dependency_overrides[get_session] = override_get_session
    original_calculate_score = routes.calculate_score
    routes.calculate_score = mock_calculate_score

    try:
        response = client.get("/score/test-product")

        assert response.status_code == 200
        data = response.json()

        assert "product" in data
        assert "score" in data
    finally:
        routes.calculate_score = original_calculate_score
        app.dependency_overrides.clear()
