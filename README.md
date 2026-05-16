# API Test Automation Suite

Production-ready REST API testing framework built with **Python**, **PyTest**, and **Pydantic**.  
Covers positive, negative, and boundary scenarios with data-driven design, schema validation, and CI-integrated regression runs.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.11+ |
| HTTP Client | `requests` |
| Test Runner | `pytest` |
| Schema Validation | `pydantic` v2 |
| Test Data | `faker` |
| Reporting | `pytest-html`, `allure-pytest` |
| Parallel Execution | `pytest-xdist` |
| CI/CD | GitHub Actions |

---

## Project Structure

```
api_automation_suite/
├── config/
│   └── settings.py          # Pydantic-based env config (local/staging/prod)
├── data/
│   └── test_data.py          # Centralised test data, Faker payloads, boundary sets
├── utils/
│   ├── api_client.py         # Base HTTP client (session, headers, timeout)
│   └── validators.py         # Pydantic schemas + assertion helpers
├── tests/
│   ├── conftest.py           # Shared fixtures (client, auth_client, created_post)
│   ├── test_users/
│   │   └── test_get_users.py # GET /users — positive, negative, boundary
│   ├── test_posts/
│   │   └── test_posts_crud.py# Full CRUD — create, read, update, delete
│   └── test_auth/
│       └── test_auth.py      # Auth header, token, and 401/403 patterns
├── reports/                  # HTML report output (git-ignored)
├── .env                      # Environment variables (git-ignored)
├── .github/workflows/ci.yml  # GitHub Actions — smoke + regression pipeline
├── pytest.ini                # Markers, paths, default flags
└── requirements.txt
```

---

## Quick Start

### 1. Clone & install

```bash
git clone https://github.com/Pratik1031/api-automation-suite
cd api_automation_suite
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env .env.local              # edit values as needed
```

Key variables in `.env`:

| Variable | Default | Description |
|---|---|---|
| `ENV` | `local` | Target environment: `local`, `staging`, `prod` |
| `BASE_URL_LOCAL` | JSONPlaceholder | API base URL for local |
| `BASE_URL_STAGING` | JSONPlaceholder | API base URL for staging |
| `API_KEY` | `test-api-key-123` | API key (if required) |
| `AUTH_TOKEN` | `Bearer test-token-abc` | Bearer token for auth tests |
| `REQUEST_TIMEOUT` | `10` | HTTP timeout in seconds |

### 3. Run tests

```bash
# Full suite
pytest

# Smoke tests only
pytest -m smoke

# Positive tests
pytest -m positive

# Negative tests
pytest -m negative

# Boundary tests
pytest -m boundary

# Specific module
pytest tests/test_posts/

# Parallel execution (auto-detect CPU cores)
pytest -n auto

# Against staging environment
ENV=staging pytest

# With live console output
pytest -s -v
```

### 4. View the report

After any run, open `reports/report.html` in your browser.

---

## Markers

| Marker | Description |
|---|---|
| `smoke` | Core happy-path tests — run on every commit |
| `regression` | Full regression suite — run nightly |
| `positive` | Valid inputs, expected success paths |
| `negative` | Invalid inputs, error handling, 4xx responses |
| `boundary` | Edge values (empty, max-length, zero, overflow) |
| `auth` | Authentication and authorisation tests |

---

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs automatically on push and PR:

```
Push / PR
   │
   ▼
┌─────────┐      pass      ┌────────────┐
│  Smoke  │ ────────────▶  │ Regression │
│  Tests  │                │  (parallel)│
└─────────┘                └────────────┘
                                  │
                                  ▼
                           HTML report uploaded
                           as build artifact
```

Nightly full regression also runs at 06:00 UTC.

---

## Adding a New API Endpoint

1. **Add schema** in `utils/validators.py`
2. **Add test data** in `data/test_data.py`
3. **Create test file** in `tests/test_<resource>/`
4. Cover: ≥3 positive, ≥3 negative, ≥3 boundary scenarios
5. Mark each test with the appropriate `@pytest.mark.*`

---

## Adapting to Your Real API

1. Update `BASE_URL_*` in `.env` to point to your API
2. Replace `UserSchema` / `PostSchema` in `validators.py` with your actual response models
3. Update `AUTH_TOKEN` / `API_KEY` with real credentials
4. Swap out `test_auth.py` endpoint to your actual protected routes

---

## License

MIT
