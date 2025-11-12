import pytest

from orchestra_daemon import auth


def test_verify_jwt_success(auth_setup):
    token = auth_setup({"sub": "user-1", "aud": "test-audience", "iss": "https://example.com/"})
    claims = auth.verify_jwt(token)
    assert claims["sub"] == "user-1"


def test_verify_jwt_failure(auth_setup):
    with pytest.raises(Exception):
        auth.verify_jwt("invalid-token")
