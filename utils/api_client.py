import requests
from config.settings import settings


class APIClient:
    """
    Base HTTP client. Wraps requests with shared headers,
    base URL, timeout, and response logging.
    """

    def __init__(self):
        self.base_url = settings.base_url
        self.timeout = settings.timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"

    def get(self, endpoint: str, params: dict = None, **kwargs) -> requests.Response:
        return self.session.get(
            self._url(endpoint), params=params, timeout=self.timeout, **kwargs
        )

    def post(self, endpoint: str, payload: dict = None, **kwargs) -> requests.Response:
        return self.session.post(
            self._url(endpoint), json=payload, timeout=self.timeout, **kwargs
        )

    def put(self, endpoint: str, payload: dict = None, **kwargs) -> requests.Response:
        return self.session.put(
            self._url(endpoint), json=payload, timeout=self.timeout, **kwargs
        )

    def patch(self, endpoint: str, payload: dict = None, **kwargs) -> requests.Response:
        return self.session.patch(
            self._url(endpoint), json=payload, timeout=self.timeout, **kwargs
        )

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self.session.delete(self._url(endpoint), timeout=self.timeout, **kwargs)

    def set_auth_header(self, token: str):
        self.session.headers.update({"Authorization": token})
