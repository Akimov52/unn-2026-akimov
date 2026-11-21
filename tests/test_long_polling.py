import unittest
from unittest.mock import Mock, call, patch

from bot.long_polling import POLLING_TIMEOUT, RETRY_DELAY, poll_once, start_long_polling
from bot.messenger import Messenger


class LongPollingTests(unittest.TestCase):
    def test_poll_once_dispatches_batch_and_advances_offset(self) -> None:
        messenger = Mock(spec=Messenger)
        dispatcher = Mock()
        messenger.get_updates.return_value = [
            {"update_id": 12, "message": {"text": "first"}},
            {"update_id": 14, "message": {"text": "second"}},
            {"update_id": 13, "message": {"text": "third"}},
        ]

        next_offset = poll_once(dispatcher, messenger, offset=10)

        self.assertEqual(next_offset, 15)
        messenger.get_updates.assert_called_once_with(
            offset=10,
            timeout=POLLING_TIMEOUT,
            allowed_updates=["message"],
        )
        dispatcher.dispatch.assert_has_calls(
            [
                call({"update_id": 12, "message": {"text": "first"}}),
                call({"update_id": 14, "message": {"text": "second"}}),
                call({"update_id": 13, "message": {"text": "third"}}),
            ]
        )
        self.assertEqual(dispatcher.dispatch.call_count, 3)

    def test_poll_once_keeps_offset_when_no_updates_arrive(self) -> None:
        messenger = Mock(spec=Messenger)
        dispatcher = Mock()
        messenger.get_updates.return_value = []

        next_offset = poll_once(dispatcher, messenger, offset=42)

        self.assertEqual(next_offset, 42)
        dispatcher.dispatch.assert_not_called()

    def test_polling_retries_after_error_and_stops_on_keyboard_interrupt(self) -> None:
        dispatcher = Mock()
        messenger = Mock(spec=Messenger)

        with (
            self.assertLogs("bot.long_polling", level="ERROR"),
            patch(
                "bot.long_polling.poll_once",
                side_effect=[RuntimeError("network error"), KeyboardInterrupt],
            ) as poll_mock,
            patch("bot.long_polling.time.sleep") as sleep_mock,
            self.assertRaises(KeyboardInterrupt),
        ):
            start_long_polling(dispatcher, messenger)

        self.assertEqual(poll_mock.call_count, 2)
        sleep_mock.assert_called_once_with(RETRY_DELAY)


if __name__ == "__main__":
    unittest.main()
