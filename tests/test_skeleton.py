from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_missing_token_is_rejected():
    assert client.get("/office/requests").status_code == 401


def test_wrong_role_is_forbidden():
    r = client.get("/office/requests", headers={"Authorization": "Bearer member:1"})
    assert r.status_code == 403
