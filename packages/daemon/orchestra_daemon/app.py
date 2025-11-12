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
    token = websocket.query_params.get("token")
    if token:
        try:
            claims = verify_jwt(token)
        except Exception:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        subject = str(claims.get("sub", "unknown"))
        metadata = {"scope": "observe"}
    else:
        subject = "local-debug"
        metadata = {"scope": "observe", "mode": "insecure"}

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
