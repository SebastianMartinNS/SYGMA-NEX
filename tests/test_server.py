import json
import pytest

# FastAPI TestClient is only available if fastapi is installed
pytest.importorskip("fastapi")

from fastapi.testclient import TestClient
from sigma_nex.server import SigmaServer


class DummyResp:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self._payload = payload or {"response": "ok"}
    def json(self):
        return self._payload


def _client_with_mocked_ollama(monkeypatch):
    server = SigmaServer()

    def fake_post(url, json=None, timeout=None):
        return DummyResp(200, {"response": "mock-answer"})

    import requests
    monkeypatch.setattr(requests, "post", fake_post)

    return TestClient(server.app)


def test_health():
    client = _client_with_mocked_ollama(pytest.MonkeyPatch())
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"
    assert "uptime" in data


def test_ask_success(monkeypatch):
    client = _client_with_mocked_ollama(monkeypatch)
    payload = {
        "question": "Come accendere un fuoco?",
        "history": ["Utente: Ciao"],
        "user_id": 1
    }
    r = client.post("/ask", json=payload)
    assert r.status_code == 200
    j = r.json()
    assert j["response"] == "mock-answer"
    assert j["model_used"]


def test_ask_blocked_user(monkeypatch, tmp_path):
    # Create a temporary blocklist that blocks user 99
    server = SigmaServer()
    # Point blocklist path to a temp file
    server.blocklist_path = tmp_path / "blocklist.json"
    server.blocklist_path.write_text(json.dumps({"users": ["99"], "chats": []}), encoding="utf-8")

    client = TestClient(server.app)
    payload = {"question": "ciao", "user_id": 99}
    r = client.post("/ask", json=payload)
    assert r.status_code == 403


def test_ollama_timeout(monkeypatch):
    server = SigmaServer()

    def raise_timeout(url, json=None, timeout=None):
        import requests
        raise requests.exceptions.Timeout()

    import requests
    monkeypatch.setattr(requests, "post", raise_timeout)

    client = TestClient(server.app)
    payload = {"question": "ciao"}
    r = client.post("/ask", json=payload)
    assert r.status_code == 504
