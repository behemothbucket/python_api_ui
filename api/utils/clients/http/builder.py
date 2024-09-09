from api.utils.clients.http.client import HTTPClient
from settings.base import base_settings

api = base_settings.api


def get_http_client(base_url: str) -> HTTPClient:
    return HTTPClient(base_url=base_url, trust_env=True)
