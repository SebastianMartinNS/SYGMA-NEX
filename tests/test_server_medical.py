import pytest
pytest.importorskip("fastapi")

from fastapi.testclient import TestClient
from sigma_nex.server import SigmaServer


def test_medical_branch_with_translation_disabled(monkeypatch):
    server = SigmaServer()

    # Disable translation
    server.translation_enabled = False

    # Make _is_medical_query return True
    monkeypatch.setattr(server, "_is_medical_query", lambda text: True)

    # Mock _call_ollama to return base and medical answers predictably
    async def fake_call(payload):
        if payload.get("model") == "medllama2":
            return "MEDICAL"
        return "BASE"

    monkeypatch.setattr(server, "_call_ollama", fake_call)

    client = TestClient(server.app)
    r = client.post("/ask", json={"question": "Ho una ferita"})
    assert r.status_code == 200
    # When translation is disabled, "MEDICAL" should not be appended (keeps BASE only)
    assert r.json()["response"] == "BASE"
