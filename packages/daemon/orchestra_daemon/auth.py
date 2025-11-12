"""JWT authentication utilities for the orchestra daemon."""

from __future__ import annotations

from functools import lru_cache
from typing import Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient, decode
from jwt.exceptions import InvalidTokenError

from .config import Settings, load_settings


bearer_scheme = HTTPBearer(auto_error=False)


@lru_cache(maxsize=1)
def _get_settings() -> Settings:
    return load_settings()


@lru_cache(maxsize=1)
def _get_jwks_client() -> PyJWKClient:
    settings = _get_settings()
    return PyJWKClient(settings.jwks_url)


def verify_jwt(token: str) -> Dict:
    settings = _get_settings()
    client = _get_jwks_client()
    try:
        signing_key = client.get_signing_key_from_jwt(token)
        claims = decode(
            token,
            signing_key.key,
            algorithms=[settings.auth0_algorithm],
            audience=settings.auth0_audience,
            issuer=settings.auth0_issuer,
        )
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_token") from exc
    return claims


async def auth_dependency(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> Dict:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_token")
    return verify_jwt(credentials.credentials)
