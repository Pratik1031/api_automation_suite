from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

ENV_URLS = {
    "local":   os.getenv("BASE_URL_LOCAL",   "https://jsonplaceholder.typicode.com"),
    "staging": os.getenv("BASE_URL_STAGING",  "https://jsonplaceholder.typicode.com"),
    "prod":    os.getenv("BASE_URL_PROD",     "https://jsonplaceholder.typicode.com"),
}


class Settings(BaseModel):
    env: str = os.getenv("ENV", "local")
    base_url: str = ""
    api_key: str = os.getenv("API_KEY", "")
    auth_token: str = os.getenv("AUTH_TOKEN", "")
    timeout: int = int(os.getenv("REQUEST_TIMEOUT", "10"))

    def model_post_init(self, __context):
        self.base_url = ENV_URLS.get(self.env, ENV_URLS["local"])


settings = Settings()
