"""FastAPI application for the orchestra daemon."""

from __future__ import annotations

import json
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocketState

from .auth import verify_jwt
from .config import load_settings
from .websocket import ConnectionManager, RateLimitError


app = FastAPI(title="Project Orchestra Daemon")
manager = ConnectionManager()


@app.on_event("startup")
async def startup_event() -> None:
    load_settings()


@app.get("/api/health")
async def health_check() -> JSONResponse:
    return JSONResponse({"status": "ok"})


@app.websocket("/ws/observe")
async def websocket_endpoint(websocket: WebSocket) -> None:
    settings = load_settings()
    token = websocket.query_params.get("token")
    if not token:
        if not settings.allow_insecure_ws:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        subject = "local-debug"
        metadata = {"scope": "observe", "mode": "insecure"}
    else:
        try:
            claims = verify_jwt(token)
        except Exception:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        subject = str(claims.get("sub", "unknown"))
        metadata = {"scope": "observe"}

    connection = await manager.connect(websocket, subject=subject, metadata=metadata)
    try:
        while True:
            data = await websocket.receive_json()
            try:
                envelope = await manager.handle_incoming(connection, data)
            except RateLimitError:
                await websocket.send_json({"type": "error", "error": "rate_limited"})
                await websocket.close(code=status.WS_1013_TRY_AGAIN_LATER)
                break
            await websocket.send_json({"type": "ack", "echo": envelope.get("type")})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    finally:
        if websocket.application_state != WebSocketState.DISCONNECTED:
            await websocket.close()
