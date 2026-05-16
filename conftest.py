import pytest
from utils.api_client import APIClient
from config.settings import settings


@pytest.fixture(scope="session")
def client() -> APIClient:
    """Session-scoped API client shared across all tests."""
    return APIClient()


@pytest.fixture(scope="session")
def auth_client() -> APIClient:
    """API client pre-configured with auth header."""
    c = APIClient()
    c.set_auth_header(settings.auth_token)
    return c


@pytest.fixture
def created_post(client):
    """
    Create a post before a test, yield its data, then clean up.
    JSONPlaceholder doesn't persist state so delete is a no-op here —
    pattern is correct for real APIs.
    """
    from data.test_data import valid_post_payload
    response = client.post("/posts", valid_post_payload())
    post = response.json()
    yield post
    client.delete(f"/posts/{post['id']}")
