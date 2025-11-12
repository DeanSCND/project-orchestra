from typing import Dict

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from jwt import encode

from orchestra_daemon import auth
from orchestra_daemon.config import Settings


@pytest.fixture(autouse=True)
def clear_caches():
    if hasattr(auth._get_settings, "cache_clear"):
        auth._get_settings.cache_clear()
    if hasattr(auth._get_jwks_client, "cache_clear"):
        auth._get_jwks_client.cache_clear()
    yield
    if hasattr(auth._get_settings, "cache_clear"):
        auth._get_settings.cache_clear()
    if hasattr(auth._get_jwks_client, "cache_clear"):
        auth._get_jwks_client.cache_clear()


@pytest.fixture
def rsa_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


@pytest.fixture
def auth_setup(monkeypatch, rsa_keys):
    private_pem, public_pem = rsa_keys
    monkeypatch.setenv("AUTH0_DOMAIN", "example.com")
    monkeypatch.setenv("AUTH0_AUDIENCE", "test-audience")
    monkeypatch.setenv("AUTH0_ISSUER", "https://example.com/")

    def fake_settings() -> Settings:
        return Settings(
            auth0_domain="example.com",
            auth0_audience="test-audience",
            auth0_issuer="https://example.com/",
        )

    class DummyKey:
        def __init__(self, key: bytes) -> None:
            self.key = key

    class DummyClient:
        def __init__(self, key: bytes) -> None:
            self._key = key

        def get_signing_key_from_jwt(self, token: str) -> DummyKey:
            return DummyKey(self._key)

    monkeypatch.setattr(auth, "_get_settings", lambda: fake_settings())
    monkeypatch.setattr(auth, "_get_jwks_client", lambda: DummyClient(public_pem))

    def make_token(claims: Dict) -> str:
        headers = {"kid": "test-key"}
        return encode(claims, private_pem, algorithm="RS256", headers=headers)

    return make_token


@pytest.fixture
def client():
    from orchestra_daemon.app import app
    from fastapi.testclient import TestClient

    return TestClient(app)
