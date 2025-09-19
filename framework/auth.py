import time
import jwt  # PyJWT
from typing import Optional, Dict
from config.config import AUTH_CONFIG
from framework.errors import AuthError
import requests


class TokenManager:
    def __init__(self, provider: str = "dashboard"):
        self.provider = provider
        self._token: Optional[str] = None
        self._expiry: float = 0.0

    def _fetch_token_from_provider(self) -> Dict:
        cfg = AUTH_CONFIG.get(self.provider)
        if not cfg or not cfg.get("token_url"):
            raise AuthError(f"No token_url configured for provider {self.provider}")
        resp = requests.post(cfg["token_url"], data={
            "client_id": cfg.get("client_id"),
            "client_secret": cfg.get("client_secret"),
            "grant_type": "client_credentials"
        }, timeout=10)
        if resp.status_code != 200:
            raise AuthError(f"Failed to fetch token: {resp.status_code} {resp.text}")
        return resp.json()

    def _set_token_from_jwt(self, token: str):
        self._token = token
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            self._expiry = payload.get("exp", time.time() + 300)
        except Exception:
            self._expiry = time.time() + 300

    def get_token(self) -> str:
        if not self._token or self._is_expiring_soon():
            self.refresh_token()
        return self._token

    def _is_expiring_soon(self, buffer_seconds=60) -> bool:
        return (self._expiry - time.time()) < buffer_seconds

    def refresh_token(self):
        data = self._fetch_token_from_provider()
        token = data.get("access_token") or data.get("token")
        if not token:
            raise AuthError("Provider response missing token")
        self._set_token_from_jwt(token)
