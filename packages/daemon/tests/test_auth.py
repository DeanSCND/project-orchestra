import pytest
from fastapi import HTTPException
from jwt.exceptions import PyJWKClientError

from orchestra_daemon import auth
from orchestra_daemon.config import Settings


def test_verify_jwt_success(auth_setup):
    token = auth_setup({"sub": "user-1", "aud": "test-audience", "iss": "https://example.com/"})
    claims = auth.verify_jwt(token)
    assert claims["sub"] == "user-1"


def test_verify_jwt_failure(auth_setup):
    with pytest.raises(HTTPException) as excinfo:
        auth.verify_jwt("invalid-token")
    assert excinfo.value.status_code == 401


def test_verify_jwt_jwks_unavailable(monkeypatch):
    monkeypatch.setenv("AUTH0_DOMAIN", "example.com")
    monkeypatch.setenv("AUTH0_AUDIENCE", "test-audience")
    monkeypatch.setenv("AUTH0_ISSUER", "https://example.com/")

    class FailingClient:
        def get_signing_key_from_jwt(self, token: str):  # pragma: no cover - simple stub
            raise PyJWKClientError("jwks unreachable")

    def fake_settings():
        return Settings(
            auth0_domain="example.com",
            auth0_audience="test-audience",
            auth0_issuer="https://example.com/",
        )

    monkeypatch.setattr(auth, "_get_settings", lambda: fake_settings())
    monkeypatch.setattr(auth, "_get_jwks_client", lambda: FailingClient())

    with pytest.raises(HTTPException) as excinfo:
        auth.verify_jwt("any-token")

    assert excinfo.value.status_code == 503
