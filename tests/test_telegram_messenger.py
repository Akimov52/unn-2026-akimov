import json
import unittest
from unittest.mock import patch

from bot.telegram_messenger import TelegramMessenger


class FakeResponse:
    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return b'{"ok": true, "result": []}'


class TelegramMessengerTests(unittest.TestCase):
    def test_get_updates_uses_configured_base_url_and_token(self) -> None:
        messenger = TelegramMessenger(
            token="test-token",
            base_url="https://test.example/custom-api/",
        )

        with patch(
            "bot.telegram_messenger.urllib.request.urlopen",
            return_value=FakeResponse(),
        ) as urlopen:
            updates = messenger.get_updates(offset=0, timeout=30, allowed_updates=["message"])

        self.assertEqual(updates, [])
        request = urlopen.call_args.args[0]
        self.assertEqual(
            request.full_url,
            "https://test.example/custom-api/bottest-token/getUpdates",
        )
        self.assertEqual(request.method, "POST")
        self.assertEqual(
            json.loads(request.data),
            {"offset": 0, "timeout": 30, "allowed_updates": ["message"]},
        )


if __name__ == "__main__":
    unittest.main()
