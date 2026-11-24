from types import SimpleNamespace
import app as app_module


def test_home():
    client = app_module.app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"AIT AI Application is Running!" in response.data


def test_health():
    client = app_module.app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    assert response.json["application"] == "AIT AI Assistant"


def test_empty_question():
    client = app_module.app.test_client()
    response = client.post("/ask", json={"question": ""})

    assert response.status_code == 400
    assert response.json["error"] == "Question is required"


def test_successful_ai_response(monkeypatch):
    fake_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(
                create=lambda **kwargs: SimpleNamespace(
                    choices=[
                        SimpleNamespace(
                            message=SimpleNamespace(
                                content="AI is intelligence demonstrated by machines."
                            )
                        )
                    ]
                )
            )
        )
    )

    monkeypatch.setattr(app_module, "client", fake_client)

    client = app_module.app.test_client()
    response = client.post(
        "/ask",
        json={"question": "What is AI?"}
    )

    assert response.status_code == 200
    assert response.json["question"] == "What is AI?"
    assert "AI is intelligence" in response.json["answer"]
