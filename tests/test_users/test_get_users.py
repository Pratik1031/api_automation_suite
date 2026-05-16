import pytest
from utils.validators import (
    assert_status, assert_schema, assert_response_time, assert_header,
    UserSchema,
)
from data.test_data import VALID_USER_IDS, INVALID_USER_IDS


class TestGetUsers:

    # ── Positive tests ────────────────────────────────────────────────────────

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_all_users_returns_200(self, client):
        response = client.get("/users")
        assert_status(response, 200)

    @pytest.mark.positive
    def test_get_all_users_returns_list(self, client):
        response = client.get("/users")
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    @pytest.mark.positive
    def test_get_all_users_schema_valid(self, client):
        response = client.get("/users")
        users = response.json()
        for user in users:
            assert_schema(user, UserSchema)

    @pytest.mark.positive
    def test_get_all_users_response_time(self, client):
        response = client.get("/users")
        assert_response_time(response, max_ms=3000)

    @pytest.mark.positive
    def test_get_all_users_content_type(self, client):
        response = client.get("/users")
        assert "application/json" in response.headers.get("Content-Type", "")

    @pytest.mark.positive
    @pytest.mark.parametrize("user_id", VALID_USER_IDS)
    def test_get_user_by_valid_id(self, client, user_id):
        response = client.get(f"/users/{user_id}")
        assert_status(response, 200)
        user = assert_schema(response.json(), UserSchema)
        assert user.id == user_id

    @pytest.mark.positive
    def test_get_user_has_required_fields(self, client):
        response = client.get("/users/1")
        data = response.json()
        required = {"id", "name", "username", "email"}
        assert required.issubset(data.keys()), (
            f"Missing fields: {required - data.keys()}"
        )

    # ── Negative tests ────────────────────────────────────────────────────────

    @pytest.mark.negative
    def test_get_user_not_found_returns_404(self, client):
        response = client.get("/users/9999999")
        assert_status(response, 404)

    @pytest.mark.negative
    def test_get_user_string_id_returns_error(self, client):
        response = client.get("/users/abc")
        assert response.status_code in (400, 404), (
            f"Expected 400 or 404, got {response.status_code}"
        )

    @pytest.mark.negative
    def test_get_user_negative_id_returns_error(self, client):
        response = client.get("/users/-1")
        assert response.status_code in (400, 404)

    @pytest.mark.negative
    def test_get_user_zero_id_returns_error(self, client):
        response = client.get("/users/0")
        assert response.status_code in (400, 404)

    @pytest.mark.negative
    def test_get_nonexistent_endpoint_returns_404(self, client):
        response = client.get("/nonexistent-endpoint")
        assert_status(response, 404)

    # ── Boundary tests ────────────────────────────────────────────────────────

    @pytest.mark.boundary
    def test_get_user_first_id(self, client):
        """Boundary: smallest valid user id."""
        response = client.get("/users/1")
        assert_status(response, 200)

    @pytest.mark.boundary
    def test_get_user_last_valid_id(self, client):
        """Boundary: last valid user in the dataset."""
        response = client.get("/users/10")
        assert_status(response, 200)

    @pytest.mark.boundary
    def test_get_user_just_beyond_last(self, client):
        """Boundary: one beyond the last valid id."""
        response = client.get("/users/11")
        assert response.status_code in (404, 200)

    @pytest.mark.boundary
    def test_get_users_with_query_filter(self, client):
        """Filter users by id query param — boundary of filter behaviour."""
        response = client.get("/users", params={"id": 1})
        assert_status(response, 200)
        data = response.json()
        assert isinstance(data, list)
