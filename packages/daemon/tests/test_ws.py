import pytest
from starlette.websockets import WebSocketDisconnect


def test_websocket_requires_token(client):
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/ws/observe"):
            pass


def test_websocket_flow(client, auth_setup):
    token = auth_setup({"sub": "user-1", "aud": "test-audience", "iss": "https://example.com/"})
    with client.websocket_connect(f"/ws/observe?token={token}") as websocket:
        websocket.send_json({"type": "ping", "payload": {"value": 1}})
        broadcast = websocket.receive_json()
        ack = websocket.receive_json()
        assert broadcast["type"] == "ping"
        assert broadcast["from"] == "user-1"
        assert ack == {"type": "ack", "echo": "ping"}


def test_websocket_rate_limit(client, auth_setup):
    token = auth_setup({"sub": "user-2", "aud": "test-audience", "iss": "https://example.com/"})
    with client.websocket_connect(f"/ws/observe?token={token}") as websocket:
        for i in range(10):
            websocket.send_json({"type": "ping", "payload": {"value": i}})
            websocket.receive_json()
            websocket.receive_json()

        websocket.send_json({"type": "ping", "payload": {"value": 11}})
        error_message = websocket.receive_json()
        assert error_message["type"] == "error"
        with pytest.raises((RuntimeError, WebSocketDisconnect)):
            websocket.receive_json()
