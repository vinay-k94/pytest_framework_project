import requests
from typing import Optional, Dict, Any
from framework.auth import TokenManager
from framework.errors import ApiError
from framework.logger import get_logger
import os

logger = get_logger(__name__)


class ApiClient:
    def __init__(self, base_url: str, auth_type: str = "none", provider: str = "dashboard"):
        """
        Initialize the API client with base URL, authentication type, and provider.
        Sets up session and token manager if authentication is enabled.
        """
        self.base_url = base_url
        self.auth_type = auth_type
        self.provider = provider
        self.timeout = 30  # seconds
        self.session = requests.Session()
        self.token_manager = None

        if self.auth_type != "none":
            self.token_manager = TokenManager(provider=self.provider)

    def _full_url(self, path: str) -> str:
        """
        Build the full URL for the API request.
        If the path is already a full URL, return as is.
        """
        if path.startswith("http"):
            return path
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    def _auth_header(self) -> dict:
        """
        Generate the authorization header if authentication is enabled.
        Returns an empty dict if no authentication.
        """
        # if self.auth_type == "none":
        #     return {}
        # token = self.token_manager.get_token()
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "User-Agent": "python-requests/2.x"
        }
        token = os.getenv(f'ACCESS_TOKEN_{os.getenv("ENV").upper()}')
        headers['Authorization'] = f"Bearer {token}"
        return headers

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        """
        Make a generic HTTP request using the specified method and path.
        Handles authentication headers and error handling.
        """
        url = self._full_url(path)
        headers = kwargs.pop("headers", {})
        headers.update(self._auth_header())
        try:
            resp = self.session.request(method, url, headers=headers, timeout=self.timeout, **kwargs)
        except requests.RequestException as e:
            raise ApiError(f"HTTP request failed: {e}")
        if resp.status_code >= 500:
            raise ApiError(f"Server error {resp.status_code}: {resp.text}")
        return resp

    def get(self, path: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        """
        Send a GET request to the specified path with optional query parameters.
        """
        return self.request("GET", path, params=params, **kwargs)

    def post(self, path: str, json: Optional[Any] = None, data: Optional[Any] = None, **kwargs) -> requests.Response:
        """
        Send a POST request to the specified path with optional JSON or form data.
        """
        return self.request("POST", path, json=json, data=data, **kwargs)

    def put(self, path: str, json: Optional[Any] = None, **kwargs) -> requests.Response:
        """
        Send a PUT request to the specified path with optional JSON data.
        """
        return self.request("PUT", path, json=json, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        """
        Send a DELETE request to the specified path.
        """
        return self.request("DELETE", path, **kwargs)
