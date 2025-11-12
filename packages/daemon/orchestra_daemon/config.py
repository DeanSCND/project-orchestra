"""Configuration loading for the orchestra daemon."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


DEFAULT_ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


@dataclass(frozen=True)
class Settings:
    auth0_domain: str
    auth0_audience: str
    auth0_issuer: str
    auth0_algorithm: str = "RS256"
    read_timeout_seconds: int = 30
    allow_insecure_ws: bool = False

    @property
    def jwks_url(self) -> str:
        return f"https://{self.auth0_domain}/.well-known/jwks.json"


def load_settings(env_path: Optional[Path] = None) -> Settings:
    load_dotenv(env_path or DEFAULT_ENV_PATH)
    import os

    domain = os.getenv("AUTH0_DOMAIN")
    audience = os.getenv("AUTH0_AUDIENCE")
    issuer = os.getenv("AUTH0_ISSUER") or (f"https://{domain}/" if domain else None)

    insecure_flag = os.getenv("ORCHESTRA_DAEMON_ALLOW_INSECURE_WS", "0").lower()
    allow_insecure_ws = insecure_flag in {"1", "true", "yes"}

    if not domain or not audience or not issuer:
        if not allow_insecure_ws:
            raise RuntimeError("AUTH0_DOMAIN, AUTH0_AUDIENCE, and AUTH0_ISSUER must be set")
        # Provide placeholders for local insecure mode.
        domain = domain or "local.example"
        audience = audience or "local-audience"
        issuer = issuer or "https://local.example/"

    algorithm = os.getenv("AUTH0_ALGORITHM", "RS256")
    timeout = int(os.getenv("DAEMON_READ_TIMEOUT_SECONDS", "30"))

    return Settings(
        auth0_domain=domain,
        auth0_audience=audience,
        auth0_issuer=issuer,
        auth0_algorithm=algorithm,
        read_timeout_seconds=timeout,
        allow_insecure_ws=allow_insecure_ws,
    )
