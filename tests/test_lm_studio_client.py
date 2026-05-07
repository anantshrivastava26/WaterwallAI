from ai import lm_studio_client


class DummyResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class DummyHttpClient:
    def __init__(self, *args, **kwargs):
        self.called = None
        self._payload = {"output": [{"type": "message", "content": "ok"}]}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def post(self, url, json, headers):
        self.called = {"url": url, "json": json, "headers": headers}
        return DummyResponse(self._payload)


def test_chat_posts_to_native_rest_endpoint(monkeypatch):
    holder = {}

    def _factory(*args, **kwargs):
        inst = DummyHttpClient(*args, **kwargs)
        holder["client"] = inst
        return inst

    monkeypatch.setattr(lm_studio_client.httpx, "Client", _factory)

    out = lm_studio_client.chat("sys", "usr", temperature=0.5, max_tokens=42)

    assert out == "ok"
    called = holder["client"].called
    assert called["url"].endswith("/api/v1/chat")
    body = called["json"]
    assert body["input"] == "usr"
    assert body["system_prompt"] == "sys"
    assert body["temperature"] == 0.5
    assert body["max_output_tokens"] == 42
    assert body["stream"] is False
    assert body["model"] == lm_studio_client.settings.lm_studio_model


def test_chat_joins_multiple_message_outputs(monkeypatch):
    def _factory(*args, **kwargs):
        inst = DummyHttpClient(*args, **kwargs)
        inst._payload = {
            "output": [
                {"type": "message", "content": "hello"},
                {"type": "reasoning", "content": "ignored"},
                {"type": "message", "content": "world"},
            ]
        }
        return inst

    monkeypatch.setattr(lm_studio_client.httpx, "Client", _factory)

    assert lm_studio_client.chat("s", "u") == "hello\nworld"
