from app import create_app


def test_health_endpoint_returns_json():
    app = create_app()
    client = app.test_client()

    response = client.get("/api/health")

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert "ffmpeg" in data["tools"]


def test_create_job_rejects_invalid_payload():
    app = create_app()
    client = app.test_client()

    response = client.post(
        "/api/jobs",
        json={"video_url": "not-a-url", "output_name": "bad/name", "bitrate": "999"},
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["field_errors"]["video_url"]
    assert data["field_errors"]["output_name"]
    assert data["field_errors"]["bitrate"]
