import json
import urllib.request
from typing import Any

from bot.messenger import Messenger

REQUEST_TIMEOUT = 40


class TelegramMessenger(Messenger):
    def __init__(self, token: str, base_url: str) -> None:
        self._url = f"{base_url.rstrip('/')}/bot{token}"

    def get_updates(self, **params: object) -> list[dict[str, Any]]:
        result = self._request("getUpdates", params)
        if not isinstance(result, list):
            raise RuntimeError("Telegram API returned an invalid updates list")
        return result

    def send_message(self, **params: object) -> dict[str, Any]:
        result = self._request("sendMessage", params)
        if not isinstance(result, dict):
            raise RuntimeError("Telegram API returned an invalid message result")
        return result

    def _request(self, method: str, params: dict[str, object]) -> Any:
        request = urllib.request.Request(
            url=f"{self._url}/{method}",
            data=json.dumps(params).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            payload: dict[str, Any] = json.loads(response.read())

        if not payload.get("ok", False):
            raise RuntimeError(str(payload.get("description", "Telegram API request failed")))

        return payload.get("result")
