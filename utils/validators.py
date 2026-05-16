from pydantic import BaseModel, Field
from typing import Optional
import jsonschema


# ── Pydantic response models ─────────────────────────────────────────────────

class UserSchema(BaseModel):
    id: int
    name: str
    username: str
    email: str


class PostSchema(BaseModel):
    id: int
    userId: int
    title: str
    body: str


class CreatedPostSchema(BaseModel):
    id: int
    userId: int
    title: str
    body: str


class TokenSchema(BaseModel):
    token: str
    expiresIn: Optional[int] = None


# ── Generic assertion helpers ─────────────────────────────────────────────────

def assert_status(response, expected: int):
    assert response.status_code == expected, (
        f"Expected {expected}, got {response.status_code}. Body: {response.text[:300]}"
    )


def assert_schema(data: dict, model: type[BaseModel]) -> BaseModel:
    """Validate dict against a Pydantic model; returns the parsed instance."""
    return model.model_validate(data)


def assert_response_time(response, max_ms: int = 2000):
    elapsed = response.elapsed.total_seconds() * 1000
    assert elapsed <= max_ms, (
        f"Response time {elapsed:.0f}ms exceeded limit {max_ms}ms"
    )


def assert_header(response, header: str, expected_value: str = None):
    assert header in response.headers, f"Missing header: {header}"
    if expected_value:
        assert response.headers[header] == expected_value, (
            f"Header '{header}': expected '{expected_value}', "
            f"got '{response.headers[header]}'"
        )
