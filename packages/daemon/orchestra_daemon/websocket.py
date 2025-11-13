"""WebSocket connection management utilities."""

from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict, Iterable

from fastapi import WebSocket


class RateLimitError(RuntimeError):
    """Raised when a connection exceeds the allowed message rate."""


@dataclass
class Connection:
    websocket: WebSocket
    subject: str
    metadata: Dict[str, str]
    timestamps: Deque[float] = field(default_factory=lambda: deque(maxlen=20))

    def record_activity(self, max_per_second: int) -> None:
        now = time.monotonic()
        while self.timestamps and now - self.timestamps[0] > 1:
            self.timestamps.popleft()
        if len(self.timestamps) >= max_per_second:
            raise RateLimitError
        self.timestamps.append(now)


class ConnectionManager:
    def __init__(self, *, max_messages_per_second: int = 10) -> None:
        self._connections: Dict[int, Connection] = {}
        self._max_messages_per_second = max_messages_per_second

    async def connect(self, websocket: WebSocket, *, subject: str, metadata: Dict[str, str]) -> Connection:
        await websocket.accept()
        connection = Connection(websocket=websocket, subject=subject, metadata=metadata)
        self._connections[id(websocket)] = connection
        return connection

    def disconnect(self, websocket: WebSocket) -> None:
        self._connections.pop(id(websocket), None)

    async def broadcast(self, payload: Dict) -> None:
        for connection in list(self._connections.values()):
            await connection.websocket.send_json(payload)

    async def handle_incoming(self, connection: Connection, message: Dict) -> Dict:
        connection.record_activity(self._max_messages_per_second)
        if not isinstance(message, dict) or "type" not in message:
            return {"type": "error", "error": "invalid_message"}

        envelope = {
            "type": message.get("type"),
            "payload": message.get("payload"),
            "from": connection.subject,
            "meta": connection.metadata,
        }
        await self.broadcast(envelope)
        return envelope

    def list_subjects(self) -> Iterable[str]:
        return [conn.subject for conn in self._connections.values()]
