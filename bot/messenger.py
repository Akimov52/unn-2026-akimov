from abc import ABC, abstractmethod
from typing import Any


class Messenger(ABC):
    @abstractmethod
    def get_updates(self, **params: object) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def send_message(self, **params: object) -> dict[str, Any]:
        raise NotImplementedError
