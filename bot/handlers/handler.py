from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any

from bot.messenger import Messenger


class HandlerStatus(Enum):
    CONTINUE = auto()
    STOP = auto()


class Handler(ABC):
    @abstractmethod
    def can_handle(self, update: dict[str, Any]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def handle(self, update: dict[str, Any], messenger: Messenger) -> HandlerStatus:
        raise NotImplementedError
