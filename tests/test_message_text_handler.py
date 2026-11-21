import unittest
from typing import Any
from unittest.mock import Mock

from bot.handlers.handler import HandlerStatus
from bot.handlers.message_text import MessageTextHandler
from bot.messenger import Messenger


class MessageTextHandlerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.handler = MessageTextHandler()
        self.messenger = Mock(spec=Messenger)

    def test_can_handle_text_message(self) -> None:
        update: dict[str, Any] = {
            "update_id": 1,
            "message": {"text": "Hello", "chat": {"id": 123}},
        }

        self.assertTrue(self.handler.can_handle(update))

    def test_ignores_non_text_updates(self) -> None:
        updates: list[dict[str, Any]] = [
            {"update_id": 2, "message": {"photo": [], "chat": {"id": 123}}},
            {"update_id": 3, "message": {"sticker": {}, "chat": {"id": 123}}},
            {"update_id": 4, "callback_query": {"data": "button"}},
            {"update_id": 5, "message": {"chat": {"id": 123}}},
        ]

        for update in updates:
            with self.subTest(update=update):
                self.assertFalse(self.handler.can_handle(update))

    def test_handle_sends_the_same_text_to_the_same_chat(self) -> None:
        update: dict[str, Any] = {
            "update_id": 6,
            "message": {"text": "Echo exactly!", "chat": {"id": 987654}},
        }

        result = self.handler.handle(update, self.messenger)

        self.assertEqual(result, HandlerStatus.STOP)
        self.messenger.send_message.assert_called_once_with(
            chat_id=987654,
            text="Echo exactly!",
        )


if __name__ == "__main__":
    unittest.main()
