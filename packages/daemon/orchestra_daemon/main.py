"""UVicorn entrypoint."""

from __future__ import annotations

import uvicorn

from .app import app


def run() -> None:  # pragma: no cover - thin wrapper
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run()
