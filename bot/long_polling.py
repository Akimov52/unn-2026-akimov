import logging
import time
from typing import Any

from bot.dispatcher import Dispatcher
from bot.messenger import Messenger

POLLING_TIMEOUT = 30
RETRY_DELAY = 5

logger = logging.getLogger(__name__)


def poll_once(dispatcher: Dispatcher, messenger: Messenger, offset: int) -> int:
    updates = messenger.get_updates(
        offset=offset,
        timeout=POLLING_TIMEOUT,
        allowed_updates=["message"],
    )

    for update in updates:
        update_id: Any = update.get("update_id")
        if isinstance(update_id, int):
            offset = max(offset, update_id + 1)
        dispatcher.dispatch(update)

    return offset


def start_long_polling(dispatcher: Dispatcher, messenger: Messenger) -> None:
    offset = 0
    while True:
        try:
            offset = poll_once(dispatcher, messenger, offset)
        except Exception:
            logger.exception("Polling failed; retrying in %s seconds", RETRY_DELAY)
            time.sleep(RETRY_DELAY)
