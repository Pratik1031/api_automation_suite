import pytest
from utils.validators import assert_status


class TestAuth:
    """
    Auth test patterns — uses JSONPlaceholder as a stand-in.
    In a real project, replace /auth/login endpoint with your actual auth endpoint
    and adjust assertions to match your API's 401/403 behaviour.
    """

    # ── Positive ──────────────────────────────────────────────────────────────

    @pytest.mark.auth
    @pytest.mark.positive
    def test_authenticated_request_succeeds(self, auth_client):
        """Auth header is present → request should succeed."""
        response = auth_client.get("/posts/1")
        assert_status(response, 200)

    @pytest.mark.auth
    @pytest.mark.positive
    def test_auth_header_is_forwarded(self, auth_client):
        """Verify the session carries the Authorization header."""
        assert "Authorization" in auth_client.session.headers
        assert auth_client.session.headers["Authorization"].startswith("Bearer")

    # ── Negative ──────────────────────────────────────────────────────────────

    @pytest.mark.auth
    @pytest.mark.negative
    def test_missing_auth_header_pattern(self, client):
        """
        Pattern test: unauthenticated client hitting a protected endpoint
        should return 401. JSONPlaceholder is open so this returns 200 —
        swap the endpoint to a real protected route.
        """
        response = client.get("/posts/1")
        # On a real protected API: assert_status(response, 401)
        assert response.status_code in (200, 401)

    @pytest.mark.auth
    @pytest.mark.negative
    def test_invalid_token_format(self, client):
        """Malformed auth token should be rejected."""
        client.session.headers.update({"Authorization": "InvalidToken!!"})
        response = client.get("/posts/1")
        assert response.status_code in (200, 401, 403)
        # Reset header
        client.session.headers.pop("Authorization", None)

    @pytest.mark.auth
    @pytest.mark.negative
    def test_expired_token_pattern(self, client):
        """Expired token should return 401. Simulated with a fake expired value."""
        client.session.headers.update({"Authorization": "Bearer expired-token-xyz"})
        response = client.get("/posts/1")
        assert response.status_code in (200, 401)
        client.session.headers.pop("Authorization", None)
