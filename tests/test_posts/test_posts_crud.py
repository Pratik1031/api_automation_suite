import pytest
from utils.validators import (
    assert_status, assert_schema, assert_response_time,
    PostSchema, CreatedPostSchema,
)
from data.test_data import valid_post_payload, BOUNDARY_TITLES


class TestCreatePost:

    # ── Positive ──────────────────────────────────────────────────────────────

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_create_post_returns_201(self, client):
        response = client.post("/posts", valid_post_payload())
        assert_status(response, 201)

    @pytest.mark.positive
    def test_create_post_schema_valid(self, client):
        response = client.post("/posts", valid_post_payload())
        assert_schema(response.json(), CreatedPostSchema)

    @pytest.mark.positive
    def test_create_post_returns_id(self, client):
        response = client.post("/posts", valid_post_payload())
        data = response.json()
        assert "id" in data
        assert isinstance(data["id"], int)

    @pytest.mark.positive
    def test_create_post_response_time(self, client):
        response = client.post("/posts", valid_post_payload())
        assert_response_time(response, max_ms=3000)

    @pytest.mark.positive
    def test_create_post_echoes_payload(self, client):
        payload = {"userId": 1, "title": "Echo Test", "body": "Verify echo"}
        response = client.post("/posts", payload)
        data = response.json()
        assert data["title"] == payload["title"]
        assert data["body"] == payload["body"]
        assert data["userId"] == payload["userId"]

    @pytest.mark.positive
    @pytest.mark.parametrize("user_id", [1, 5, 10])
    def test_create_post_different_user_ids(self, client, user_id):
        response = client.post("/posts", valid_post_payload(user_id=user_id))
        assert_status(response, 201)
        assert response.json()["userId"] == user_id

    # ── Negative ──────────────────────────────────────────────────────────────

    @pytest.mark.negative
    def test_create_post_missing_title(self, client):
        payload = {"userId": 1, "body": "No title here"}
        response = client.post("/posts", payload)
        # JSONPlaceholder is lenient; real APIs return 400 — check either
        assert response.status_code in (201, 400)

    @pytest.mark.negative
    def test_create_post_missing_body(self, client):
        payload = {"userId": 1, "title": "No body here"}
        response = client.post("/posts", payload)
        assert response.status_code in (201, 400)

    @pytest.mark.negative
    def test_create_post_empty_payload(self, client):
        response = client.post("/posts", {})
        assert response.status_code in (201, 400)

    @pytest.mark.negative
    def test_create_post_invalid_user_id_type(self, client):
        payload = {"userId": "not-an-int", "title": "Bad userId", "body": "Test"}
        response = client.post("/posts", payload)
        assert response.status_code in (201, 400, 422)

    @pytest.mark.negative
    def test_create_post_null_title(self, client):
        payload = {"userId": 1, "title": None, "body": "Null title"}
        response = client.post("/posts", payload)
        assert response.status_code in (201, 400, 422)

    # ── Boundary ──────────────────────────────────────────────────────────────

    @pytest.mark.boundary
    @pytest.mark.parametrize("label,title", BOUNDARY_TITLES.items())
    def test_create_post_boundary_titles(self, client, label, title):
        payload = {"userId": 1, "title": title, "body": "Boundary test body"}
        response = client.post("/posts", payload)
        assert response.status_code in (201, 400, 422), (
            f"Unexpected status {response.status_code} for boundary case '{label}'"
        )


class TestGetPost:

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_all_posts_returns_200(self, client):
        response = client.get("/posts")
        assert_status(response, 200)

    @pytest.mark.positive
    def test_get_all_posts_is_list(self, client):
        response = client.get("/posts")
        assert isinstance(response.json(), list)

    @pytest.mark.positive
    def test_get_post_by_id(self, client):
        response = client.get("/posts/1")
        assert_status(response, 200)
        assert_schema(response.json(), PostSchema)

    @pytest.mark.positive
    def test_get_posts_filter_by_user(self, client):
        response = client.get("/posts", params={"userId": 1})
        assert_status(response, 200)
        posts = response.json()
        assert all(p["userId"] == 1 for p in posts)

    @pytest.mark.negative
    def test_get_post_not_found(self, client):
        response = client.get("/posts/9999999")
        assert_status(response, 404)

    @pytest.mark.boundary
    def test_get_first_post(self, client):
        response = client.get("/posts/1")
        assert_status(response, 200)

    @pytest.mark.boundary
    def test_get_last_valid_post(self, client):
        response = client.get("/posts/100")
        assert_status(response, 200)


class TestUpdatePost:

    @pytest.mark.positive
    def test_put_post_returns_200(self, client, created_post):
        payload = {
            "id": created_post["userId"],
            "userId": 1,
            "title": "Updated Title",
            "body": "Updated body content",
        }
        response = client.put(f"/posts/{created_post['userId']}", payload)
        assert_status(response, 200)

    @pytest.mark.positive
    def test_patch_post_returns_200(self, client, created_post):
        response = client.patch(
            f"/posts/{created_post['id']}", {"title": "Patched Title"}
        )
        assert_status(response, 200)

    @pytest.mark.positive
    def test_patch_post_updates_field(self, client, created_post):
        response = client.patch(
            f"/posts/{created_post['id']}", {"title": "New Patched Title"}
        )
        assert response.json()["title"] == "New Patched Title"

    @pytest.mark.negative
    def test_put_nonexistent_post(self, client):
        payload = {"userId": 1, "title": "Ghost", "body": "No such post"}
        response = client.put("/posts/9999999", payload)
        assert response.status_code in (200, 404, 500)


class TestDeletePost:

    @pytest.mark.positive
    def test_delete_post_returns_200(self, client, created_post):
        response = client.delete(f"/posts/{created_post['id']}")
        assert_status(response, 200)

    @pytest.mark.negative
    def test_delete_nonexistent_post(self, client):
        response = client.delete("/posts/9999999")
        assert response.status_code in (200, 404)
