from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_webhook_alerts():
    payload = {
        "source": "prometheus",
        "alerts": [
            {
                "fingerprint": "abc123",
                "status": "firing",
                "labels": {
                    "alertname": "HighErrorRate",
                    "service": "checkout-service",
                    "severity": "critical",
                    "namespace": "prod",
                },
                "annotations": {
                    "summary": "High 5xx error rate detected",
                    "description": "5xx error rate > 10% for 5m",
                },
                "startsAt": "2026-04-29T10:00:00Z",
            }
        ],
    }

    resp = client.post("/webhooks/alerts", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "incident_id" in data
    assert data["status"] == "processing"
