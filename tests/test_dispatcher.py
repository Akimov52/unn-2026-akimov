import unittest
from typing import Any

from bot.dispatcher import Dispatcher
from bot.handlers.handler import Handler, HandlerStatus
from bot.messenger import Messenger


class RecordingHandler(Handler):
    def __init__(
        self,
        can_handle_result: bool,
        result: HandlerStatus,
        calls: list[str],
        name: str,
    ) -> None:
        self._can_handle_result = can_handle_result
        self._result = result
        self._calls = calls
        self._name = name

    def can_handle(self, _update: dict[str, Any]) -> bool:
        self._calls.append(f"can:{self._name}")
        return self._can_handle_result

    def handle(self, _update: dict[str, Any], _messenger: Messenger) -> HandlerStatus:
        self._calls.append(f"handle:{self._name}")
        return self._result


class DispatcherTests(unittest.TestCase):
    def test_dispatch_stops_after_first_handler_returns_stop(self) -> None:
        calls: list[str] = []
        dispatcher = Dispatcher(messenger=None)  # type: ignore[arg-type]
        dispatcher.add_handlers(
            RecordingHandler(False, HandlerStatus.CONTINUE, calls, "first"),
            RecordingHandler(True, HandlerStatus.STOP, calls, "second"),
            RecordingHandler(True, HandlerStatus.STOP, calls, "third"),
        )

        dispatcher.dispatch({"update_id": 1})

        self.assertEqual(calls, ["can:first", "can:second", "handle:second"])

    def test_dispatch_does_nothing_when_no_handler_accepts_update(self) -> None:
        calls: list[str] = []
        dispatcher = Dispatcher(messenger=None)  # type: ignore[arg-type]
        dispatcher.add_handlers(
            RecordingHandler(False, HandlerStatus.CONTINUE, calls, "first"),
            RecordingHandler(False, HandlerStatus.CONTINUE, calls, "second"),
        )

        dispatcher.dispatch({"update_id": 2})

        self.assertEqual(calls, ["can:first", "can:second"])


if __name__ == "__main__":
    unittest.main()
